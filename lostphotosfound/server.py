#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

import os
import sys

# to avoid image duplicates
import hashlib

# for the mime list (all images extensions)
import mimetypes

# for the index
import shelve

# to build the mail object and pickle fields
from email import message_from_string
from email.utils import parsedate

# the working man (should we connect to IMAP as a read-only client btw?)
from imapclient import IMAPClient

from lostphotosfound.utils import _app_folder
from lostphotosfound.utils import _charset_decoder

class Server:
    """
    Server class to fetch and filter data

    Connects to the IMAP server, search according to a criteria,
    fetch all attachments of the mails matching the criteria and
    save them locally with a timestamp
    """
    def __init__(self, host, username, password, debug=False):
        """
        Server class __init__ which expects an IMAP host to connect to

        @param host: gmail's default server is fine: imap.gmail.com
        @param username: your gmail account (i.e. obama@gmail.com)
        @param password: we highly recommend you to use 2-factor auth here
        """

        if not host:
            raise Exception('Missing IMAP host parameter in your config')

        try:
            self._server = IMAPClient(host, use_uid=True, ssl=True)
        except:
            raise Exception('Could not successfully connect to the IMAP host')

        setattr(self._server, 'debug', debug)

        # mails index to avoid unnecessary redownloading
        index = '.index_%s' % (username)
        index = os.path.join(_app_folder(), index)
        self._index = shelve.open(index, writeback=True)

        # list of attachments hashes to avoid dupes
        hashes = '.hashes_%s' % (username)
        hashes = os.path.join(_app_folder(), hashes)
        self._hashes = shelve.open(hashes, writeback=True)

        self._username = username
        self._login(username, password)

    def _login(self, username, password):
        """
        Login to the IMAP server and selects the all mail folder
       
        @param username: your gmail account (i.e. obama@gmail.com)
        @param password: we highly recommend you to use 2-factor auth here
        """

        if not username or not password:
            raise Exception('Missing username or password parameters')

        # you may want to hack this to only fetch attachments from a
        # different exclusive label (assuming you have them in english)
        all_mail = '[Gmail]/All Mail'
        
        try:
            self._server.login(username, password)
        except:
            raise Exception('Cannot login, check username/password, are you using 2-factor auth?')

        # this is how we get the all mail folder even if the user's
        # gmail interface is in another language, not in english
        if not self._server.folder_exists(all_mail):
            for folder in self._server.xlist_folders():
                labels = folder[0]
                if 'AllMail' in labels[-1]:
                    all_mail = folder[2]

        self._server.select_folder(all_mail)

    def _filter_messages(self):
        """Filter mail to only parse ones containing images"""

        # creates a list of all types of image files to search for,
        # even though we have no idea if gmail supports them or what
        mimetypes.init()
        mimes = []
        for ext in mimetypes.types_map:
            if 'image' in mimetypes.types_map[ext]:
                mimes.append(ext.replace('.', ''))
        mimelist = ' OR '.join(mimes)
        
        # that's why we only support gmail
        # for other mail services we'd have to translate the custom
        # search to actual IMAP queries, thus no X-GM-RAW cookie for us
        criteria = 'X-GM-RAW "has:attachment filename:(%s)"' % (mimelist)
        try:
            messages = self._server.search([criteria])
        except:
            raise Exception('Search criteria return a failure, it must be a valid gmail search')    

        # stats logging
        print 'LOG: %d messages matched the search criteria %s' % (len(messages), criteria)
        return messages
 
    def lostphotosfound(self):
        """The actual program, which fetchs the mails and all its parts attachments"""

        messages = self._filter_messages()

        for msg in messages:
            try:
                idfetched = self._server.fetch([msg], ['X-GM-MSGID'])
            except:
                raise Exception('Could not fetch the message ID, server did not respond')

            msgid = str(idfetched[idfetched.keys()[0]]['X-GM-MSGID'])

            # mail has been processed in the past, skip it
            if msgid in self._index.keys():
                print 'Skipping X-GM-MSDID %s' % (msgid)
                continue

            # if it hasn't, fetch it and iterate through its parts
            msgdata = self._server.fetch([msg], ['RFC822'])

            for data in msgdata:
                mail = message_from_string(msgdata[data]['RFC822'])
                if mail.get_content_maintype() != 'multipart':
                    continue

                # logging
                header_from = _charset_decoder(mail['From'])
                header_subject = _charset_decoder(mail['Subject'])
                print '[%s]: %s' % (header_from, header_subject)
                
                for part in mail.walk():
                    # if it's only plain text, i.e. no images
                    if part.get_content_maintype() == 'multipart':
                        continue                   
                    # if no explicit attachments unless they're inline
                    if part.get('Content-Disposition') is None:
                        pass
                    # if non-graphic inline data
                    if not 'image/' in part.get_content_type():
                        continue
                    
                    # only then we can save this mail part
                    self._save_part(part, mail)

                # all parts of mail processed, add it to the index
                self._index[msgid] = msgid

    def _save_part(self, part, mail):
        """
        Internal function to decode attachment filenames and save them all

        @param mail: the mail object from message_from_string so it can checks its date
        @param part: the part object after a mail.walk() to get multiple attachments
        """

        if not hasattr(self, "seq"):
            self.seq = 0
        
        # we check if None in filename instead of just if it is None
        # due to the type of data decode_header returns to us
        header_filename = _charset_decoder(part.get_filename())

        # i.e. some inline attachments have no filename field in the header
        # so we have to hack around it and get the name field
        if 'None' in header_filename:
            header_filename = part.get('Content-Type').split('name=')[-1].replace('"', '')
        elif not header_filename[0][0] or header_filename[0][0] is None:
            # we should hopefully never reach this, attachments would be 'noname' in gmail
            header_filename = 'attachment-%06d.data' % (self.seq)
            self.seq += 1

        # sanitize it
        punct = '!"#$&\'*+/;<>?[\]^`{|}~'
        header_filename = header_filename.translate(None, punct)

        # 2012-10-28_19-15-22 (Y-M-D_H-M-S)
        header_date = parsedate(mail['date'])
        header_date = '%s-%s-%s_%s-%s-%s_' % (header_date[0],
                                              header_date[1],
                                              header_date[2],
                                              header_date[3],
                                              header_date[4],
                                              header_date[5])
        filename = header_date + header_filename

        # we should create it in the documents folder
        username = self._username
        userdir = os.path.expanduser('~/LostPhotosFound')
        savepath = os.path.join(userdir, username)
        if not os.path.isdir(savepath):
            os.makedirs(savepath)
    
        # logging complement
        print '\t...%s' % (filename)

        saved = os.path.join(savepath, filename)
        if not os.path.isfile(saved):
            with open(saved, 'wb') as imagefile:
                try:
                    payload = part.get_payload(decode=True)
                except:
                    message = 'Failed when downloading attachment: %s' % (saved)
                    raise Exception(message)

                hash = hashlib.sha1(payload).hexdigest()
                # gmail loves to duplicate attachments in replies
                if hash not in self._hashes.keys():
                    try:
                        imagefile.write(payload)
                    except:
                        message = 'Failed writing attachment to file: %s' % (saved)
                        raise Exception(message)
                    self._hashes[hash] = hash
                else:
                    print 'Duplicated attachment %s (%s)' % (saved, hash)
                    os.remove(saved)
    
    def close(self):
        """Gracefully sync/close indexes and disconnects from the IMAP server"""

        self._index.sync()
        self._index.close()
        self._hashes.sync()
        self._hashes.close()
        self._server.close_folder()
        self._server.logout()
