# -*- coding: utf-8 -*-
"""
Created on Oct 9 2019

@author: Alimatou Seck

Description: This code publishes LLFS precip data to Google drive.
Inputs needed: clients_secret.json, mycreds.txt, .csv precip file and directory
               , google drive folder id
Arguments: directory where the precip file is located
"""

#modules------------------------------------------------------------------------
from pydrive.auth import GoogleAuth #need to install this (with pip)
from pydrive.drive import GoogleDrive
import sys
import time
import pandas as pd
import datetime as dt
import numpy as np
from shutil import copyfile
#-------------------------------------------------------------------------------

#inputs-------------------------------------------------------------------------

#directory containing files to publish
###maindir = "/home/user1/MODEL/p52fc05_sa/output/icprb/" #replaced with argument
maindir = sys.argv[1]
print (maindir)

#name of the file to be publish
###add list
drive_file_name1 = "MergeMASP_PRC.csv" 
drive_file_name2 = "MergeMASP_PRC_weighted.csv" 

#name of file and directory
###add list
precip_file1 = maindir + "/" + drive_file_name1
precip_file2 = maindir + "/" + drive_file_name2
#print (precip_file1)

#name of file containing area weight coefficients
weight_file = "weight1.csv"


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

#uplaod original files from FEWS
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

#calculate area weighted average precipitation
list_ = []
weight = pd.read_csv(weight_file, header=0,  skiprows=[1], sep=',')
df = pd.read_csv(precip_file1, index_col=0, header=0, skiprows=[1],  sep=',', parse_dates=[0],  date_parser= pd.datetools.to_datetime)
list_.append(df)
frame = pd.concat(list_)
frame[frame == -999] = np.nan
test1 = frame
test1.to_csv('out1.csv')

test2 = pd.DataFrame(test1.values*weight.values, columns=test1.columns, index=test1.index)

test3 = test1
test3['weight_avg'] = test2.sum(skipna=False,axis=1)
test3['avg'] = test1.mean(axis=1)

test3.to_csv('out3.csv')
#-------------------------------------------------------------------------------

#upload weight averaged precip

precip_out1 = "out3.csv"
#save weight averaged file to ICPRB output directory
copyfile(precip_out1, precip_file2)
#uplaod original files from FEWS
###Need to use variable for google folder id###
file_list = drive.ListFile({'q':"'1pRRs6RcJBSGYTs_epGvkJUcDBXGI7Fcj' in parents and trashed=False"}).GetList()
try:
        for file1 in file_list:
            if file1['title'] == drive_file_name2:
                file1.Delete()
                print ("deleted file")                
except:
        pass
f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})
f['title'] = drive_file_name2 # Change title.
f.SetContentFile(precip_file2)
f.Upload()

#-------------------------------------------------------------------------------

#timing
end = time. time()
print(end - start)