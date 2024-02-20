import requests
from bs4 import BeautifulSoup
import threading
import time

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
    full_list_url = []
    num_pages = 333

    # Create a list to store threads
    threads = []
    start_time = time.time()  # Start timer
    
    # Create and start threads
    for i in range(1, num_pages + 1):
        t = threading.Thread(target=lambda: full_list_url.extend(scrape_urls(i)))
        threads.append(t)
        t.start()

    # Wait for all threads to complete and then join
    for t in threads:
        t.join()

    end_time = time.time()  # Stop timer
    execution_time = end_time - start_time

    print("Scraping completed!")
    print("Total URLs scraped:", len(full_list_url))
    print("Total time:", execution_time, "seconds")


thread_scraping()