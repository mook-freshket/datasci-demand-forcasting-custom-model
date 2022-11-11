#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import pandas as pd
import os
import shutil

from google.oauth2 import service_account
import gspread
import gspread_dataframe as gd


# In[2]:




# This file will read response from googleform and create new folder and config file within that folder only if the folder is not there.

# # Read response

# In[3]:


#save to gsheet
#get credential path & setup scope
path_for_credential = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#create credential + scope
credentials = service_account.Credentials.from_service_account_file(path_for_credential)
scoped_credentials = credentials.with_scopes(scope)

#authorize credential
gc = gspread.authorize(scoped_credentials)

#setup spreadsheet_name / key
spreadsheet_key = '1XdlBrLi0E3CN9ks7lsMak8Ms8WsugQb9sBxgQeT7UiY'
wks_name = 'Form Responses 1'
#read current gspread, convert to dataframe,drop null
ws = gc.open_by_key(spreadsheet_key).worksheet(wks_name)
existing = gd.get_as_dataframe(ws)
#drop column Unname
existing = existing.drop(columns=[c for c in existing.columns if 'Unnamed' in c])
#drop null row
existing = existing.dropna(subset=['Model Name'])

response = existing.copy()
response.columns = [c.strip().lower().replace(" ","_") for c in response.columns]
response.columns


# # Create Dir + files

# In[4]:


file_list = os.listdir()
file_list = [f for f in file_list if ('.py' in f)]
file_list


# In[5]:


response.model_name = response.model_name.str.lower().str.replace(" ","_")


# In[13]:


#read every name in file
for name in response['model_name']:
    if os.path.isdir(name): #check whether the path is created
        print('Folder is already created')
    else: #if not
        os.mkdir(name) #create folder
        print('Folder is created')        
        #save config file
        config = response.loc[response.model_name==name]
        config.to_csv(f"{name}/config.csv",index=False)
        
    for file in file_list:
        #move py file
        if file == 'dag_demand_forecast_custom_model_tuning.py':
            new_filename = f'dag_demand_forecast_{name}_model_tuning.py'
            original = f"{file}"
            target = f"{name}/{new_filename}"
            shutil.copyfile(original, target)
        elif file == 'dag_demand_forecast_custom_model_prediction.py':
            new_filename = f'dag_demand_forecast_{name}_model_prediction.py'
            original = f"{file}"
            target = f"{name}/{new_filename}"
            shutil.copyfile(original, target)
        else:
            original = f"{file}"
            target = f"{name}/{file}"
            shutil.copyfile(original, target)




