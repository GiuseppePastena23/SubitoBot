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
import dearpygui.dearpygui as dpg
import requests
import logging
from Product import Product


'''Check if the URL is correct by checking if it is actually an URL and by checking if is actually an existent subito.it page '''
def check_url(url) -> bool:
    try:
        response = requests.options(url)
        if response.ok:   # alternatively you can use response.status_code == 200
            try:
                if(driver.find_element(By.CLASS_NAME ,"ErrorLayout_message__1rngn")): 
                    logging.info(f"Found the ErrorLayout_message in {url} URL is not correct")
                    return False
            except exceptions.NoSuchElementException:
                logging.info(f"Cannot find the ErrorLayout_message in {url}, URL is correct")
                return True
        else:
            logging.info("URL non existent")
            return False
    except Exception as e:
        logging.exception(f"an error occurred: {e}.")

#FIX overlapping URLS
#TODO refactor this function in three functions 
def check_sites(urls) -> None:
    driver = webdriver.Chrome(service=service, options =chrome_options)
    driver2 = webdriver.Chrome(service=service, options =chrome_options)
    start = time.time()
    results = 0
    
    for url in urls: 
        products = []
        most_recent_post_id = 0
        exit_flag = False
        txt_file_name = os.path.join(os.getcwd(), "lastcheckedproducts", str(url).replace("https://www.subito.it/annunci-italia/vendita/usato/?q=", "").replace("+", "").replace("\n", "") + "-last_checked.txt")
        if(os.path.isfile(txt_file_name)):
            f = open(txt_file_name, "r")
            most_recent_post_id = int(f.readline().replace("\n", ""))
            f.close()
        
        i = 2 # product page counter 
        original_url = url 
        current_url = original_url 
        try:
            while not exit_flag: # Keep checking pages until an error message is found
                driver.get(current_url)
                logging.info(f"Current URL : {current_url}") 


                try:
                    # Try to find the error message element
                    error_message = driver.find_element(By.CLASS_NAME, "ErrorLayout_message__1rngn")
                    if error_message:
                        break # Exit the while loop if the error message is found
                except exceptions.NoSuchElementException:
                    # Error message not found, continue processing
                    pass

                for price, clickable in zip(driver.find_elements(By.CLASS_NAME, 'index-module_container__zrC59'), driver.find_elements(By.CLASS_NAME, 'SmallCard-module_link__hOkzY')):
                    product_price = price.text
                    if ("VENDUTO" not in product_price and len(product_price) > 0):
                        product_price = product_price.replace(" €", "")
                        product_link = str(clickable.get_attribute('href'))
                        driver2.get(product_link)
                        product_id = int(driver2.find_element(By.XPATH, '//*[@id="layout"]/main/div[3]/div[1]/div[1]/section/div[2]/div[1]/span').text.replace("ID: ", ""))
                        if(product_id == most_recent_post_id):
                            exit_flag = True
                            break
                        prodotto = Product(product_id, product_link, product_price) 
                        products.append(prodotto)
                        f = open("prices.txt","a")
                        f.write(prodotto.to_string())
                        results += 1
                
                current_url = original_url + "&o=" + str(i)
                i += 1

            f = open(txt_file_name, "w")
            if(not exit_flag and len(products) > 0):
                f.flush()
                f.write(str(products[0].get_id()) + "\n")
            f.close()
            time.sleep(5)
            
        except Exception as e:
            logging.exception(f"an error occurred: {e}")
            continue
            

    end = time.time()
    logging.info(f"URLs list checked, Found {results} in {end-start:.6f} seconds")
    driver.quit()
    driver2.quit()

#--------------------------------------#
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
chrome_options = Options()
#chrome_options.add_argument("--headless=new")
service = Service(executable_path="chromedriver.exe")

products = [] 
#read_prices_from_file()



'''driver.get("https://subito.it") 
# accept cookie prompt 
try:
    cookie_button = driver.find_element(By.ID, "didomi-notice-agree-button")
    cookie_button.click() 
except Exception:
    logging.info("Cannot find cookie button, The browser is probably running in headless mode")'''



