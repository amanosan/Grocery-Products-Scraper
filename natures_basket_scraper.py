# Scraping Data from Nature's Basket

import json
from utils import get_items

category_index = {
    # 'Fruits-Vegetables': 5,
    'Health': 3,
    'Indian-Grocery': 12,
    'Internation-Cuisine': 4,
    'Snacks-Beverages': 9,
    'Breakfast--Dairy-Bakery': 11
}
url = "https://www.naturesbasket.co.in/Online-grocery-shopping/"
no_img_url = "https://d1z88p83zuviay.cloudfront.net/Images/no-images425x425.jpg"

for category, index in category_index.items():
    product_list = get_items(
        url + f"{category}/{index}_0_0", "./chromedriver.exe")

    with open(f'./natures_basket_product_data/{category}.txt', 'a+') as file:
        for i in range(len(product_list[0])):
            file.write(
                f"{product_list[0][i]}, {product_list[1][i]}, {product_list[2][i]}, {product_list[3][i]}, {product_list[4][i]}, {product_list[5][i]}\n")
