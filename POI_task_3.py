from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

driver=webdriver.ChromiumEdge()
all_property_names = []
all_property_types = []
all_property_links = []
try:
        driver.get('https://www.99acres.com/')
        cnt_property=1
        while True:
            try:
                properties = driver.find_elements(By.XPATH, f'// *[ @ id = "app"] / div / div[2] / div[2] / div[2] / div[1] / div[1] / div / ul / li[1] / div / ul / li / div / ul / li[{cnt_property}] / a')
                properties_link = [element.get_attribute('href') for element in properties if element.get_attribute('href')]
                all_property_links.extend(properties_link)
                cnt_property+=1
                if not properties_link:
                    break
            except NoSuchElementException:
                break
        for link in all_property_links:
            driver.get(link)
            property_names_cnt=2
            while True:
                try:
                    property_names = driver.find_elements(By.XPATH, f'/html/body/div[1]/div/div/div[4]/div[3]/div[2]/section[{property_names_cnt}]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[1]/div')
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
            driver.back()
        print(all_property_names)
        print(all_property_types)
finally:
    driver.quit()