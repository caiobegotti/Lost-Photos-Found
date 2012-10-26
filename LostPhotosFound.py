#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code is under GPLv2
# <caio1982@gmail.com>

import os
import time

# to build the mail object and pickle fields
from email import message_from_string
from email.header import decode_header
from email.utils import parsedate

# the working man (should we connect to IMAP as a read-only client btw?)
from imapclient import IMAPClient

# for configuration file
import ConfigParser
import sys


def get_server(host, username, password):
    all_mail = '[Gmail]/All Mail'
    try:
        server = IMAPClient(host, use_uid=True, ssl=True)
    except:
        raise Exception('Could not successfully connect to the IMAP host')

    server.login(username, password)

    if not server.folder_exists(all_mail):
        for folder in server.xlist_folders():
            labels = folder[0]
            if 'AllMail' in labels[-1]:
                all_mail = folder[2]

    server.select_folder(all_mail)
    return server

def get_messages(server):
    # that's why we only support gmail
    # for other mail services we'd have to translate the custom
    # search to actual IMAP queries, thus no X-GM-RAW cookie to us
    criteria = 'X-GM-RAW "has:attachment filename:(jpg OR
                                                  jpeg OR
                                                   gif OR
                                                   png OR
                                                  tiff OR
                                                   tif OR
                                                   ico OR
                                                   xbm OR
                                                   bmp)"'
    messages = server.search([criteria])

    # stats
    print 'LOG: %d messages matched the search criteria %s' % (len(messages), criteria)
    return messages
 
def save_part(part, mail):
    if not hasattr(save_part, "seq"):
        save_part.seq = 0;

    filename = decode_header(part.get_filename()).pop(0)[0].decode('iso-8859-1').encode('utf-8')
    if not filename:
        filename = 'attachment-%06d.bin' % (save_part.seq)
	save_part.seq += 1
    
    header_date = parsedate(mail['date'])
    header_date = '%s-%s-%s_%s:%s:%s_' % (header_date[0],
                                          header_date[1],
                                          header_date[2],
                                          header_date[3],
                                          header_date[4],
                                          header_date[5])
    filename = header_date + filename

    if not os.path.isdir(USERNAME):
        os.mkdir(USERNAME)

    print '\t...%s' % (filename)

    saved = os.path.join(USERNAME, filename)
    if not os.path.isfile(saved):
        f = open(saved, 'wb')
        f.write(part.get_payload(decode=True))
        f.close()
 
def filter_content(messages):
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
                save_part(part, mail)

class Config:
    """ Configuration file manager

    Locate, open and read configuration file options. Create a template
    if no configuration file is found.

    """
    def __init__(self):
        self._dir = os.path.expanduser('~/.LostPhotosFound')
        self._file = os.path.join(self._dir, 'config')

        if not os.path.isdir(self._dir):
            os.mkdir(self._dir, 0700)
            self._create_file()
        elif not os.path.isfile(self._file):
            self._create_file()
        
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._file)

    def get(self, section, option):
        return self._config.get(section, option)

    def _create_file(self):
        config = ConfigParser.ConfigParser()
        config.add_section('Gmail')
        config.set('Gmail', 'host', 'imap.gmail.com')
        config.set('Gmail', 'username', 'username@gmail.com')
        config.set('Gmail', 'password', 'password')

        with open(self._file, 'w') as configfile:
            config.write(configfile)

        print '\nPlease edit your config file %s\n' % (self._file)
        sys.exit()

config = Config()
host = config.get('Gmail', 'host')
username = config.get('Gmail', 'username')
password = config.get('Gmail', 'password')

server = get_server(host, username, password)
messages = get_messages(server)
filter_content(messages)    
server.close_folder()
server.logout()
