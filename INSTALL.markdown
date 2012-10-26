INSTALL
-------

To install or upgrade IMAPClient (main dependency) via PyPI use pip:

```
pip install imapclient 
pip install --upgrade imapclient
```

Or using  EasyInstall:

```
easy_install IMAPClient
easy_install --upgrade IMAPClient
```

Your Python installation is supposed to have the ```email``` module by the way. Tests have been done using Python 2.7.3rc2.

Once you're set just run the script, it will create a basic config file so you can edit your username, password and eventually the IMAP server (though Google's is always the same). The config file is in ~/.LostPhotosFound/config by default.
