"""
Downloads example CSV files using SFTP (simulated for demo purposes).
"""

import os
import random
import pandas as pd

def download_files():

    local_dir = "downloads"
    os.makedirs(local_dir, exist_ok=True)

    # Simulate 3 CSV files
    for i in range(1, 4):
        filename = f"sample_data_{i}.csv"
        local_path = os.path.join(local_dir, filename)

        # Generate fake data
        df = pd.DataFrame({
            "Category": ["Food", "Travel", "Supplies"],
            "Amount": [round(random.uniform(5, 100), 2) for _ in range(3)],
            "Date": pd.date_range("2026-01-20", periods=3)
        })
        df.to_csv(local_path, index=False)
        print(f"Created simulated file: {local_path}")
    
    return [os.path.join(local_dir, f) for f in os.listdir(local_dir) if f.endswith(".csv")]
