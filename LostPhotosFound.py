#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code is under GPLv2
# <caio1982@gmail.com>
#
# INSTALL:
#	sudo easy_install -U distribute && easy_install IMAPClient
#
# TODO:
#	- avoid looping through messages already processed (i.e. resume support)
#	- save the attached images with a timestamp or "comment" with date/time etc
#	- create a simple interface with pyqt like an album frame (QFileSystemWatcher?)
#	- CLI options for host, username, password, folder, criteria and attachment size
#	- is_multipart() seems better if attachment is too big/inline (it crashes)
#	- better (real) debug logging :-)

# to save the images
import os

# to build the mail object and pickle fields
from email import message_from_string
from email.header import decode_header

# the working man (should we connect to IMAP as a read-only client btw?)
from imapclient import IMAPClient

HOST = 'imap.gmail.com'
USERNAME = 'username@gmail.com'
PASSWORD = 'password'
ALL_MAIL = '[Gmail]/All Mail'
SSL = True

try:
    server = IMAPClient(HOST, use_uid=True, ssl=SSL)
except:
    raise Exception('Could not successfully connect to the IMAP host')

server.login(USERNAME, PASSWORD)

if not server.folder_exists(ALL_MAIL):
    for folder in server.xlist_folders():
        labels = folder[0]
        if 'AllMail' in labels[-1]:
            ALL_MAIL = folder[2]

server.select_folder(ALL_MAIL)

    #print "Available folders:"
    #for f in server.list_folders():
    #    print f[-1]
    #raise Exception('Your "All Mail" label is either not visible or in another language!')

# that's why we only support gmail
# for other mail services we'd have to translate the custom
# search to actual IMAP queries, thus no X-GM-RAW cookie to us
criteria = 'X-GM-RAW "has:attachment filename:(jpg OR jpeg OR gif OR png OR tiff OR tif OR ico OR xbm OR bmp)"'
messages = server.search([criteria])

# stats
print 'LOG: %d messages matched the search criteria %s' % (len(messages), criteria)

for m in messages:
    data = server.fetch([m], ['RFC822'])
    for d in data:
        # SEQ is also available
        mail = message_from_string(data[d]['RFC822'])
        if mail.get_content_maintype() != 'multipart':
            continue
        
        # this whole mess up to the print statement
        # is only for debugging purposes :-(
        header_from = mail["From"]
        if not decode_header(header_from).pop(0)[1]:
            header_from = decode_header(header_from).pop(0)[0].decode('iso-8859-1').encode('utf-8')
        else:
            header_from = decode_header(header_from).pop(0)[0].decode(decode_header(header_from).pop(0)[1]).encode('utf-8')
        
        header_subject = mail["Subject"]
        if not decode_header(header_subject).pop(0)[1]:
            header_subject = decode_header(header_subject).pop(0)[0].decode('iso-8859-1').encode('utf-8')
        else:
            header_subject = decode_header(header_subject).pop(0)[0].decode(decode_header(header_subject).pop(0)[1]).encode('utf-8')
        
        print '[%s]: %s' % (header_from, header_subject)

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            seq = 1
            if not filename:
                filename = 'attachment-%03d%s' % (seq, 'bin')
                seq += 1
            if not os.path.isdir(USERNAME):
                os.mkdir(USERNAME)
            saved = os.path.join(USERNAME, filename)
            if not os.path.isfile(saved):
                f = open(saved, 'wb')
                f.write(part.get_payload(decode=True))
                f.close()

server.close_folder()
server.logout()
