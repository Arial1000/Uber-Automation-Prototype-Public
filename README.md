# Uber Automation Prototype
This is an application designed to allow Markham eployees to automatically clean Uber CSV formatted receipts and insert/udpate the Uber Rides table in Quickbase with the new records.
## Installation
### Clone Environment
Open command line:  
`git clone https://github.com/Arial1000/Uber_Automation_Prototype.git`  
`cd <your-repo-folder>`

### Create Virtual Environment
Opent terminal in VS Code:  
`python -m venv venv`  
`venv\Scripts\activate`  
`pip install -r requirements.txt`

### Set up Credentials
1. Create a directory called .env in the root directory of the project.
2. Add the following credentials to your .env file:
   - QB_TOKEN
   - REALM
   - TABLE_ID
   - APP_TOKEN

## Usage
### Running the Program
In the root folder run:  
`python -u upload.py`  
## Managing Dependencies
1. Install dependencies only as needed to keep requirements.txt clean
2. Update requirements.txt after installing a package
   pip freeze > requirements.txt
3. Commit requirements.txt





