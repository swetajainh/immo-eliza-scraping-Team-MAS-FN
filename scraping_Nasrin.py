import requests
from bs4 import BeautifulSoup 
import re
import json
import time
import threading
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

# Function to scrape URLs
def scrape_urls(page_num):
    base_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page_num}&orderBy=relevance"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    urls = []
    for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
        urls.append(elem.get('href'))
        
    # Save URLs to file - full_list.txt (local storage)
    with open("full_list.txt", "w") as f:
        for url in urls:
            f.write(url + '\n')
    return urls


def thread_scraping():
    full_list_url = []
    num_pages = 1

    # Create a list to store threads
    threads = []
    start_time = time.time()  # Start timer
    
    # Create and start threads
    for i in range(1, num_pages + 1):
        #This line creates a new thread (t) with a target function. 
        #The target function is a lambda function that calls scrape_urls(i) for the current value of i.
        t = threading.Thread(target=lambda: full_list_url.extend(scrape_urls(i)))
        #The newly created thread t is appended to the list threads, 
        # which keeps track of all the threads created.
        threads.append(t)
        #This starts the thread t, which executes the target function asynchronously. 
        t.start()

    # Wait for all threads to complete and then join
    for t in threads:
        t.join()

    end_time = time.time()  # Stop timer
    execution_time = end_time - start_time

    print("Scraping completed!")
    print("Total URLs scraped:", len(full_list_url))
    print("Total time:", execution_time, "seconds")
    return full_list_url

thread_scraping()

# Reading URLs from the file
with open("./full_list.txt", "r") as file:
    original_urls = file.readlines()

# Removing duplicates
unique_urls = list(set(original_urls))

# Check if duplicates exist
if len(original_urls) != len(unique_urls):
    print("Duplicates found!")
else:
    print("No duplicates found.")


# Function to report the progress of the scrapping process 
def reporting(str, i): 
    """Reports on scraping progress"""
    sys.stdout.write(str + ' %d\r' %i)
    sys.stdout.flush()
    return

def counter():
    """Creates a global counter for use in list comprehension"""
    global counters 
    if counters < 1: 
        counters = 1
    else:
        counters +=1
    return

