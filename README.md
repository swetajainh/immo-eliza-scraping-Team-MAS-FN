![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/f3564c1b-8544-4016-b989-b3c912bc9fdd)

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/bd3f0bf0-304f-45ff-904b-6ddfde72864e)

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/a2accc53-360f-4f22-8492-c2ec2a818a6d)






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


![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/17d172df-1cb5-442e-bd41-a32070b55d8f)

 
 **scraper**

   |__scraper.py

   |__main.py

 **Data**

   |__full_list.csv

   |__house_apart_sale.csv

 .gitignore
  requirements.txt

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/d849e299-92be-413a-b1a7-505b7880554a)

 1. Clone the repository to your local machine.
 2.  To run the script, you can execute the main.py file from your command line: 
 3. The scraper file scraps each url page and gathers information about at least 10000 properties all over Belgium over various parameters 

 ```python
 def scrape_urls(page_num)
 def thread_scraping()
 def counter()
 def create_dataframe()
```
![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/36a5259e-68bc-4416-ad55-64b8eaeb08fd)

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/7fe7c46d-7406-4d8d-83f0-5fe786f5f73c)

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/a8e72b43-abae-4006-a425-18d57a19830a)

Team members are Afaf, Miguel Bueno, Nasrin, Shweta Jain and each one of them contributed equally.

![image](https://github.com/swetajainh/immo-eliza-scraping-Team-MAS-FN/assets/158171729/bd9dd628-48f5-4247-8890-5a32c2bf00f9)

we had one week to complete the task.





