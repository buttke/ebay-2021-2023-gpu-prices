import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import time

with open('monthly_links.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

data_root = 'data'
os.makedirs(data_root, exist_ok=True)
os.chdir(data_root)

for url in urls:
    time.sleep(0.2)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    folder_name = soup.title.string.replace(" ", "_").replace("/", "_")
    print(folder_name)
    os.makedirs(folder_name, exist_ok=True)
    os.chdir(folder_name)

    tables = soup.find_all('table')

    for i, table in enumerate(tables):
        df = pd.read_html(str(table))[0]

        csv_filename = f'table_{i}.csv'
        df.to_csv(csv_filename, index=False)
        print(f"Saved table {i} to {csv_filename} in {folder_name}")

    os.chdir('..')
