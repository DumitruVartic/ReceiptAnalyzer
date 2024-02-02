import requests
from bs4 import BeautifulSoup
import json, re

pattern = re.compile(r"(\d+(\.\d+)?)\s*(kg|g|ml)|(kg+\s+[A-Za-z]+)")

async def scrape_receipt(url, path):
    ''' Scrape receipt data from url and save it to path in json format '''
    soup = get_receipt_soup(url)
    receipt = parse_receipt(soup)
    receipt["url"] = url
    receipt["receipt_data_id"] = url.split("/")[-1:] if len(url.split("/")) <= 5 else url.split("/")[-4:]
    json.dump(receipt, open(path, "w", encoding="utf-8"), indent=4)

def get_receipt_soup(url):
    ''' Get receipt html page as BeautifulSoup object '''
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    return BeautifulSoup(response.content, "html.parser").find("div", {"class": "font-monospace"})

def parse_receipt(soup):
    ''' 
        Parse receipt data from BeautifulSoup object
        Return dict with the receipt data
        Current structure of receipt:
        - store_name
        - adress
        - date
        - total_price
        - products
            - product_name
            - quantity
            - price
            - total_price
            - weigth/volume
            - weigth_type
    '''
    rows = soup.find_all("div")
    
    product_end = 0
    for i, row in enumerate(rows):
        if i > 4 and row.find("p", {"class": "text-xs"}):
            product_end = i
            break

    receipt = {}
    products = []
    for i, row in enumerate(rows):
        if "TOTAL" in row.text:
            receipt["total_price"] = float(row.find_all('span')[1].text.strip())
        if "DATA" in row.text:
            receipt["date"] = row.find_all('span')[0].text.strip().split()[-1]
        if i == 0:
            receipt["store_name"] = row.text.strip()
        if i == 2:
            receipt["adress"] = row.text.strip()
        if i > 4 and i < product_end:
            product = {}
            product["product_name"] = row.find_all('span')[0].text.strip()
            if not product["product_name"]:
                continue
            price_data = row.find_all('span')[1].text.strip().split("x")
            product["quantity"] = float(price_data[0].strip())
            product["price"] = float(price_data[1].strip())
            product["total_price"] = float(rows[i+1].find_all('span')[1].text.split()[0])
            unit_groups = re.search(pattern, product["product_name"])
            # if quantity is not specified, or weigth/volume == quantity then it is assumed that the product is sold by weight/volume
            # maybe add flag to specify that the product is sold as a whole
            if unit_groups:
                product["weigth/volume"] = float(unit_groups.group(1)) if unit_groups.group(1) else product["quantity"]
                product["weigth_type"] = unit_groups.group(3) if unit_groups.group(3) else "kg"
            else:
                product["weigth/volume"] = product["quantity"]
                product["weigth_type"] = "kg"
            products.append(product)
    receipt["products"] = products
    return receipt