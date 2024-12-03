import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

url = 'https://www.tomshardware.com/news/gpus-historical-ebay-pricing'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

os.mkdir(soup.title.string)
os.chdir(soup.title.string)

tables = soup.find_all('table')

for i, table in enumerate(tables):
    df = pd.read_html(str(table))[0]
    
    csv_filename = f'table_{i}.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Saved table {i} to {csv_filename}")
