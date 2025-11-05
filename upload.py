
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd 
from dotenv import load_dotenv
import requests
import json
import numpy as np

load_dotenv()
REALM = os.getenv("REALM")
TABLE_ID = os.getenv("TABLE_ID")
TOKEN = os.getenv("QB_TOKEN")

def formatter(type, variable):
    if type == 'date':
        variable = variable.split()
        variable = variable[0]
        if "/" in variable:
            parts = variable.split("/")
            variable = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
        return variable
    if type == 'int':
        variable
        if(variable != "--"):
            variable = int(variable)
        return variable

def record_exists(record_id):
    
    url = f"https://api.quickbase.com/v1/records/query"

    headers = {
        "QB-Realm-Hostname": f"{REALM}.quickbase.com",
        "User-Agent": "QuickbasePythonClient",
        "Authorization": f"QB-USER-TOKEN {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "from": TABLE_ID,
        "select": [3],  # the Record ID field
        "where": f"{{3.EX.{record_id}}}"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("Error querying Quickbase:", response.text)
        return False

    result = response.json()
    return len(result.get("data", [])) > 0

    

def create_post_request(csv_file, row_num):
    # Replace with your values
    # or just paste it here for testing
    FIELD_ID = 18  # the field ID of the field you want to change

    url = f"https://api.quickbase.com/v1/records"

    headers = {
        "QB-Realm-Hostname": f"{REALM}.quickbase.com",
        "User-Agent": "QuickbasePythonClient",
        "Authorization": f"QB-USER-TOKEN {TOKEN}",
        "Content-Type": "application/json"
    }

    df = pd.read_csv(csv_file)
    print("csv file received")
    variable_list = []
    columns = [
    'Trip/Eats ID',
    'Trip/Eats ID (Unique)',
    'Transaction Timestamp (UTC)',
    'Request Date (UTC)',
    'Request Time (UTC)',
    'Request Date (Local)',
    'Request Time (Local)',
    'Drop-off Date (UTC)',
    'Drop-off Time (UTC)',
    'Drop-off Date (Local)',
    'Drop-off Time (Local)',
    'Request Timezone Offset from UTC',
    'First Name',
    'Last Name',
    'Email',
    'Employee ID',
    'Group',
    'Service',
    'Program',
    'City',
    'Country',
    'Distance (mi)',
    'Duration (min)',
    'Pickup Address',
    'Drop-off Address',
    'Expense Code',
    'Expense Memo',
    'Payment Method',
    'Transaction Type',
    'Trip/Meal Fare (Local Currency)',
    'Booking Fee/Service Fee (Local Currency)',
    'Airport Fee (Local Currency)',
    'City Fee (Local Currency)',
    'Toll Fee (Local Currency)',
    'Delivery Fee (Local Currency)',
    'Promotions/Discounts (Local Currency)',
    'Tip in Local Currency',
    'Other Charges(Local Currency)',
    'Total Fare (local currency)',
    'Total Taxes (local currency)',
    'Payments made by employees/guests (local currency)',
    'Transaction Amount (Local Currency)',
    'Membership Savings(Local Currency)',
    'Local Currency Code',
    'Tip in USD',
    'Total Fare USD',
    'Total Taxes USD',
    'Payments made by employees/guests (USD currency)',
    'Transaction Amount USD',
    'Network Transaction Id',
    'IsGroupOrder',
    'Fulfilment Type',
    'Cancellation type',
    'Estimated Service and Technology Fee (incl. Taxes, if any) in USD'
    ]
    for col in columns:
        if col not in df.columns:
            print(f"⚠️ Warning: Column not found — {col}")
            continue
        value = df.iloc[row_num, df.columns.get_loc(col)]
        
        # Apply formatting if needed
        if col in ['Transaction Timestamp (UTC)', 
                'Request Date (UTC)', 'Request Date (Local)',
                'Drop-off Date (UTC)', 'Drop-off Date (Local)',
                'Drop-off Time (Local)']:
            value = formatter('date', value).strip()
        elif col == 'Duration (min)':
            value = formatter('int', value)
        
        variable_list.append([value])
    print("Variable list")
    #print(variable_list)
    data = {
        "to": TABLE_ID,
        "data": [
            {
                # "7": {"value": trip_ID_unique},  # field ID 3 is always the record ID field
                # "6": {"value": trip_eats_ID },
                # "8": {"value": transaction_timestamp},
                # # "9": {'value': request_date_UTC},
                # "10": {"value": request_time_UTC},
                # "11": {"value": request_date_local},
                # "12": {"value": request_time_local},
                # "13": {"value": drop_off_date_UTC},
                # "14": {"value": drop_off_time_UTC},
                # "15": {"value": drop_off_date_local},
                # "16": {"value": drop_off_time_local},
                # "17": {"value": request_timezone_offset_from_UTC},
                # "18": {"value": first_name},
                # "19": {"value": last_name},
                # "20": {"value": email},
                # "21": {"value": employee_id},
                # "22": {"value": group},
                # "23": {"value": service},
                # "24": {"value": program},
                # "25": {"value": city},
                # "26": {"value": country},
                # "27": {"value": distance},
                # "28": {"value": duration},
                # "29": {"value": pickup_address},
                # "30": {"value": drop_off_address},
                # "31": {"value": expense_code},
                # "32": {"value": expense_memo},
                # "33": {"value": payment_memo},
                # "34": {"value": transaction_type},
                # "35": {"value": trip_meal_fare_local},
                # "36": {"value": booking_and_service_fee_local},
                # "37": {"value": airport_fee_local},
                # "38": {"value": city_fee_local},
                # "39": {"value": toll_fee_local},
                # "40": {"value": delivery_fee_local},
                # "41": {"value": promotions_dicounts_local},
                # "42": {"value": tip_in_local_currency},
                # "43": {"value": other_charges_local},
                # "44": {"value": total_fare_local},
                # "45": {"value": total_taxes_local},
                # "46": {"value": payments_made_by_employees_and_guests_local},
                # "47": {"value": transaction_amount_local},
                # "48": {"value": membership_savings_local},
                # "49": {"value": local_currency_code},
                # "50": {"value": tip_in_USD},
                # "51": {"value": total_fare_USD},
                # "52": {"value": total_taxes_USD},
                # "53": {"value": payments_made_by_employees_and_guests_USD},
                # "54": {"value": transaction_amount_USD},
                # "55": {"value": network_transaction_id},
                # "56": {"value": isGroupOrder},
                # "57": {"value": fulfilment_type},
                # "58": {"value": cancellation_type},
                # "59": {"value": estimated_service_and_technoloy_fee_incl_taxes_USD}
            }
        ]
    }
    for index, sublist in enumerate(variable_list):
        value = sublist[0]
        if str(value).strip() != '--':
            if isinstance(value, (np.generic, np.ndarray)):
                value = value.item()
            data["data"][0][str(index + 6)] = {"value": value}

    print("data")
    #print(data["data"][0])
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.text)

