from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType

import pandas as pd
from config import *
import time

def get_home_links(url):
    driver = webdriver.ChromiumEdge()
    try:
        driver.get(url)

        counter = 1 
        scraper_list = []
        while True:
            try:
                # Fetch all property links
                properties = driver.find_elements(By.XPATH, xpathpattern_home.format(counter))
                properties_link = [element.get_attribute('href') for element in properties if element.get_attribute('href')]
                if properties_link:
                    scraper_list.extend(properties_link)
                    counter += 1
                else:
                    break
            except NoSuchElementException:
                break
            finally:
                if len(scraper_list) > 1:
                    print(f"{len(scraper_list)} links found")
                    pd.DataFrame({'links':scraper_list}).to_csv(f'all_property_links.csv',index=False)

    finally:
        driver.quit()

def get_area_details(link):
    all_property_names = []
    all_property_types = []
    driver = webdriver.ChromiumEdge()
    driver.get(link)
    property_names_cnt=2
    while True:
        try:
            property_names = driver.find_elements(By.XPATH, xpathpattern_areawise.format(property_names_cnt))
            property_name = [element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower() for element in property_names if element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower()]
            all_property_names.extend(property_name)
            property_names_cnt+=2
            if not property_name:
                break
        except NoSuchElementException:
            break
    property_types = driver.find_elements(By.CSS_SELECTOR,'.tupleNew__propType h2')
    property_type = [element.get_attribute('span').strip()+element.get_attribute('innerText').strip().replace('\r\n', '').replace('\n', '').lower() for
        element in property_types]
    all_property_types.extend(property_type)
    time.sleep(15)
    # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pageComponent a')))
    print(all_property_names)
    print(all_property_types)
    pd.DataFrame({'names':all_property_names}).to_csv(f'all_property_names_{link.split("/")[-1]}.csv',index=False)
    driver.quit()