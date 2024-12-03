import pandas as pd
import os
from glob import glob
import re

base_dir = './data'

time_series_data = []

for folder in sorted(glob(os.path.join(base_dir, '*'))):
    if not os.path.isdir(folder):
        continue

    # Match date of folder
    folder_name = os.path.basename(folder)
    match = re.search(r'([A-Za-z]+)_+(\d{4})', folder_name)
    if not match:
        print(f"Skipping folder: {folder_name} (no valid date found)")
        continue

    month, year = match.groups()
    timestamp = f"{month} {year}"

    # Process both table_0.csv and table_1.csv
    for table_name in ['table_0.csv', 'table_1.csv']:
        csv_path = os.path.join(folder, table_name)
        if not os.path.exists(csv_path):
            print(f"Skipping folder: {folder_name} (no {table_name} found)")
            continue

        df = pd.read_csv(csv_path)

        # Identify the leftmost "eBay Price" column dynamically
        ebay_price_col = next((col for col in df.columns if "eBay Price" in col), None)
        if not ebay_price_col:
            print(f"Skipping folder: {folder_name} (no eBay Price column found in {table_name})")
            continue

        # Rename columns for consistency
        column_mapping = {
            "GPU": "GPU",
            ebay_price_col: "eBay Price",
            "QTY Sold": "QTY Sold"
        }
        df = df.rename(columns=column_mapping)

        # Only need these from original
        df = df[["GPU", "eBay Price", "QTY Sold"]]

        # Add a "Month" column
        df["Month"] = timestamp

        time_series_data.append(df)

# Combine all the data frames into one final data frame
final_df = pd.concat(time_series_data, ignore_index=True)

# Save the final data frame to a CSV file
final_df.to_csv('gpu_time_series.csv', index=False)
print("Time series data saved as gpu_time_series.csv")