def update_post_request(record_id):
   # Replace with your values
    # or just paste it here for testing
    RECORD_ID = record_id  # the Record ID you want to update
    FIELD_ID = 17  # the field ID of the field you want to change

    url = f"https://api.quickbase.com/v1/records"

    headers = {
        "QB-Realm-Hostname": f"{REALM}.quickbase.com",
        "User-Agent": "QuickbasePythonClient",
        "Authorization": f"QB-USER-TOKEN {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": TABLE_ID,
        "data": [
            {
                "3": {"value": RECORD_ID},  # field ID 3 is always the record ID field
                str(FIELD_ID): {"value": "name"}
                
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.text)

def get_env_var(name, default=None, required=False):
    """
    Get an environment variable, strip whitespace, and handle missing values.
    
    :param name: Name of the env variable
    :param default: Default value if variable is not set
    :param required: If True, raise error when variable is missing
    :return: The stripped environment variable value
    """
    value = os.getenv(name, default)
    
    if value is not None:
        value = value.strip()  # Remove leading/trailing whitespace
    
    if required and not value:
        raise EnvironmentError(f"Required environment variable '{name}' is missing!")
    
    return value


def clean_csv(file_path):
    # Example: read, do some cleaning, and return cleaned DataFrame
    print(f"file path; {file_path}")
    if 'keep' not in file_path:
        
        df = pd.read_csv(file_path, skiprows=5)
        # Insert your cleaning steps here, e.g., remove empty rows, rename columns
        df.reset_index(drop=True, inplace=True)
        df.insert(loc=1, column='Trip/Eats ID (Unique)', value="None")
        df['Trip/Eats ID (Unique)'] = df['Trip/Eats ID'] + "-" + df['Transaction Amount (Local Currency)'].astype(str)
        # 1. Remove the '--' from string columns
        
        # print(df.columns.tolist())

        return df
    else:
        # print("keep.txt found")
        return ''

def convert_to_json(df):
    json_record = df.to_json(orient='records')
    return json_record

def select_csv():
    root = tk.Tk()
    root.withdraw()  # hide the main window

    while True:
        file_path = filedialog.askopenfilename(
            title="Select the Uber CSV file",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            print("No file selected. Exiting.")
            return None  # user cancelled

        if file_path.lower().endswith(".csv") and os.path.isfile(file_path):
            print("Selected file:", file_path)
            
            return file_path
        else:
            print("That’s not a valid CSV file. Please try again.")

def get_downloaded_files():
    directory_path = 'from_uber_downloads'  # Current directory, or specify a path like '/path/to/directory'
    all_entries = os.listdir(directory_path)
    files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]

    for file_name in files:
        print(file_name)
    return files
    


# Example usage:
def execute_download():
    with open("paramiko_downloader.py", "r") as f:
        code = f.read()
    exec(code)

execute_download()
files = get_downloaded_files()
csv_file = ''
dir ='from_uber_downloads'
for file in files:
    if file.lower().endswith('.csv'):
        csv_file = os.path.join(dir, file)
    
# csv_file = select_csv()
        if csv_file:
        # call your CSV cleaning and Quickbase upload functions here
            df = clean_csv(csv_file)
            #print(df['Trips Unique'].head())
            file_name = os.path.basename(csv_file)
            df.to_csv(f"csv_downloads/{file_name}", index=False)
            print("Downloaded")
            
            json_record = convert_to_json(df)
            if json_record:
                print("Json Records:")
                #print(json_record)
            else:
                print("CSV to JSON conversion failed")
            
            created = record_exists(5270)
            if(False):
                update_post_request(5269)
            
            else:
                for row_num, row in df.iterrows():
                    create_post_request(f"csv_downloads/{file_name}", row_num)
                os.remove(csv_file)
            pass
    else:
            pass

