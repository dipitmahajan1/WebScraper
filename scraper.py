# Import the library Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim


class Scraper:

    location_data = {}


    def __init__(self) :

        self.PATH = '/Users/dipitmahajan/digital-twin-dashboard-main/chromedriver'

        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #self.driver = webdriver.Chrome(self.PATH, options=self.options)


        self.location_data["Price"] = "NA"
        self.location_data["Description"] = "N/A"
        self.location_data["Address"] = "N/A"
        self.location_data["Title"] = "N/A"
        self.location_data["Latitude"]  = "N/A"
        self.location_data["Longitude"] = "N/A"


    def get_location_information(self) :

        Price = []
        Address = []

        try:

            price = self.driver.find_elements(by=By.CLASS_NAME, value="propertyCard-priceValue")
                                                                                                        #power = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Power"]')
                                                                                                        # for price in Price :
                                                                                                        #     print(price.text)

           

            address = self.driver.find_elements(By.TAG_NAME, "address")
           
            # Title = self.driver.find_element(by=By.CLASS_NAME, value="expPropCardDescription")

            # Description = self.driver.find_element(by=By.CLASS_NAME, value="text")

            for amount,add in zip(price,address) :
                Price.append(amount.text)
                Address.append(add.text)

            column = {'Price':Price, 'Location' :Address}
            properties = pd.DataFrame(column) 

            print(properties)


            geolocator = Nominatim(user_agent='New_application')

            for index,row in properties.iterrows():

                location = geolocator.geocode(row['Location'])

                if location == None :

                    properties.loc[index,'Latitude'] = 'N/A'
                    properties.loc[index,'Longitude'] = 'N/A'

                else:

                    lat,lng = location.latitude , location.longitude
                    properties.loc[index,'Latitude'] = lat
                    properties.loc[index,'Longitude'] = lng


            print(properties)

        except:

            pass

        # try :

        #     for amount,add in zip(price,address) :
        #         Price.append(amount.text)
        #         Address.append(add.text)

        #     column = {'Price':Price, 'Location' :Address}
        #     properties = pd.DataFrame(column) 

        #     print(properties)
        #     geolocator = Nominatim(user_agent='New_application')

        #     for index,row in properties.iterrows():

        #         location = geolocator.geocode(row['Location'])

        #         if location == None :

        #             properties.loc[index,'Latitude'] = 'N/A'
        #             properties.loc[index,'Longitude'] = 'N/A'

        #         else:

        #             lat,lng = location.latitude , location.longitude
        #             properties.loc[index,'Latitude'] = lat
        #             properties.loc[index,'Longitude'] = lng


        #     print(properties)

        #     # self.location_data["Description"] = Description.text
        #     # self.location_data["Address"] = Address.text
        #     # self.location_data["Title"] = Title.text

        # except :

        #     pass

        

        

    # def get_coordinates(properties):

    #     try:

    #         geolocator = Nominatim(user_agent='New_application')

    #         for index,row in properties.iterrows():

    #             location = geolocator.geocode(row['Location'],timeout= 10)

    #             if location == None :

    #                 properties.loc[index,'Latitude'] = 'N/A'
    #                 properties.loc[index,'Longitude'] = 'N/A'

    #             else:

    #                 lat,lng = location.latitude , location.longitude
    #                 properties.loc[index,'Latitude'] = lat
    #                 properties.loc[index,'Longitude'] = lng


    #             print(properties)


    #     except:

    #         return properties


    def scrape(self, url): # Passed the URL as a variable

        try:
            #self.driver.get(url) # Get is a method that will tell the driver to open at that particular URL
            self.driver.execute("get", {'url': url})
            

        except Exception as e:
            self.driver.quit()
            return

        time.sleep(10) # Waiting for the page to load.

        self.get_location_information()

        #self.get_coordinates(self.properties)


        self.driver.quit()


        return (self.location_data)
    

url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E1498&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false"
x = Scraper()
print(x.scrape(url))
    



    









