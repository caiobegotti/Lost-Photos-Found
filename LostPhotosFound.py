#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code is under GPLv2
# <caio1982@gmail.com>
#
# INSTALL:
#	pip install imapclient
#	pip install --upgrade imapclient
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
    criteria = 'X-GM-RAW "has:attachment filename:(jpg OR jpeg OR gif OR png OR tiff OR tif OR ico OR xbm OR bmp)"'
    messages = server.search([criteria])

    # stats
    print 'LOG: %d messages matched the search criteria %s' % (len(messages), criteria)
    return messages
 
def save_part(part):
    if not hasattr(save_part, "seq"):
        save_part.seq = 0;

    filename = part.get_filename()
    if not filename:
        filename = 'attachment-%06d.bin' % (save_part.seq)
	save_part.seq += 1

    if not os.path.isdir(USERNAME):
        os.mkdir(USERNAME)

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
                save_part(part)

server = get_server(HOST, USERNAME, PASSWORD)
messages = get_messages(server)
filter_content(messages)    
server.close_folder()
server.logout()
