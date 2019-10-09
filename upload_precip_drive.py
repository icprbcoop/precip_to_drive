# -*- coding: utf-8 -*-
"""
Created on Oct 9 2019
@author: Alimatou_S
"""
"""
#pydrive needs to be installed (pip install PyDrive)
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
"""
"""
file1 = drive.CreateFile({'title': 'Hello.txt'})  
file1.SetContentString('Hello World!') 
file1.Upload()
"""
"""
precip_file1= "/home/user1/MODEL/p52fc05_sa/output/icprb/MergeMASP_PRC.csv"
#file_path = "/home/user1/MODEL/ICPRBextras/ExtrasV1.0/csv_to_sheets/csv_to_drive/document.txt"
file1 = drive.CreateFile(metadata={"title": "masp.csv"})
file1.SetContentFile(precip_file1)
file1.Upload()
"""

#modules
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


#inputs
precip_file1 = "MergeMASP_PRC.csv"
creds_file = "mycreds.txt"

#outputs
drive_masp_file = "masp.csv"

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile(creds_file)
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
gauth.SaveCredentialsFile(creds_file)

drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
try:
        for file1 in file_list:
            if file1['title'] == drive_masp_file:
                file1.Delete()
                f = drive.CreateFile()
                f.SetContentFile(file)
                f.Upload()
            else:
                f = drive.CreateFile()
                f.SetContentFile(file)
                f.Upload()
except:
    pass
© 2019 GitHub, Inc.