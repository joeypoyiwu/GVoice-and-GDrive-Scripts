# GVoice and GDrive Upload

## Prerequisites

**MUST** have Python 3+ installed.

1. [PyGoogleVoice](https://github.com/pettazz/pygooglevoice) setup and installed. Run `setup.py` upon download.
2. [PyDrive](https://pypi.org/project/PyDrive/) setup and installed.
3. A `client_secrets.json` file for [PyDrive](https://pythonhosted.org/PyDrive/quickstart.html)

For each folder in GDrive and GVoice, input your necessary values in the `config_template.yml` files, and rename them to `config.yml` after editting:

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

The current `upload.py` file authenticates the user, and saves the credentials and refreshes the tokens if they are expired.

If you do not want this, and instead want authentication to go through the Web Client everytime, edit `auth()` from:

```python
from pydrive.auth import GoogleAuth

def auth():
    #Authentication for G Drive API with PyDrive
    print("Authenticating...")
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        print("Opening up web client to authenticate...")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
    # Refresh them if expired
        print("Refreshing token...")
        gauth.Refresh()
    else:
        # Initialize the saved creds
        print("Authorized!\n")
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)
```

to:

```python
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
# Create local webserver and auto handles authentication.
gauth.LocalWebserverAuth()
```

### KNOWN ISSUES

Unfortunately, `pygooglevoice` is not officially supported by Google. [This link](https://github.com/pettazz/pygooglevoice/pull/40) aptly describes why accounts with 2FA enabled will not work.

For `voicemail_download.py` to work properly, please **disable 2FA**.

Contact:
>[Email](joeywu99@gmail.com)
