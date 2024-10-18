from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

driver = webdriver.ChromiumEdge()
try:
    driver.get('https://www.pepperfry.com/stores/cities/all.html')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sd-city-card a')))
    city_elements = driver.find_elements(By.CSS_SELECTOR, '.sd-city-card a')
    city_links = [element.get_attribute('href') for element in city_elements]
    all_addresses=[]
    for link in city_links:
        driver.get(link)
        cnt=1
        while True:
            try:
                # goes through all the addresses in one location
                address_elements = driver.find_elements(By.XPATH,f'//*[@id="studio-card-section-wrapper"]/div[1]/div/div/div[{cnt}]/pf-studio-specific-card-section/div/div/div/a/div[2]/div')
                addresses = [address.get_attribute('innerText') for address in address_elements if address.get_attribute('innerText').strip()]
                all_addresses.extend(addresses)
                if not addresses:
                    break
                cnt += 1
            except NoSuchElementException:
                break
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sd-city-card a')))
    # fetched all the store addresses now dumping them into csv
    df = pd.DataFrame(all_addresses)
    if not os.path.exists('data'):
        os.mkdir('data')
    df.to_csv('data/pepperfry_store_addresses.csv', index=False)
finally:
    driver.quit()