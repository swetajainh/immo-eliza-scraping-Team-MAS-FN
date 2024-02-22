import requests
from bs4 import BeautifulSoup
import re
import json
import time
import threading
from collections import defaultdict
import pandas as pd
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor, as_completed
from pathlib import Path
import sys
from scraper import scrape_urls
from scraper import thread_scraping
from scraper import scrape_house
from scraper import counter
from scraper import create_dataframe
from scraper import reporting
import csv

# Initialize counter for the counter function
counters = 1

def main():
    # Select current working directory
    cwd = Path.cwd()

    # Define file paths
    csv_path = cwd / 'house_apart_sale' 
    url_path = cwd / 'full_list.txt'

    # Create DataFrame from scraped data
    dataset = create_dataframe()

    # Write DataFrame to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dataset.columns)
        writer.writeheader()
        for index, row in dataset.iterrows():
            writer.writerow(row.to_dict())

    # Read CSV back into DataFrame
    df = pd.read_csv(csv_path)
    print(df.head())

# Call the main function
main()
