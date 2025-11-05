import paramiko
from datetime import datetime, timedelta
import os


# Define SFTP connection parameters
port = 2222
hostname = "sftp.uber.com"
username = "a6245ed6"
password = "jasmine7"

# Create an SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SFTP server
try:
    ssh_client.connect(hostname, port, username, password)

# Create an SFTP session
    sftp = ssh_client.open_sftp()
    print(f"Connected to {hostname} as {username}.")
except Exception as err:
    raise Exception(err)

# Now you can perform SFTP operations

#List contents
dir = '/from_uber/trips'
sftp.chdir(dir)
files = sftp.listdir(dir)
print("Files: ")
# print(files)

#Date range
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

#Close connection
sftp.close()
ssh_client.close()