def scrape_house(url):
    """Scrapes all the info from a house listing"""

    # Get the house listing and make a soup
    try:
        house_page = requests.get(url)
        house_page = BeautifulSoup(house_page.text, 'html.parser')
    # Return an empty dictionary if we can't parse the URL
    except: 
        return {}

    # Get the hidden info from the java script
    try:
        #To extract the JSON-like data, the function uses a regular expression
        # (regex = r"window.classified = (\{.*\})") to capture the JSON-like data enclosed within curly braces {}.
        regex = r"window.classified = (\{.*\})" # Only captures what's between brackets
        script = house_page.find('div',attrs={"id":"main-container"}).script.text
        script = re.findall(regex, script)
        script = json.loads(script[0])
    except:
        return {}

    final_dictionary = {}
    
    
    # URL
    try:
        final_dictionary['url'] = url
    except:
        final_dictionary['url'] = 'UNKNOWN'
    #id
    try: 
        final_dictionary['id'] = script['id']
    except: 
        final_dictionary['id'] = 'UNKNOWN'
    # Region
    try:
        final_dictionary['region'] = script['property']['location']['region']
    except:
        final_dictionary['region'] = 'UNKNOWN'
    # Province
    try:
        final_dictionary['province'] = script['property']['location']['province']
    except:
        final_dictionary['province'] = 'UNKNOWN'
    # Locality
    try:
        final_dictionary['locality'] = script['property']['location']['locality']
    except:
        final_dictionary['locality'] = 'UNKNOWN'
    # ZIP Code
    try:
        final_dictionary['zip_code'] = script['property']['location']['postalCode']
    except:
        final_dictionary['zip_code'] = 'UNKNOWN'
    # Type of property
    try:
        final_dictionary['property_type'] = script['property']['type']
    except:
        final_dictionary['property_type'] = 'UNKNOWN'
    # Subtype of property
    try:
        final_dictionary['property_subtype'] = script['property']['subtype']
    except:
        final_dictionary['property_subtype'] = 'UNKNOWN'
    # Price
    try:
        final_dictionary['price'] = script['price']['mainValue']
    except:
        final_dictionary['price'] = 'UNKNOWN'
    # Number of rooms
    try:
        final_dictionary['number_rooms'] = script['property']['bedroomCount']
    except:
        final_dictionary['number_rooms'] = 'UNKNOWN'
    # Living area
    try:
        final_dictionary['living_area'] = script['property']['netHabitableSurface']
    except:
        final_dictionary['living_area'] = 'UNKNOWN'
    # Fully equipped kitchen (Yes/No)
    try:
        final_dictionary['kitchen'] = script['property']['kitchen']['type']
    except:
        final_dictionary['kitchen'] = 0
    # Furnished (Yes/No)
    try:
        final_dictionary['furnished'] = script['transaction']['sale']['isFurnished']
    except:
        final_dictionary['furnished'] = 'UNKNOWN'
    # Open fire (Yes/No)
    try:
        final_dictionary['fireplace'] = script['property']['fireplaceCount']
    except:
        final_dictionary['fireplace'] = 0
    # Terrace (Yes/No)
    try:
        final_dictionary['terrace'] = script['property']['hasTerrace']
    except:
        final_dictionary['terrace'] = 0
    # If yes: Area
    try:
        final_dictionary['terrace_area'] = script['property']['terraceSurface']
    except: 
        final_dictionary['terrace_area'] = 0
    # Garden
    try:
        final_dictionary['garden'] = script['property']['hasGarden']
    except:
        final_dictionary['garden'] = 0
    # If yes: Area
    try:
        final_dictionary['garden_area'] = script['property']['gardenSurface']
    except:
        final_dictionary['garden_area'] = 0
    # Surface of the land 
    try: 
        final_dictionary['surface_land'] = script['property']['land']['surface']
    except:
        final_dictionary['surface_land'] = "UNKNOWN"
    # Number of facades
    try:
        final_dictionary['number_facades'] = script['property']['building']['facadeCount']
    except:
        final_dictionary['number_facades'] = "UNKNOWN"
    # Swimming pool (Yes/No)
    try:
        final_dictionary['swimming_pool'] =  script['property']['hasSwimmingPool']
    except:
        final_dictionary['swimming_pool'] = 0
    # State of the building (New, to be renovated, ...)
    try:
        final_dictionary['building_state'] = script['property']['building']['condition']
    except:
        final_dictionary['building_state'] = 'UNKNOWN'


    return final_dictionary
   

def create_dataframe():
    """Will scrape info from house pages and create a pandas DataFrame from the info we scrape"""
    # Initialize list and fetch all URLs
    houses_links = []
    houses_links = thread_scraping()
    
    print("")
    print("Scraping individual pages...")
    start_time = time.time()  # Start timer

    # Scrape info from house pages concurrently
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [(executor.submit(scrape_house, url), counter(), reporting("Individual pages scraped:", counters), 
                    time.sleep(.2)) for url in houses_links]
        results =  [item[0].result() for item in futures]
        df = pd.DataFrame(results)
    
    # Export our dataset to a csv"
    df.to_csv(csv_path, index = True)
    #df.to_excel(excel_path, index=True)


    end_time = time.time()  # Stop timer
    execution_time = end_time - start_time

    print("Scraping completed!")
    print("Total time spent scraping:", execution_time, "seconds")
    return df

# Initialize counter for the counter function
counters = 1

# Build path to file
# Selects current working directory
cwd = Path.cwd()
csv_path = r'.\data_output'
url_path = r'.\full_list.txt'
csv_path = (cwd / csv_path).resolve()
url_path = (cwd / url_path).resolve()

dataset = create_dataframe()
print(dataset)

column_names = dataset.columns
print(column_names)



