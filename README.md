# CSV Processing & API Upload Demo

This project demonstrates a complete workflow for **processing CSV files** and **posting data to an API**. It’s designed as a **portfolio project** to showcase Python skills in file handling, data cleaning, and API interaction. All data and endpoints are simulated for demonstration purposes.

---

## Features

- **File download simulation**  
  Creates sample CSV files locally to mimic downloading data from an external source.

- **CSV processing & cleaning**  
  - Normalizes column names and data formats  
  - Maps categories to standardized codes  
  - Handles numeric and date formatting with error checking

- **API interaction**  
  Posts processed records to a mock API endpoint (`https://mockapi.io`) to simulate sending data to an external system.

- **Modular code structure**  
  - `file_downloader.py`: simulates file downloads  
  - `process_csv.py`: main workflow for processing CSVs and posting data

---

## Usage
### Running the Program
In the root folder run:  
`python -u process.py`  

## Managing Dependencies
1. Install dependencies only as needed to keep requirements.txt clean
2. Update requirements.txt after installing a package
   pip freeze > requirements.txt
3. Commit requirements.txt





