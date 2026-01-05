
"""
Processes Uber receipt PDFs and uploads normalized records to Quickbase.
"""

import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd 
from dotenv import load_dotenv
import requests
import numpy as np
import paramiko_downloader

load_dotenv()
REALM = os.getenv("REALM")
TABLE_ID = os.getenv("TABLE_ID")
TOKEN = os.getenv("QB_TOKEN")
REPORT_ID = os.getenv("PROJECT_CODE_REPORT_ID") # ID of the grouped report
EVENTS_TABLE_ID = os.getenv("EVENTS_TABLE_ID")

def formatter(type, variable):
    if type == 'date':
        variable = variable.split()
        variable = variable[0]
        if "/" in variable:
            parts = variable.split("/")
            variable = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
    if type == 'numeric':
        variable
        if(variable != "--"):
            variable = float(variable)
    if type == 'currency':
        if(variable != "--"):
            variable = float(variable)
        
    return variable



def get_events():
     headers = {
        'Content-Type': 'application/json',
        'QB-Realm-Hostname': f'{REALM}',
        'Authorization': f'QB-USER-TOKEN {TOKEN}'
    }
    
     body = {
        "tableId": f"{EVENTS_TABLE_ID}"
    }
     url = f"https://api.quickbase.com/v1/reports/{REPORT_ID}/run?tableId={EVENTS_TABLE_ID}"
     
     response = requests.post(url, headers=headers)

     if response.status_code == 200:
        data = response.json()
       
            
        return data
     else: 
        print(f"Error: {response.status_code} - {response.text}")

data = get_events()

codes = []
code_to_record_id = {}
duplicates = []
for row in data.get("data", []):
    code = row["80"]["value"].upper().strip()
    record_id = row["3"]["value"]
    codes.append(code)
    if code_to_record_id.get(code) is None:
        code_to_record_id[code] = record_id
    else:
        duplicates.append(code)

def get_fields():
    
    headers = {
        'Content-Type': 'application/json',
        'QB-Realm-Hostname': f'{REALM}',
        'User-Agent': '{User-Agent}',
        'Authorization': f'QB-USER-TOKEN {TOKEN}'
    }
    includeFieldPerms = True
    params = {
        'tableId': f'{TABLE_ID}',
        'includeFieldPerms': "true"
    }
    r = requests.get(
    'https://api.quickbase.com/v1/fields', 
    params = params, 
    headers = headers
    )

    fields = r.json()
    return fields

fields = get_fields()
columns_to_ids = {}
id_to_column = {}
field_type = {}
columns = []
for f in fields:
    columns_to_ids[f["label"]] = f["id"]
    id_to_column[f["id"]] = f["label"]
    field_type[f["id"]] = f["fieldType"]
    columns.append(f["label"])

data = {
        "to": TABLE_ID,
        "mergeFieldId": 3,
        "data": [
            {
            }
        ]
    }

def add_project_code(df):
    project_code_id = columns_to_ids["Project Code"]
    
    for idx, row in df.iterrows():
        value = row["Expense Code (Uber Original)"]
        if code_to_record_id.get(value) is not None:
            df.at[idx, "Project Code"] = str(value)
            df.at[idx, "Related Events"] = code_to_record_id.get(value)
            df.at[idx, "Related Expense"] = 27
        else:
            print(f"Row {idx}: ⚠️ Warning: Project Code not found — {value}")
    return df



def dynamic_post_request(csv_file, row_num):
    
    url = f"https://api.quickbase.com/v1/records"

    headers = {
        "QB-Realm-Hostname": f"{REALM}.quickbase.com",
        "User-Agent": "QuickbasePythonClient",
        "Authorization": f"QB-USER-TOKEN {TOKEN}",
        "Content-Type": "application/json"
    }
    df = pd.read_csv(csv_file)
    print("csv file received")

    for col in columns:
        if col not in df.columns:
            print(f"⚠️ Warning: Column not found — {col}")
            continue
        else:
            value = df.iloc[row_num, df.columns.get_loc(col)]
            id = columns_to_ids.get(col)
            fieldType = field_type.get(id)
            if fieldType == "date":
                value = formatter('date', value).strip()
            if fieldType == "numeric":
                value = formatter('numeric', value)
            if fieldType == "currency":
                value = formatter("currency", value)
 
            if str(value).strip() != '--':
                if isinstance(value, (np.generic, np.ndarray)):
                    value = value.item()
                if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
                    value = None
                data["data"][0][str(id)] = {"value": str(value)}
    
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.text)


def clean_csv(file_path):
    
    print(f"file path; {file_path}")
    if 'keep' not in file_path:
        
        df = pd.read_csv(file_path, skiprows=5)
        df.reset_index(drop=True, inplace=True)
        df.insert(loc=1, column='Trip/Eats ID (Unique)', value="None")
        df["Project Code"] = " "
        df["Project Code"] = df["Project Code"].astype(str)
        df["Related Events"] = 0
        df["Related Expense"] = 0
        df["Related Staff"] = df["Employee ID"]
        df["Expense Code (Uber Original)"] = df["Expense Code"]
        df = df.drop(columns=['Expense Code'])
        df['Expense Code'] = " "

        if 'Transaction Amount (Local Currency)' in df.columns:
            df['Trip/Eats ID (Unique)'] = df['Trip/Eats ID'] + "-" + df['Transaction Amount (Local Currency)'].astype(str)
        elif 'Transaction Amount in Local Currency (incl. Taxes)' in df.columns:
            df.rename(columns={'Transaction Amount in Local Currency (incl. Taxes)': 'Transaction Amount (Local Currency)'}, inplace = True)
            df['Trip/Eats ID (Unique)'] = df['Trip/Eats ID'] + "-" + df['Transaction Amount (Local Currency)'].astype(str)
        else:
            print("Unkown column")
        df = add_project_code(df)

        return df
    else:
        return ''

def get_downloaded_files():
    directory_path = 'from_uber_downloads'  
    all_entries = os.listdir(directory_path)
    files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]

    for file_name in files:
        print(file_name)
    return files
    

def main():
    paramiko_downloader.download_files()
    files = get_downloaded_files()
    csv_file = ''
    dir ='from_uber_downloads'
    for file in files:
        if file.lower().endswith('.csv'):
            csv_file = os.path.join(dir, file)
        
            if csv_file:
                df = clean_csv(csv_file)
                file_name = os.path.basename(csv_file)
                df.to_csv(f"csv_downloads/{file_name}", index=False)
                print("Downloaded")

                for row_num, row in df.iterrows():
                    dynamic_post_request(f"csv_downloads/{file_name}", row_num)
                os.remove(csv_file)
                pass
        else:
                pass

main()

