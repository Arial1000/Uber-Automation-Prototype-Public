"""
Processes CSV files and uploads normalized records to a mock API.
"""

import pandas as pd
import numpy as np
import requests
from file_downloader import download_files

def formatter(type, value):
    if type == "date":
        value = str(value).split()[0]
    elif type in ["numeric", "currency"]:
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = None
    return value

def add_mapping(df, mapping):
    """
    Example of mapping categories to codes.
    """
    df["Mapped Code"] = df["Category"].map(mapping).fillna("UNKNOWN")
    return df

def post_to_api(row, endpoint="https://mockapi.io/projects/demo"):
    """
    Simulate sending each row to a public/mock API.
    """
    data = row.to_dict()
    response = requests.post(endpoint, json=data)
    print(f"Posted row {row.name} | Status: {response.status_code}")
    return response.status_code

def clean_csv(file_path, mapping):
    df = pd.read_csv(file_path)
    df = add_mapping(df, mapping)

    # Apply formatting
    for col in ["Amount", "Date"]:
        df[col] = df[col].apply(lambda x: formatter("numeric" if col=="Amount" else "date", x))
    
    return df

def main():
    # Simulate download
    files = download_files()

    # Example mapping
    category_mapping = {
        "Food": "F001",
        "Travel": "T001",
        "Supplies": "S001"
    }

    for file in files:
        df = clean_csv(file, category_mapping)
        print(f"Processing {file}:\n", df, "\n")
        
        for idx, row in df.iterrows():
            post_to_api(row)

if __name__ == "__main__":
    main()
