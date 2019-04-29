from googlevoice import Voice
import yaml
import sys

#opens up local .yml file to read values for email and password.
conf = yaml.load(open('./config.yml'))
email = conf['user']['email']
pwd = conf['user']['password']
dir = './voicemails'

def voicemail_get():
    voice = Voice()
    client = voice.login(email, pwd)

    for message in voice.voicemail().messages:
        message.download(dir)

def creds_check():

    for k, v in conf.items():
        if v == None:
            print("Please edit the config.yml file to include your email and password credentials.")
        else:
            voicemail_get()
            print("Success!")

creds_check()
