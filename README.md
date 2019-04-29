# GVoice and GDrive Upload

## Prerequisites

**MUST** have Python 3+ installed.

- [PyGoogleVoice](https://github.com/pettazz/pygooglevoice) setup and installed.
- [PyDrive](https://pypi.org/project/PyDrive/) setup and installed.
- A `client_secrets.json` file for [PyDrive](https://pythonhosted.org/PyDrive/quickstart.html)

For each folder in GDrive and GVoice, input your necessary values in the `config_template.yml` files.

### EXAMPLE

For `config_template.yml` in the folder `GDrive`:
```
folderid:
  id: exampleID
directory:
  dir: ~/path/to/file
  title: title to give
```

For `config_template.yml` in the folder `GVoice`:
```
user:
    email: youremail@domain.com
    password: email password
```

### How To

Run `main.sh` to download all voicemails in your Google Voice account, and have it upload to your Google Drive account.

You can specify a specific folder to upload the file to, or just upload it to your root directory.

If you would like to run both separately:

**Google Voice Voicemail Download** - Set directory to download the .mp3 files of voicemails to in `config_template.yml`, then run `voicemail_download.py`

**Google Drive Upload** - Set the directory to pull the .mp3 files of voicemails in `config_template.yml`, then run `upload.py`
