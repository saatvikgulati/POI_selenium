from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

uk_stores = {}
driver = webdriver.ChromiumEdge()
try:
    driver.get('https://stores.cartier.com/it/search?q=UK%2CLondon&category=storeLocatorSearch&r=10&storetype=false')
    cnt=1
    address_list = []
    while True:
        try:
            # fetching all addresses
            addresses = driver.find_elements(By.XPATH,f'/html/body/main/div/div[4]/div[1]/div/div[2]/div/ol/li[{cnt}]/article/div[3]/address/div[1]/span')
            ad = [element.get_attribute('innerText').replace('\r\n','').strip().lower() for element in addresses if element.get_attribute('innerText').replace('\r\n','').strip().lower()]
            address_list.extend(ad)
            if not addresses:
                break
            cnt += 1
        except NoSuchElementException:
            break
    address_list = [element.replace('\n','') for element in address_list]
    address_list = list(set(address_list))
    uk_stores['UK, London'] = address_list

    # dumping to csv
    df = pd.DataFrame(dict([(i,pd.Series(j)) for i,j in uk_stores.items()]))
    if not os.path.exists('data'):
        os.mkdir('data')
    df.to_csv('data/uk_london_addresses.csv',index=False)
finally:
    driver.quit()