from bs4 import BeautifulSoup
import requests
from datetime import date
import xlsxwriter

today = date.today()
ukdate = today.strftime("%d-%m-%Y")
headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})

products = ["https://www.argos.co.uk/product/5718469",
            "https://www.argos.co.uk/product/4019956",
            "https://www.argos.co.uk/product/8434719",
            "https://www.argos.co.uk/product/8819217",
            "https://www.argos.co.uk/product/4019846",
            "https://www.argos.co.uk/product/8996745",
            "https://www.argos.co.uk/product/7442984",
            "https://www.argos.co.uk/product/6017808",
            "https://www.argos.co.uk/product/6788986",
            "https://www.argos.co.uk/product/8069500",
            "https://www.argos.co.uk/product/8687669",
            "https://www.argos.co.uk/product/4659282",
            "https://www.argos.co.uk/product/7955536",
            "https://www.argos.co.uk/product/7956975",
            "https://www.argos.co.uk/product/4094373",
            "https://www.argos.co.uk/product/9188466",
            "https://www.argos.co.uk/product/7307160",
            "https://www.argos.co.uk/product/6846440",
            "https://www.argos.co.uk/product/6847504",
            "https://www.argos.co.uk/product/1400386",
            "https://www.argos.co.uk/product/6556493",
            "https://www.argos.co.uk/product/6851387",
            "https://www.argos.co.uk/product/6851150",
            "https://www.argos.co.uk/product/2077921",
            "https://www.argos.co.uk/product/2078195"]

product_dict = {}

for product in products:
    # Get url from tuple
    response = requests.get(product, headers=headers)

    # Create the soup from the url request
    soup = BeautifulSoup(response.text, features="html.parser")

    # Get the item name
    product = soup.find("span", attrs={"data-test": "product-title"})
    product_text = product.get_text()

    # Get the Cat No
    cat_num = soup.find("span", attrs={"itemprop": "sku"})
    cat_num_text = cat_num.get_text()

    # Get the price
    price = soup.find("h2")
    price_text = price.get_text()

    # Stick it in an array for flask
    product_dict[product_text + " " + "(" + cat_num_text + ")"] = price_text

workbook = xlsxwriter.Workbook("xlsx/prices_" + ukdate + ".xlsx")
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

row = 2
col = 0

worksheet.write(0, 0, "Price Checker", bold)

for product_xlsx, price_xlsx in (product_dict.items()):
    worksheet.write(row, col, product_xlsx)
    worksheet.write(row, col + 1, price_xlsx)
    row += 1

worksheet.set_column(0, 0, 70)
workbook.close()
