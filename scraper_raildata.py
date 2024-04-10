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



    def get_detailed_information(self,df1) :

        try:
            df = df1
            df_final = pd.DataFrame()
            for index, row in df.iterrows():
                link_value = "https://www.railwaydata.co.uk/stations/overview/?TLC="+row['ID']

                self.driver.execute("get", {'url': link_value})

                usage = self.driver.find_elements(by=By.TAG_NAME, value="font")
                station_usage = []
                for e in usage :
                    station_usage.append(e.text)

                df.loc[index,'Used'] = station_usage[1]
                df.loc[index,'Busiest'] = station_usage[2]
                df.loc[index,'Passtoservice'] = station_usage[3]
                df.loc[index,'Changesince21/22'] = station_usage[5]
                df.loc[index,'Details'] = link_value


                stats = self.driver.find_element(by=By.XPATH, value="//div[@class='col-7 col-12-small']/div[2]/div")
                print(stats)
                stat = stats.text
                res_dict = {}
                lines = stat.splitlines()
                for line in lines:
                    if ':' in line  and line.count(':') == 1: 
                        key, value = line.split(':')
                        key = key.strip()
                        value = value.strip()
                        res_dict[key] = value
                    else :
                        continue

                df_stat = pd.DataFrame([res_dict])

                location = self.driver.find_element(by=By.XPATH, value="//div[@class='col-5 col-12-small']/div[2]/div")
                loc = location.text
                loc_dict= {}
                new_lines = loc.splitlines()
                for line in new_lines:
                    if ':' in line  and line.count(':') == 1: 
                        key, value = line.split(':')
                        key = key.strip()
                        value = value.strip()
                        loc_dict[key] = value
                    else :
                        continue

                df_loc = pd.DataFrame([loc_dict])

                res_df =  pd.concat([df_loc, df_stat], axis=1, join='outer')

                df_final = pd.concat([df_final, res_df], axis=0, ignore_index=True) 


                time.sleep(1)
            
                self.driver.execute("get", {'url': "https://www.railwaydata.co.uk/linefiles/route/assets/?ELR=STY&b=0&s=1&l=0&t=0&g=&c="})
                

                time.sleep(1)


            df = pd.concat([df, df_final], axis=1, join='outer')

            print(df)
            return df
             
        except:

            pass


    def write_to_csv(self, df) :

        try :
            df.to_csv('STY.csv')

        except Exception as e:
            print("error in writing to csv")




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
            data = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table"))).get_attribute("outerHTML")
            df  = pd.read_html(data)
            df1 = df[0] 
            df1.columns = df1.iloc[0]
            df1 = df1[1:]
            df1 = df1.reset_index(drop=True)
            df1.columns.values[8] = "Links"

        except Exception as e:
            self.driver.quit()
            print(e)
            return 0

        time.sleep(10)  # Waiting for the page to load.

        df_end = self.get_detailed_information(df1)

        self.write_to_csv(df_end)
        self.driver.quit()
    

url = "https://www.railwaydata.co.uk/linefiles/route/assets/?ELR=STY&b=0&s=1&l=0&t=0&g=&c="
x = Scraper()
x.scrape(url)