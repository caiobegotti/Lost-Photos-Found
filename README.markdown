Lost-Photos-Found
===============

Recover all your images buried deep in Gmail! It's actually better than LostPhotos (another similar app for Mac and Windows) because we support ALL types of images you may have in your mails, and can locate and save inline images as well. These days people just drag & drop images onto messages, so LostPhotos wont' work for you here, but we will!

Installation and usage
----------------------

To install the basic dependencies via PyPI:

```
pip install -r requirements.txt
```

Your Python installation is supposed to have the ```email``` module by the way. Tests have been done using Python 2.7.x.

Once your environment is ready just run ```./lpf.py```. It will create a basic config file and aks for your credentials. The config file is in ~/.LostPhotosFound/config by default, if you ever need to change it.

Your password will be stored in your system's keychain not in the config file, don't worry. The app works just fine with Google's 2-step authentication too, just provide an app specific password for it and you're good.

Development
-----------

Wanna help? Fork it and pick your favorite from the ```TODO``` section below. It's a GPL project, real open source and free.

TODO
----

- Generic IMAP server support, not just Gmail's?
