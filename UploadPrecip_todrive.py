# -*- coding: utf-8 -*-
"""
Created on Oct 9 2019

@author: Alimatou Seck

Description: This code publishes LLFS precip data to Google drive.
Inputs needed: clients_secret.json, mycreds.txt, .csv precip file and directory
               , google drive folder id
Arguments: directory where the prep file is located
"""

#modules------------------------------------------------------------------------
from pydrive.auth import GoogleAuth #need to install this (with pip)
from pydrive.drive import GoogleDrive
import sys
import time
#-------------------------------------------------------------------------------

#inputs-------------------------------------------------------------------------

#directory containing files to publish
###maindir = "/home/user1/MODEL/p52fc05_sa/output/icprb/" #replaced with argument
maindir = sys.argv[1]
print (maindir)

#name of the file to be publish
drive_file_name1 = "MergeMASP_PRC.csv" 

#name of file and directory
precip_file1 = maindir + "/" + drive_file_name1  
#print (precip_file1)

#creditential file containing google drive authentication
creds_file = "mycreds.txt"

#id of google drive folder
fid = '1pRRs6RcJBSGYTs_epGvkJUcDBXGI7Fcj'
#-------------------------------------------------------------------------------


#timing the code
start = time. time()

#-------------------------------------------------------------------------------


#Authentication
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

#-----------------------------------------------------------------------------

#Upload file
###Need to use variable for google folder id###
file_list = drive.ListFile({'q':"'1pRRs6RcJBSGYTs_epGvkJUcDBXGI7Fcj' in parents and trashed=False"}).GetList()
try:
        for file1 in file_list:
            if file1['title'] == drive_file_name1:
                file1.Delete()
                print ("deleted file")                
except:
        pass
f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})
f['title'] = drive_file_name1 # Change title.
f.SetContentFile(precip_file1)
f.Upload()
#-----------------------------------------------------------------------------

#timing
end = time. time()
print(end - start)