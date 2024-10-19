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
    all_city_names=[]
    all_store_addresses = {}
    cnt_name = 1
    while True:
        try:
            city_names = driver.find_elements(By.XPATH,f'//*[@id="studio-card-section-wrapper"]/div[1]/div/pf-all-cities-section/div/cdk-virtual-scroll-viewport/div[1]/div/div[{cnt_name}]/pf-city-card/div/div/div[1]')
            city_name = [element.get_attribute('innerText').replace('\r\n', '').strip().lower() for element in city_names if element.get_attribute('innerText').replace('\r\n','').strip().lower()]
            all_city_names.extend(city_name)
            cnt_name += 1
            if not city_name:
                break
        except NoSuchElementException:
            break
    for link in city_links:
        driver.get(link)
        cnt=1
        while True:
            try:
                # goes through all the addresses in one location
                address_elements = driver.find_elements(By.XPATH,f'//*[@id="studio-card-section-wrapper"]/div[1]/div/div/div[{cnt}]/pf-studio-specific-card-section/div/div/div/a/div[2]/div')
                addresses = [address.get_attribute('innerText').replace('\r\n','').strip().lower() for address in address_elements if address.get_attribute('innerText').replace('\r\n','').strip().lower()]
                all_addresses.extend(addresses)
                if not addresses:
                    break
                cnt += 1
            except NoSuchElementException:
                break
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sd-city-card a')))
    all_addresses = list(set(all_addresses))
    all_city_names = list(set(all_city_names))
    all_addresses = [element.replace('\n','').strip() for element in all_addresses]
    #due to bhubaneshwar spelling being different in city_names have to replace it
    all_city_names = [element.replace('\n','').strip().replace('bhubaneshwar','bhubaneswar') for element in all_city_names]
    for city_name in all_city_names:
        all_store_addresses[city_name] = [address_name for address_name in all_addresses if city_name in address_name]
    # Create a DataFrame
    df = pd.DataFrame(dict([(i,pd.Series(j)) for i,j in all_store_addresses.items()]))
    if not os.path.exists('data'):
        os.mkdir('data')
    df.to_excel('data/pepperfry_store_addresses.xlsx', index=False)
finally:
    driver.quit()