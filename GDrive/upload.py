from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
import glob, os

conf = yaml.load(open('./config.yml'))
folder = conf['folderid']['id']
dir = conf['directory']['dir']
title = conf['directory']['title']

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

#Upload file to specified folder. Specific folder ID can be found with 'folderid.py'
    def upload_voicemail(fid):

        if dir == None:
            print("\n********** No directory path set! Please set directory with voicemail mp3's in the config.yml file. **********")
        elif fid == None:
            os.chdir(dir)
            for mp3 in glob.glob("*.mp3"):
                f = (dir + str("/"+mp3))
                print ("Uploading" + str(f) + " To default root G Drive directory...")
                #If the fid value does not exist, the file will upload to the default GDrive directory
                file = drive.CreateFile()
                file.SetContentFile(f)
                file.Upload()
                print("\nUploaded!\n")
        else:
            os.chdir(dir)
            for mp3 in glob.glob("*.mp3"):
                f = (dir + str("/"+mp3))
                print ("Uploading" + str(f) +" \nTo folder " + str(title) + " \nWith ID: " + str(fid))
                #If the fid value does not exist, the file will upload to the default GDrive directory
                file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})
                file.SetContentFile(f)
                file.Upload()
                print("\nUploaded!\n")

    #Create folder with metadata. You can change the title of the folder to any string value.
    def create_folder():

        folder_metadata = {'title' : title, 'mimeType' : 'application/vnd.google-apps.folder'}
        print("Creating folder...\n")
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        print("Folder created! \n")

        #Gets parent folder ID. Make sure to put the parent ID of the folder you want into config.yml
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print ('title: %s, id: %s' % (file1['title'], file1['id']))
        fid = input("\nEnter the folder ID of the folder you want to upload to: ")
        upload_voicemail(fid)

    def folderid_check():

        fid = folder

        for k, v in conf['folderid'].items():
            if v == None:
                prompt = input("Will you be uploading the .mp3 file to a specific folder? (Y or N): ")
                if prompt == "Y":
                    prompt = input("Do you have the file ID of the folder you want to upload to? (Y or N): ")
                    if prompt == "Y":
                        fid = input("Enter your folder ID: ")
                        upload_voicemail(fid)
                    elif prompt == "N":
                        print("Creating folder. Make sure to note down the folder ID. \nYou can either put it in the config.yml file (Recommended) \nOR re-do the program and say 'Y' to the previous question.")
                        create_folder()
                elif prompt == "N":
                    upload_voicemail(fid)
            else:
                upload_voicemail(fid)

    folderid_check()

auth()
