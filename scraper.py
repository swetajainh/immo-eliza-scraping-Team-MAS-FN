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

"""Scrapes URLs from Immoweb search results for a given page number.
    Args:
        page_num (int): The page number to scrape.
    Returns:
        list: A list of URLs scraped from the page.
"""
# Function to scrape URLs
def scrape_urls(page_num):
    base_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page_num}&orderBy=relevance"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    urls = []
    for elem in soup.find_all("a", attrs={"class": "card__title-link"}):
        urls.append(elem.get('href'))
        
    # Save URLs to file - full_list.txt (local storage)
    with open("full_list.txt", "a") as f:
        for url in urls:
            f.write(url + '\n')
    return urls


def thread_scraping():
    """Performs multithreaded scraping of URLs from Immoweb."""
    full_list_url = []
    num_pages = 333

    # Create a list to store threads
    threads = []
    start_time = time.time()  # Start timer
    
    # Create and start threads
    for i in range(1, num_pages + 1):
        #Creates a new thread (t) with a target function. 
        t = threading.Thread(target=lambda: full_list_url.extend(scrape_urls(i)))
        threads.append(t)
        #This starts the thread t, which executes the target function asynchronously. 
        t.start()

    # Wait for all threads to complete and then join
    for t in threads:
        t.join()

    # Stop timer
    end_time = time.time()  
    execution_time = end_time - start_time

    print("Scraping completed!")
    print("Total URLs scraped:", len(full_list_url))
    print("Total time:", execution_time, "seconds")
    return full_list_url

thread_scraping()


# Function to report the progress of the scrapping process 
def reporting(str, i): 
    """Reports on scraping progress"""
    sys.stdout.write(str + ' %d\r' %i)
    sys.stdout.flush()
    return

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


def counter():
    """Creates a global counter for use in list comprehension"""
    global counters 
    if counters < 1: 
        counters = 1
    else:
        counters +=1
    return


"""Scrapes information from a house listing URL.
    Args:
        url (str): The URL of the house listing.
    Returns:
        dict: A dictionary containing information about the house.
"""
def scrape_house(url):
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
        final_dictionary['url'] = 'Nan'
    #id
    try: 
        final_dictionary['id'] = script['id']
    except: 
        final_dictionary['id'] = 'Nan'
    # Region
    try:
        final_dictionary['region'] = script['property']['location']['region']
    except:
        final_dictionary['region'] = 'Nan'
    # Province
    try:
        final_dictionary['province'] = script['property']['location']['province']
    except:
        final_dictionary['province'] = 'Nan'
    # Locality
    try:
        final_dictionary['locality'] = script['property']['location']['locality']
    except:
        final_dictionary['locality'] = 'Nan'
    # ZIP Code
    try:
        final_dictionary['zip_code'] = script['property']['location']['postalCode']
    except:
        final_dictionary['zip_code'] = 'Nan'
         # Longitude
    try:
        final_dictionary['Longitude'] = script['property']['location']['longitude']
    except:
        final_dictionary['Longitude'] = 'Nan'
    # Latitude
    try:
        final_dictionary['Latitude'] = script['property']['location']['latitude']
    except:
        final_dictionary['Latitude'] = 'Nan'
    # Type of property
    try:
        final_dictionary['property_type'] = script['property']['type']
    except:
        final_dictionary['property_type'] = 'Nan'
    # Subtype of property
    try:
        final_dictionary['property_subtype'] = script['property']['subtype']
    except:
        final_dictionary['property_subtype'] = 'Nan'
    # Price
    try:
        final_dictionary['price'] = script['price']['mainValue']
    except:
        final_dictionary['price'] = 'Nan'
    # Number of rooms
    try:
        final_dictionary['number_rooms'] = script['property']['bedroomCount']
    except:
        final_dictionary['number_rooms'] = 'Nan'
    # Living area
    try:
        final_dictionary['living_area'] = script['property']['netHabitableSurface']
    except:
        final_dictionary['living_area'] = 'Nan'
    # Fully equipped kitchen (Yes/No)
    try:
        final_dictionary['kitchen'] = script['property']['kitchen']['type']
    except:
        final_dictionary['kitchen'] = 0
    # Furnished (Yes/No)
    try:
        final_dictionary['furnished'] = script['transaction']['sale']['isFurnished']
    except:
        final_dictionary['furnished'] = 'Nan'
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
        final_dictionary['surface_land'] = "Nan"
    # Number of facades
    try:
        final_dictionary['number_facades'] = script['property']['building']['facadeCount']
    except:
        final_dictionary['number_facades'] = "Nan"
    # Swimming pool (Yes/No)
    try:
        final_dictionary['swimming_pool'] =  script['property']['hasSwimmingPool']
    except:
        final_dictionary['swimming_pool'] = 0
    # State of the building (New, to be renovated, ...)
    try:
        final_dictionary['building_state'] = script['property']['building']['condition']
    except:
        final_dictionary['building_state'] = 'Nan'
    # Energy
    ##Heating Type
    try: 
        final_dictionary['energy_type'] = script["property"]["energy"]["heatingType"]
    except: 
        final_dictionary['energy_type'] = "Nan"
    ##EPC score 
    try: 
        final_dictionary['EPC_score'] = script["transaction"]["certificates"]["epcScore"]
    except: 
        final_dictionary['EPC_score'] = "Nan"
    ##EnergyConsumptionPerSqm
    try: 
        final_dictionary['EnergyConsumptionPerSqm'] = script["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
    except: 
        final_dictionary['EnergyConsumptionPerSqm'] = "Nan"
    #Parking
    try: 
        final_dictionary['parking_outdoor'] = script["property"]["parkingCountOutdoor"]
    except: 
        final_dictionary['parking_outdoor'] = "Nan"
    try: 
        final_dictionary['parking_indoor'] = script["property"]["parkingCountIndoor"]
    except: 
        final_dictionary['parking_indoor'] = "Nan"

    return final_dictionary
   

def create_dataframe():
    """Scrapes house information and creates a pandas DataFrame."""
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
output_folder = (cwd / 'data_output').resolve() # Adjusted CSV file path and name
csv_filename = "RawData_house_sale.csv"
csv_path = (output_folder / csv_filename).resolve()
url_path = './full_list.txt'
csv_path = (cwd / csv_path).resolve()
url_path = (cwd / url_path).resolve()

# Ensure the "output" folder exists
output_folder = (cwd / 'data_output').resolve()
output_folder.mkdir(parents=True, exist_ok=True)

# Get the raw data
dataset = create_dataframe()
print("Original DataFrame:")
print(dataset)


