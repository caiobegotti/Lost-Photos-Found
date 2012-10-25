#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code is under GPLv2
# <caio1982@gmail.com>

# to build the mail object and pickle fields
import email

# the working man (should we connect to IMAP as a read-only client btw?)
from imapclient import IMAPClient

HOST = 'imap.gmail.com'
USERNAME = 'username@gmail.com'
PASSWORD = 'password'
SSL = True

server = IMAPClient(HOST, use_uid=True, ssl=SSL)
server.login(USERNAME, PASSWORD)

server.select_folder('[Gmail]/All Mail')

# that's why we only support gmail
# for other mail services we'd have to translate the custom
# search to actual IMAP queries, thus no X-GM-RAW cookie to us
messages = server.search(['X-GM-RAW "has:attachment filename:(jpg OR jpeg OR gif OR png OR tiff OR tif OR ico OR xbm OR bmp)"'])

# stats
print '%d messages with attachments' % (len(messages),)

for m in messages:
    data = server.fetch([m], ['RFC822'])
    for d in data:
        # SEQ is also available
        body = email.message_from_string(data[d]['RFC822'])
        print body['Subject']
