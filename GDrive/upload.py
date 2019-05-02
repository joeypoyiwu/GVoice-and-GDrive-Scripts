from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
import glob, os

#opens the config.yml file, and passes the variables over here as a dict
conf = yaml.load(open('./config.yml'))
folder = conf['folderid']['id']
dir = conf['directory']['dir']
title = conf['directory']['title']

#Authentication for G Drive API with PyDrive
def auth():
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
    auth_ok = GoogleDrive(gauth)
    # Returns the auth value to the function
    return auth_ok

#Upload file to specified folder. Specific folder ID can be found with 'folderid.py'
def upload_voicemail(fid, drive):

    #Print reminder if no directory variable was set in config.yml
    if dir == None:
        print("\n********** No directory path set! Please set directory with voicemail mp3's in the config.yml file. **********")
    #Uploads mp3 files to default GDrive root if no folderid was set in config.yml
    elif fid == None:
        os.chdir(dir)
        #this will look for any files in the dir variable with the extension .mp3, and upload each.
        for mp3 in glob.glob("*.mp3"):
            f = (dir + str("/"+mp3))
            print ("Uploading " + str(f) + " to default root G Drive directory...")
            #If the fid value does not exist, the file will upload to the default GDrive directory
            file = drive.CreateFile()
            file.SetContentFile(f)
            file.Upload()
            print("\nUploaded!\n")
    #If folderid and dir variables are present in config.yml, voicemails will be uploaded to specified GDrive folder
    else:
        os.chdir(dir)
        for mp3 in glob.glob("*.mp3"):
            f = (dir + str("/"+mp3))
            print ("Uploading: " + str(f) +" \nTo folder: " + str(title) + " \nWith ID: " + str(fid))
            #If the fid value does not exist, the file will upload to the default GDrive directory
            file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})
            file.SetContentFile(f)
            file.Upload()
            print("\nUploaded!\n")

#Create folder with metadata. You can change the title of the folder to any string value.
def create_folder(drive):

    folder_metadata = {'title' : title, 'mimeType' : 'application/vnd.google-apps.folder'}
    print("Creating folder...\n")
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    print("Folder created! \nBe sure to enter this folder ID into your config.yml file!")

    #Gets parent folder ID. Make sure to put the parent ID of the folder you want into config.yml
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print ('title: %s, id: %s' % (file1['title'], file1['id']))
    fid = input("\nEnter the folder ID of the folder you want to upload to: ")
    upload_voicemail(fid, drive)

#prompts user to either upload files to a specific folder or not. It will them prompt the user to create a folder if they do not have a folderid.
def main():

    # Assigns auth value from auth() to object 'drive'
    drive = auth()
    fid = folder

    for k, v in conf['folderid'].items():
        if v == None:
            prompt = input("\nWill you be uploading the .mp3 file to a specific folder? (Y or N): ")
            if prompt == "Y":
                prompt = input("\nDo you have the file ID of the folder you want to upload to? (Y or N): ")
                if prompt == "Y":
                    fid = input("\nEnter your folder ID: ")
                    upload_voicemail(fid, drive)
                elif prompt == "N":
                    print("\nCreating folder. Make sure to note down the folder ID. \nYou can either put it in the config.yml file (Recommended) \nOR re-do the program and say 'Y' to the previous question.")
                    create_folder(drive)
            elif prompt == "N":
                upload_voicemail(fid, drive)
        else:
            upload_voicemail(fid, drive)

main()
