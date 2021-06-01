'''
    NOTE - Flipkart keeps changing the class attributes of the html tags.
    Therefore this script might not work in the future.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import re
import random

url = "https://www.flipkart.com/grocery/pr?sid=73z&marketplace=GROCERY&page="

browser = webdriver.Chrome('chromedriver.exe')

for page_number in range(1, 26):
    page_url = url + f"{page_number}"

    browser.get(page_url)
    time.sleep(5)  # loading the website

    if page_number == 1:
        input_pincode = browser.find_element_by_class_name('_166SQN')
        input_pincode.send_keys("110027", Keys.RETURN)
        time.sleep(2)

    page = bs(browser.page_source, 'html.parser')

    # finding container:
    container = page.find_all('div', {'class': '_1YokD2 _3Mn1Gg'})

    # all the products on the page:
    products = container[1].find_all('div', {'class': '_2OvUl0 _1ZK7VC'})

    name = []
    id = []
    image = []
    price = []
    mrp = []
    variant = []
    quantity = []
    for product in products:
        # product id:
        product_link = product.find('a')['href']
        product_id = re.search("pid=\w+", product_link)
        product_id = product_id.group().split("=")[1]
        id.append(product_id)

        # product name:
        product_name = product.find('div', {'class': '_1MbXnE'}).text
        name.append(product_name)

        # product selling price:
        product_selling_price = product.find(
            'div', {'class': '_30jeq3 _3aGlZL'}).text
        product_selling_price = re.sub("[^\w]", "", product_selling_price)
        price.append(float(product_selling_price))

        # product mrp:
        try:
            product_mrp = product.find('div', {'class': {'_3I9_wc'}}).text
        except:
            product_mrp = product_selling_price
        product_mrp = re.sub("[^\w]", "", product_mrp)
        mrp.append(float(product_mrp))

        # product variant:
        try:
            product_variant = product.find(
                'div', {'class': '_1MbXnE _1kHdUD'}).text
        except:
            product_variant = "1"
        variant.append(product_variant)

        # product quantity:
        product_quantity = float(random.randint(100, 1000))
        quantity.append(product_quantity)

        # product image:
        product_image = product.find('img')['src']
        image.append(product_image)

    for i in range(len(id)):
        with open("./flipkart_product_data/flipkart_data.txt", "a+") as file:
            file.write(
                f"{id[i]}, {name[i]}, {price[i]}, {mrp[i]}, {variant[i]}, {quantity[i]}, {image[i]}\n")

browser.close()
