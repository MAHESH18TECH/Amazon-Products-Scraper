#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing the necessary Libraries
import pandas as pd
import random
import time
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#Setting Up our webdriver by adding options

chrome_options = Options()



chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(executable_path=r'chromedriver', options=chrome_options)

product_links = []


prdct_links = []
prdct_name = []
prdct_price = []
prdct_reviews_count = []



df = pd.DataFrame()


#Navigationg the links for 20 pages

for page in range(1,10):
    try:
        driver.get(f'https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1690041116&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}')
        time.sleep(random.uniform(3.9,4.5))
        
        #Getting Links for all products
        links = driver.find_elements(By.CSS_SELECTOR, 'h2 a')  # CSS selector for product links
        for link in links:
            product_links.append(link.get_attribute("href"))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(product_links))
        
        for m in product_links:
            prdct_links.append(m)
            
        # Get the product name, price, rating, and number of reviews.
        product_name = driver.find_elements(By.XPATH,'//*[@class="a-size-medium a-color-base a-text-normal"]')
        for name in product_name:
            prdct_name.append(name.text)
            
        #Getting the price 
        product_price = driver.find_elements(By.XPATH,'//*[@class = "a-price"]')
        for p in product_price:
            prdct_price.append(p.text)
            
        #Getting the number of reviews
        number_of_reviews = driver.find_elements(By.XPATH,'//*[@class = "a-size-base s-underline-text"]')
        for reviews in number_of_reviews:
            prdct_reviews_count.append(reviews.text)

    except Exception as e:
        prdct_links.append("NaN")
        nprdct_name.append("NaN")
        prdct_price.append("NaN")
        prdct_reviews_count.append("NaN")


# Find the maximum length among the lists
max_length = max(len(prdct_links), len(prdct_name), len(prdct_price), len(prdct_reviews_count))
    
# Pad the shorter lists with a default value (e.g., None) to match the maximum length
padded_list1 = prdct_links + [None] * (max_length - len(prdct_links))
padded_list2 = prdct_name  + [None] * (max_length - len(prdct_name))
padded_list3 = prdct_price + [None] * (max_length - len(prdct_price))
padded_list4 = prdct_reviews_count + [None] * (max_length - len(prdct_reviews_count))

# Create a DataFrame from the padded lists
df = pd.DataFrame({'Product Links': padded_list1, 'Product Name': padded_list2, 'Product Price': padded_list3, 'Product Reviews Count': padded_list4})
de = df.dropna()
de.to_csv("Product_Details_Part1.csv")

#Part2 Code

data_2 = []

for l in product_links:
    driver.get(l)
    time.sleep(5)
    try:
        # Wait for the product details to load.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))

        # Get ASIN
        asin = driver.find_element(By.XPATH,'//*[@id="detailBullets_feature_div"]/ul/li[4]').text.strip()

        # Get Product Description
        product_description = driver.find_element(By.ID, "featurebullets_feature_div").text.strip()

        # Get Manufacturer
        manufacturer = driver.find_element(By.XPATH,'//*[@id="detailBullets_feature_div"]/ul/li[8]').text.strip()

        #Get Rating
        rating_element = driver.find_element(By.XPATH, '//*[@id="detailBulletsWrapper_feature_div"]/ul[2]/li')
        rating_text = rating_element.text.strip()
        product_rating = rating_text

    except Exception as e:
        asin = "null"
        product_description = "null"
        manufacturer = "null"
        product_rating = "null"

    finally:
        print("ASIN:", asin)
        print("Product Description:", product_description)
        print("Manufacturer:", manufacturer)
        print("Product Rating (out of 5):", product_rating[18:21])
        
    
    part2_data = { "ASIN" : asin, "Product Description": product_description,"Manufacturer" : manufacturer, "Product Rating (out of 5)" : product_rating[18:21]}

    data_2.append(part2_data) 
dt = pd.DataFrame(data_2)
dt.to_csv("Product_Details_Part2.csv")

