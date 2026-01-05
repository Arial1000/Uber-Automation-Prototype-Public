"""
Dowloads receipts from Uber using sftp protocol.
"""

import paramiko
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
def download_files():
    load_dotenv()
    port = os.getenv("PORT")
    hostname = os.getenv("HOST_NAME")
    username = os.getenv("UN")
    ssh_key_path = os.getenv("SSH_KEY")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname = hostname, port= port, username = username, key_filename= ssh_key_path)

        sftp = ssh_client.open_sftp()
        print(f"Connected to {hostname} as {username}.")
    except Exception as err:
        raise Exception(err)


    dir = '/from_uber/trips'
    sftp.chdir(dir)
    files = sftp.listdir(dir)
    print("Files: ")

    today = datetime.today()
    past_week_dates = [(today - timedelta(days=i)).strftime("%Y_%m_%d") for i in range(7)]
    print("Past week dates: ")
    print(past_week_dates)

    downloaded_files = []
    local_dir = "from_uber_downloads"
    for date_str in past_week_dates:
            filename = f"daily_trips-{date_str}.csv"
            if filename in files:
                local_path = os.path.join(local_dir, filename)
                sftp.get(filename, local_path)
                print(f"Downloaded: {filename}")
                downloaded_files.append(local_path)
            else:
                print(f"File not found for {date_str}: {filename}")

    sftp.close()
    ssh_client.close()
