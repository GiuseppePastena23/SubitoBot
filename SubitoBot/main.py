import os
import sys
import time
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import logging
from Product import Product


'''Check if the URL is correct by checking if it is actually an URL and by checking if is actually an existent subito.it page '''
def check_url(url) -> bool:
    try:
        response = requests.options(url)
        if not(response.ok):
            logging.info("URL non existent")
            return False
        try:
            if(driver.find_element(By.CLASS_NAME ,"ErrorLayout_message__1rngn")): 
                logging.info(f"Found the ErrorLayout_message in {url} URL is not correct")
                return False
        except exceptions.NoSuchElementException:
                logging.info(f"Cannot find the ErrorLayout_message in {url}, URL is correct")
                return True 
    except Exception as e:
        logging.exception(f"an error occurred: {e}.")


def check_lastid(txt_file_name, url):
    
    if(os.path.isfile(txt_file_name)):
        f = open(txt_file_name, "r")
        most_recent_post_id = int(f.readline().replace("\n", ""))
        f.close()
        return most_recent_post_id

    else:
        return 0
    
def is_error_message(url, driver):
    try: 
        if(driver.find_element(By.CLASS_NAME ,"ErrorLayout_message__1rngn")): 
                logging.info(f"Found the ErrorLayout_message in {url} URL is not correct")
                return True
    except Exception:
        return False
    


    
#FIX overlapping URLS
#TODO refactor this function in three functions 
def check_sites(urls) -> None:
    
    start = time.time()
    results = 0
    
    for url in urls: 
        products = []
        exit_flag = False
        txt_file_name = os.path.join(os.getcwd(), "lastcheckedproducts", str(url).replace("https://www.subito.it/annunci-italia/vendita/usato/?q=", "").replace("+", "").replace("\n", "") + "-last_checked.txt")
        most_recent_post_id = check_lastid(txt_file_name, url)
        

        i = 2 # product page counter (starts at 2 because page 1 is the firstPage)

        original_url = url 
        current_url = url 
        try:
            while not exit_flag: # Keep checking pages until an error message is found
                driver.get(current_url)

                logging.info(f"Current URL : {current_url}") 
                
                if is_error_message(url, driver):
                    break
                
                for price, clickable in zip(driver.find_elements(By.CLASS_NAME, 'index-module_container__zrC59'), driver.find_elements(By.CLASS_NAME, 'SmallCard-module_link__hOkzY')):
                    product_price = price.text
                    if ("VENDUTO" not in product_price and len(product_price) > 0):
                        product_price = product_price.replace(" €", "")
                        product_link = str(clickable.get_attribute('href'))

                        driver2.get(product_link)
                        product_id = int(driver2.find_element(By.XPATH, '//*[@id="layout"]/main/div[3]/div[1]/div[1]/section/div[2]/div[1]/span').text.replace("ID: ", ""))
                        
                        if(product_id == most_recent_post_id):
                            exit_flag = True # if this is TRUE it means that the product is already been checked, there are no new products
                            break
                        
                        prodotto = Product(product_id, product_link, product_price) 
                        products.append(prodotto)
                        all_products.append(prodotto)

                        with open("prices.txt", "a") as f:
                            f.write(prodotto.to_string())
                            f.close()

                        results += 1
                
                current_url = original_url + "&o=" + str(i)
                i += 1

            if(exit_flag == False and len(products) > 0):
                with open(txt_file_name, 'w') as f:
                    f.write(str(products[0].get_id()) + "\n")
                    f.close()
            
        except Exception as e:
            logging.exception(f"an error occurred: {e}")
            continue
            

    end = time.time()
    logging.info(f"URLs list checked, Found {results} in {end-start:.6f} seconds")
    driver.quit()
    driver2.quit()

def get_products():
    return all_products


#--------------------------------------#
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver2 = webdriver.Chrome(service=service, options=chrome_options)

all_products = []

