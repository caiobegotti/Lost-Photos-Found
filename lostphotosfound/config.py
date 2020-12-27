#!/usr/bin/env python
# -*- coding: utf-8 -*-
# same license, author and
# credits of the main script

# common fs/system call
import os

# for configuration file
import configparser

# keychain/keyring storage
import keyring
import getpass

from lostphotosfound.utils import _app_folder

SECTION = 'lost-photos-found'

class Config:
    """Configuration file manager (default is ~/.LostPhotosFound/config)"""

    def __init__(self):
        self._file = os.path.join(_app_folder(), 'config')
        self._config = configparser.ConfigParser()
        self._config.read(self._file)

        if not self._config.has_option(SECTION, 'username'):
            self._setup()

        username = self._config.get(SECTION, 'username')
        password = keyring.get_password(SECTION, username)
        self._config.set(SECTION, 'password', password)

    def _setup(self):
        """Function to create a config file and store password in system keychain"""

        config = configparser.ConfigParser()
        config.add_section(SECTION)

        username = input("Gmail username: ")
        if "@" not in username:
            username += "@gmail.com"

        password = getpass.getpass("Password: ")

        config.set(SECTION, 'host', 'imap.gmail.com')
        config.set(SECTION, 'username', username)
        keyring.set_password(SECTION, username, password)

        with open(self._file, 'w') as configfile:
            config.write(configfile)

        self._config.read(self._file)

        print("\nSetup saved at {}, your password is in the system keychain!".format(self._file))
        print("If you want to change any parameter, just delete the config file to start over.\n")

    def get(self, option):
        """Get and return a given config field, i.e. username"""

        return self._config.get(SECTION, option)
