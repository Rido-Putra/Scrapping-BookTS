import requests
from bs4 import BeautifulSoup
import re

def opening():
    print("------------------------------------------")
    print("Hello, Welcome to scrapping project!")
    print("------------------------------------------")
    return 

#HTTP Request
def get_request(url):  
    request = requests.get(url)
    if request.status_code == 200:
        print("request succesful")
        html = request.content
        return html
    else:
        print("request failed")

#HTML Parsing
def get_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

#Regular Expression --> cheat untuk ambil data by pola
def regexpression(string):
    pattern = r'\((\d+) available\)'
    matches = re.search(pattern, string)
    if matches:
        availability = matches.group(1)
        return availability
    else: 
        return None
    
#Scrape One Product
def scrape_product(soup):
    title = soup.find("h1").get_text()
    price = soup.find("p").get_text()
    price_fix = float(price.replace("£", ""))
    stock_availability = regexpression(soup.find("p", class_ ="instock availability").get_text())
    description = soup.find("div", id ="content_inner").find_all("p")
    # for index , p in enumerate(decsription): ==> find index "p"
    #     print(f'index {index}, p {p}')
    final_description = description[3]
    final_description = final_description.get_text()        
    product = {"title" : title, 
               "price" : price_fix, 
               "stock availability" : stock_availability, 
               "product description" : final_description }  
    return product






if __name__ == "__main__":
    """
    1. acces url book.toscrape.com
    2. check statuscode for request url
    2a. if status code 200 --> continue, else "error can't access url"
    3. convert html to beautifulsoup
    4. start scrape for 1 product (title, price, stock availability, product description)
    5. construct dictionary info one variable"""

    welcome = opening()
    base_url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    html = get_request(base_url)
    soup = get_soup(html)
    product1 = scrape_product(soup)
    print(product1)
    

