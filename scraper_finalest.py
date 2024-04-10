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

        # self.location_data["Operator"] = "NA"
        # self.location_data["Description"] = "N/A"
        # self.location_data["Address"] = "N/A"
        # self.location_data["Title"] = "N/A"
        # self.location_data["Latitude"]  = "N/A"
        # self.location_data["Longitude"] = "N/A"


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
                df.loc[index,'Location'] = location.text
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
                    #df.iloc[index]['Info'] = df1[0].to_dict('records')
                    val = df1[0]
                    df.loc[index,'Info'] = val.to_dict('records')
                except NoSuchElementException:
                    print("not able to retrieve element")
                    pass
                except Exception as e:
                    print(e)
                    pass

            
                self.driver.execute("get", {'url': "https://openinframap.org/stats/area/United%20Kingdom/plants"})
                

                time.sleep(1)
            
            print(df)



            # elems = self.driver.find_elements(By.TAG_NAME, 'a')
            
            # for elem in elems:
            #     print(elem.get_attribute("href"))
                # url1 = elem.get_attribute("href")
                # self.driver.execute("get", {'url': url1})
                # elements = self.driver.find_elements(By.TAG_NAME, 'a')
            
                # for elem in elements:
                #     print(elem.get_attribute("href"))

            # operator = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Operator"]')
            # power = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Power"]')
            # source = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Source"]')
            # method = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Method"]')
            # wikidata = self.driver.find_elements(By.CSS_SELECTOR, '[data-label="Wikidata"]')
            
            # print(operator[0].text)
            # operator1= []
            # for op in operator :
            #     operator1.append(op.text)
            # power1= []
            # for op in power :
            #     power1.append(op.text)
            # source1= []
            # for op in source :
            #     source1.append(op.text)
            # method1= []
            # for op in method :
            #     method1.append(op.text)
            # wikidata1= []
            # for op in wikidata :
            #     wikidata1.append(op.text)

            #Price = self.driver.find_elements(by=By.CLASS_NAME, value="propertyCard-priceValue")
            # Address = self.driver.find_elements(By.TAG_NAME, "address")
            # for address in Address :
            #     print(address.text)
            # Title = self.driver.find_element(by=By.CLASS_NAME, value="expPropCardDescription")
            # Description = self.driver.find_element(by=By.CLASS_NAME, value="text")

        except:

            pass

        # try :
        #     # self.location_data["Operator"] = operator.text
        #     # print(self.location_data["Operator"])
        #     #self.write_to_dataframe(operator1,power1,source1,method1,wikidata1) 
            
        #     #self.location_data["Description"] = Description.text
        #     #self.location_data["Address"] = Address.text
        #     #self.location_data["Title"] = Title.text
        # except :
        #     pass

    def write_to_dataframe(self,operator,power,source,method,wikidata):
        try:

            data = pd.DataFrame({'Operator': operator,
                                'Power': power,
                                'Source': source,
                                'Method': method,
                                'Wikidata': wikidata
                                })
            print(data)
            

        except Exception as e:
            print("error in writing to dataframe")

    def scrape(self, url): # Passed the URL as a variable

        try:
            
            self.driver.execute("get", {'url': url})
            data = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.plants-table"))).get_attribute("outerHTML")
            df1  = pd.read_html(data)
            df = df1[0]  #iterating list to get dataframe
            print(df)

        except Exception as e:
            self.driver.quit()
            print(e)
            return 0

        time.sleep(10) # Waiting for the page to load.

        self.get_location_information(df)


        self.driver.quit()


        return (self.location_data)
    

url = "https://openinframap.org/stats/area/United%20Kingdom/plants"
x = Scraper()

print(x.scrape(url))
    



    









