LostPhotosFound
===============

Linux version of the LostPhotos application for Mac/Windows. Well, it's actually better than LostPhotos because we support ALL types of images you may have in your mails, and can locate and save inline images as well. These days people just drag & drop images onto messages, so LostPhotos wont' work for you here, but we will!

Installation and usage
----------------------

To install the basic dependencies via PyPI:

```
pip install imapclient
pip install chardet
```

Your Python installation is supposed to have the ```email``` module by the way. Tests have been done using Python 2.7.3rc2.

Once your environment is ready just run ```./lpf.py```. It will create a basic config file so you can edit your username, password and eventually the IMAP server (though Google's is always the same). The config file is in ~/.LostPhotosFound/config by default and it works just fine with 2-step authentication.

Development
-----------

Wanna help? Fork it and pick your favorite from the ```TODO``` section below. It's a GPL project, real open source and free.

TODO
----

- Use python-keyring instead of handling passwords on our own
- create a simple interface with pyqt like an album frame (QFileSystemWatcher?)
- CLI options for host, username, password, folder, criteria and attachment size
- Better (real) debug logging :-)
- Statistics!
