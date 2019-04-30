from googlevoice import Voice
import yaml
import sys

#opens up local .yml file to read values for email and password.
conf = yaml.load(open('./config.yml'))
email = conf['user']['email']
pwd = conf['user']['password']
dir = conf['user']['dir']

#This will authenticate with Google Voice via the email and password variables in config.yml, and then download each voicemail in the account as .mp3
def voicemail_get():
    voice = Voice()
    client = voice.login(email, pwd)

    #This will download each voicemail in the account as mp3 to the variable dir from config.yml
    for message in voice.voicemail().messages:
        message.download(dir)

#This will check if credentials are set in config.yml
def creds_check():

    for k, v in conf.items():
        if v == None:
            print("\nPlease edit the config.yml file to include your email and password credentials.")
        else:
            voicemail_get()
            print("\nSuccess! Downloaded all voicemail files in account " + str(email))

creds_check()
