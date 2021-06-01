from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import random

url = "https://www.naturesbasket.co.in/Online-grocery-shopping/category/"
no_img_url = "https://d1z88p83zuviay.cloudfront.net/Images/no-images425x425.jpg"

category_index = {
    'fruits-vegetables': 5,
    'health': 3,
    'indian_grocery': 12
}


def get_items(url, driver_path):
    browser = webdriver.Chrome(driver_path)

    browser.get(url)
    time.sleep(5)  # waiting for webpage to load

    # scrolling to get all the products
    for _ in range(100):
        browser.execute_script("window.scrollBy(0, 400)")
        time.sleep(2)

    # getting the page source code
    page_source = browser.page_source
    page = bs(page_source, 'html.parser')

    # getting the products container
    container = page.find_all('div', {'class': 'source_Class'})
    if len(container) == 2:
        products = container[1].find_all('div', {'class': 'Search'})
    elif len(container) == 3:
        products = container[2].find_all('div', {'class': 'Search'})

    # getting all the product information
    product_name = []
    product_id = []
    product_image = []
    product_price = []
    product_variant = []
    product_quant = []
    for product in products:
        p_image = product.find('img')['src']  # product image
        if p_image == no_img_url:
            continue
        p_id = product['pro-id']  # product ID
        p_name = product.find(
            'a', {'class': 'search_Ptitle'}).text  # product name
        p_price = float(
            list(product.find('span', {'class': 'search_PSellingP'}))[2])  # product price
        try:
            p_variant = product.find(
                'div', {'class': 'productvariantdiv'}).div.text.strip()
        except:
            p_variant = "1 Pc"
        p_quantity = float(random.randint(100, 1000))  # quantity of product

        # storing the data
        product_image.append(p_image)
        product_id.append(p_id)
        product_name.append(p_name)
        product_price.append(p_price)
        product_variant.append(p_variant)
        product_quant.append(p_quantity)

    browser.close()
    return [product_id, product_name, product_price, product_variant, product_quant, product_image]
