#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

# common fs/system call
import os
import sys

# for configuration file
import ConfigParser

class Config:
    """
    Configuration file manager

    Locate, open and read configuration file options, creates a template
    if no configuration file is found (default is ~/.LostPhotosFound/config)
    """
    def __init__(self):
        self._file = os.path.join(_app_folder(), 'config')

        if not os.path.isfile(self._file):
            self._create_file()

        self._config = ConfigParser.ConfigParser()
        self._config.read(self._file)

    def get(self, section, option):
        """
        Get and return a given config field, i.e. username

        @param section: likely to be your mail service, i.e. gmail
        @param option: the field you want to retrieve from the config
        """
        return self._config.get(section, option)

    def _create_file(self):
        """Internal function to create a dummy config file if none is found"""

        config = ConfigParser.ConfigParser()
        config.add_section('gmail')
        config.set('gmail', 'host', 'imap.gmail.com')
        config.set('gmail', 'username', 'username@gmail.com')
        config.set('gmail', 'password', 'password')

        with open(self._file, 'w') as configfile:
            config.write(configfile)

        print '\nPlease edit your config file %s\n' % (self._file)
        sys.exit()

def _app_folder():
    """
    Internal function to return the app folder in user's home in a multi-OS way
    """
    dir = os.path.expanduser('~/.LostPhotosFound')
    if not os.path.isdir(dir):
        os.mkdir(dir, 0700)
    return dir
