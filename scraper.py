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
        # Fetch all property links
        WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@data-custominfo, "For Buyers")]')))
        properties = driver.find_elements(By.XPATH, '//a[contains(@data-custominfo, "For Buyers")]')
        properties_link = [element.get_attribute('href') for element in properties if element.get_attribute('href')]
        if len(properties_link) > 1:
            print(f"{len(properties_link)} links found")
            pd.DataFrame({'links':properties_link}).to_csv(f'data/all_property_links.csv',index=False)

    finally:
        driver.quit()

def get_area_details(url):
    all_property_names = []
    all_property_types = []
    driver = webdriver.ChromiumEdge()
    try:
        for link in url:
            driver.get(link)
            WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tupleNew__locationName, .ellipsis')))
            property_names = driver.find_elements(By.CSS_SELECTOR, 'div.tupleNew__locationName, .ellipsis')
            property_name = [element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower() for element in property_names if element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower()]
            all_property_names.extend(property_name)
            WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'h2.PseudoTupleRevamp__subHeading, .ellipsis, .PseudoTupleRevamp__projectHeading')))
            property_types = driver.find_elements(By.CSS_SELECTOR,'h2.PseudoTupleRevamp__subHeading, .ellipsis, .PseudoTupleRevamp__projectHeading')
            for element in property_types:
                if property_types:
                    spans = element.find_elements(By.TAG_NAME, 'span')
                    span_text = [element.get_attribute('innerText').strip().replace('\r\n', '').replace('\n', '').lower() for
                                 element in spans if spans]
                    all_property_types.extend(span_text)
            # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pageComponent a')))
        print(all_property_types)
        print(all_property_names)
        pd.DataFrame({'names':all_property_names}).to_csv(f'data/all_property_names_{link.split("/")[-1]}.csv',index=False)
    finally:
        driver.quit()