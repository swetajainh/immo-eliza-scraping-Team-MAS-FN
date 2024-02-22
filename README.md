![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)

The real estate company "Immo Eliza" wants to develop a machine learning model to make price predictions on real estate sales in Belgium.
The final dataset is a csv file with at least the following 18 columns:
- Property ID 
-  Locality name
-  Postal code
-  Price
- Type of property (house or apartment)
- Subtype of property (bungalow, chalet, mansion, ...)
- Type of sale (note: exclude life sales)
- Number of rooms
- Living area (area in m²)
- Equipped kitchen (0/1)
- Furnished (0/1)
- Open fire (0/1)
- Terrace (area in m² or null if no terrace)
- Garden (area in m² or null if no garden)
- Surface of good
- Number of facades
- Swimming pool (0/1)
- State of building (new, to be renovated, ...)


![alt text](image-4.png)
 
 **scraper**

   |__scraper.py

   |__main.py

 **Data**

   |__full_list.csv

   |__house_apart_sale.csv

 .gitignore
  requirements.txt

 ![alt text](image-5.png) 
 1. Clone the repository to your local machine.
 2.  To run the script, you can execute the main.py file from your command line: 
 3. The scraper file scraps each url page and gathers information about at least 10000 properties all over Belgium over various parameters 

 ```python
 def scrape_urls(page_num)
 def thread_scraping()
 def counter()
 def create_dataframe()
```

