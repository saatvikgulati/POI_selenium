from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import config

driver=webdriver.ChromiumEdge()
all_property_names = []
all_property_types = []
all_property_links = []
try:
        driver.get(config.url_home)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@data-custominfo, "For Buyers")]')))
        properties = driver.find_elements(By.XPATH, '//a[contains(@data-custominfo, "For Buyers")]')
        properties_link = [element.get_attribute('href').strip().lower() for element in properties if element.get_attribute('href').strip().lower()]
        all_property_links.extend(list(set(properties_link)))
        for link in all_property_links:
            print(link)
            driver.delete_all_cookies()
            driver.get(link)
            property_names = driver.find_elements(By.CSS_SELECTOR, 'div.tupleNew__locationName, .ellipsis')
            properties_name = [element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower() for element in property_names if element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower()]
            print(properties_name)
            property_types = driver.find_elements(By.CSS_SELECTOR,'h2.PseudoTupleRevamp__subHeading, .ellipsis, .PseudoTupleRevamp__projectHeading')
            for element in property_types:
                if property_types:
                    spans = element.find_elements(By.TAG_NAME,'span')
                    span_text = [element.get_attribute('innerText').strip().replace('\r\n','').replace('\n','').lower() for element in spans if spans]
                    all_property_types.extend(span_text)
            driver.back()
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@data-custominfo, "For Buyers")]')))
        all_dict={'Name':all_property_names,'Links':all_property_links,'Types':all_property_types}
        pd.DataFrame(dict([(i,pd.Series(j)) for i,j in all_dict.items()])).to_csv('data/property_list.csv',index=False)
        print(all_property_types)
finally:
    driver.quit()