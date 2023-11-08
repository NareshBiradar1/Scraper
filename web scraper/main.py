from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]

def scrape_flipkart_product_info(product_url):
    while True:
        headers = ({
            'User-Agent': random.choice(user_agents),
            'Accept-Language': 'en-US, en;q=0.5'
        })

        try:
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()  # Check for request success
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_element = soup.find('span', {'class': 'B_NuCI'})
        product_price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})

        if product_name_element and product_price_element:
            product_name = product_name_element.get_text().strip()
            product_price = product_price_element.get_text().strip()
            data = [
                ["Product Name", product_name[:35] + "..."],
                ["Product Price", product_price],
            ]
            return data
        else:
            print("not found prod")
            continue

def scrape_amazon_product_info(product_url):
    while True:
        headers = {
            'User-Agent': random.choice(user_agents),
        }

        try:
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()  # Check for request success
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Checking for captcha
        captcha_element = soup.find('p', {'class': 'a-last'})

        if captcha_element:
            continue  

        product_name_element = soup.find('span',{'class': 'a-size-large product-title-word-break'} or {'id': 'productTitle'})
        product_price_element = soup.find('span', {'class': 'a-price-whole'})
        product_price_symbol = soup.find('span', {'class': 'a-price-symbol'})

        if product_name_element and product_price_element:
            product_name = product_name_element.get_text().strip()
            price_symbol = product_price_symbol.get_text().strip()
            product_price = product_price_element.get_text().strip()[:-1]

            data = [
                ["Product Name", product_name[:35] + "..."],
                ["Product Price", price_symbol +" "+ product_price],
            ]
            return data
        else:
            continue  

if __name__ == "__main__":
    # Prompt the user to enter URLs for both Amazon and Flipkart products
    amazon_url = input(" Amazon product URL: ")
    flipkart_url = input("Flipkart product URL: ")

    print("Fetching data.........")

    # Scrape product information from Amazon and Flipkart
    amazon_info = scrape_amazon_product_info(amazon_url)
    flipkart_info = scrape_flipkart_product_info(flipkart_url)

    if amazon_info and flipkart_info:
        # Create a table combining data from Amazon and Flipkart
        combined_data = [
            ["Product  Name", amazon_info[0][1], flipkart_info[0][1]],
            ["Product  Price", amazon_info[1][1], flipkart_info[1][1]]
        ]

        headers = [" ", "Amazon", "Flipkart"]
        table = tabulate(combined_data, headers, tablefmt="pretty")

        print("Scraping successful:")
        print(table)
    else:
        print("Scraping failed.")