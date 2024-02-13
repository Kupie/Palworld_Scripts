SAVES_FOLDER = 'C:\\Users\\Admin\\Desktop\\SAVE_BACKUP\\'
gdrive_creds = 'C:\\Users\\Admin\\Desktop\\PALWORLD_SCRIPTS\\gdrive_creds.txt'

from os import listdir
from os.path import isfile, join
import os
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


secrets_file = os.path.normpath("C:/Users/Admin/Desktop/PALWORLD_SCRIPTS/client_secrets.json")
settings_file = os.path.normpath("C:/Users/Admin/Desktop/PALWORLD_SCRIPTS/gdrive_creds_2.txt")

gauth = GoogleAuth(settings_file=settings_file)

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = secrets_file
gdriveFolderID = '1sTBJ5AJGdHFBb_9mq9qffzsVfU8rgBLs'

from os import listdir
from os.path import isfile, join
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile(gdrive_creds)
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(gdrive_creds)

drive = GoogleDrive(gauth)

saveFilesList = [f for f in listdir(SAVES_FOLDER) if isfile(join(SAVES_FOLDER, f))]

query_str = "\'" + gdriveFolderID + "\'" + " in parents and trashed=false"    

alreadyUploaded = []
file_list = drive.ListFile({'q': query_str}).GetList()
for file in file_list:
	alreadyUploaded.append(file['title'])
	#print('title: %s, id: %s' % (file['title'], file['id']))


for fileName in saveFilesList:
	if fileName not in alreadyUploaded:
		print('Uploading: ' + fileName)
		# Upload file to folder
		file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": gdriveFolderID}], 'title': fileName})
		file.SetContentFile(SAVES_FOLDER + fileName)
		file.Upload()
	else:
		print('Already Uploaded: ' + fileName)
