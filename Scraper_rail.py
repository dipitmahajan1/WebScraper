# Import the library Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim


class Scraper:

    location_data = {}


    def __init__(self) :

        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



    def get_location_information(self,df3) :

        try:
            df = df3.head(5)
            df['Location'] = ''
            df['Info'] = ''
            for index, row in df.iterrows():
                #print(df['Wikidata'].iloc[0])
                link= self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=row['Wikidata'])
                time.sleep(1)

                link.click()


                time.sleep(1)

                window_after = self.driver.window_handles[1]
                self.driver.switch_to.window(window_after)

                location = self.driver.find_element(by=By.CLASS_NAME, value="wikibase-kartographer-caption")
                #print(location.text)
                df.iloc[index]['Location'] = location.text
                #print(df)

                self.driver.close()
                window_before = self.driver.window_handles[0]
                self.driver.switch_to.window(window_before)


                time.sleep(1)

                link= self.driver.find_element(by=By.LINK_TEXT, value=row['Name'])

                time.sleep(1)

                link.click()


                time.sleep(1)

                try:
                    data = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table"))).get_attribute("outerHTML")
                    df1  = pd.read_html(data)
                    #print(df1[0].to_dict('records'))
                    df.iloc[index]['Info'] = df1[0].to_dict('records')
                except NoSuchElementException:
                    print("not able to retrieve element")
                    pass
                except Exception as e:
                    print(e)
                    pass

            
                self.driver.execute("get", {'url': "https://openinframap.org/stats/area/United%20Kingdom/plants"})
                

                time.sleep(1)
            
            print(df)



            
        except:

            pass


    def scrape(self, url): # Passed the URL as a variable

        try:
            
            self.driver.execute("get", {'url': url})

            data = self.driver.find_element(by=By.XPATH, value="/html/body/div/p/table[1]")

            # data = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.plants-table"))).get_attribute("outerHTML")
            # df1  = pd.read_html(data)
            # df = df1[0]  #iterating list to get dataframe
            print(data)

        except Exception as e:
            self.driver.quit()
            print(e)
            return 0

        time.sleep(10) # Waiting for the page to load.

        # self.get_location_information(df)


        self.driver.quit()


        # return (self.location_data)
    

url = "https://www.railwaydata.co.uk/linefiles/route/?ELR=CMP2"
x = Scraper()

print(x.scrape(url))
    



    









