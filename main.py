import requests
from bs4 import BeautifulSoup
import re
import sqlite3


def opening():
    """Display welcome message."""
    print("------------------------------------------")
    print("Hello, Welcome to scrapping project!")
    print("------------------------------------------")
    return


# HTTP Request
def get_request(url):
    """Make an  HTTP request to the given URL  and return the HTML content if successful"""
    request = requests.get(url)
    if request.status_code == 200:
        print("request succesful")
        html = request.content
        # soup = BeautifulSoup(html, "html.parser")
        return html
    else:
        print("request failed")


# HTML Parsing
def get_soup(html):
    """Parse HTML content using BeautifulSoup and return the soup objeck"""
    soup = BeautifulSoup(html, "html.parser")
    return soup


# Regular Expression --> cheat untuk ambil data by pola
def regexpression(string):
    """Extract availability number using regular expression."""
    pattern = r"\((\d+) available\)"
    matches = re.search(pattern, string)
    if matches:
        availability = matches.group(1)
        return availability
    else:
        return None


# Scrape One Product
def scrape_product(url):
    """Scrape product details from given URL."""
    html = get_request(url)
    if html is None:
        return None

    soup = get_soup(html)
    title = soup.find("h1").get_text()
    price = soup.find("p", class_="price_color").get_text()
    price_fix = float(price.replace("£", ""))
    stock_availability = regexpression(
        soup.find("p", class_="instock availability").get_text()
    )
    description = soup.find("div", id="content_inner").find_all("p")
    # for index , p in enumerate(decsription): ==> find index "p"
    #     print(f'index {index}, p {p}')
    final_description = description[3]
    final_description = final_description.get_text()
    product = {
        "title": title,
        "price": price_fix,
        "stock availability": stock_availability,
        "product description": final_description,
    }
    return product


# extract product info page 1 from soup
def product_detail(soup):
    products: list[BeautifulSoup] = soup.find_all(
        "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
    )
    urls = []
    for index, i in enumerate(products):
        relative_url = i.find("a")["href"]
        full_url = f"https://books.toscrape.com/{relative_url}"
        urls.append(full_url)

    product_infos: list[BeautifulSoup] = []
    for index, url in enumerate(urls):
        product_info = scrape_product(url)
        if product_info:
            print(f"Scrape product {index+1}/{len(urls)}:{url}")
            product_infos.append(product_info)
    return product_infos


def get_max_page(soup):
    max_page: BeautifulSoup = soup.find("li", class_="current")
    max_page = str(max_page.get_text())
    max_page = max_page.strip()
    # max_page = get_max_page_manual(max_page)
    max_page = get_max_p_re(max_page)
    if max_page is not None:
        return max_page
    else:
        return None


def get_max_page_manual(max_page: str):
    out = ""
    for p in max_page:
        if p.isnumeric():
            out += p
        elif not p.isnumeric():
            out = ""
    return int(out)


def get_max_p_re(max_page: str):
    pattern = r"Page \d+ of (\d+)"

    match = re.search(pattern, max_page)

    if match:
        out = int(match.group(1))
    else:
        out = None
    return out  # Output: 150


def get_all_urls(max_page: int):
    product_urls = []
    for p in range(1, 2):  # max_page+1
        url = f"https://books.toscrape.com/catalogue/page-{p}.html"
        print(f"Accessing {url}...")
        html = get_request(url)
        soup = get_soup(html)
        products: list[BeautifulSoup] = soup.find_all(
            "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
        )

        for index, i in enumerate(products):
            relative_url = i.find("a")["href"]
            full_url = f"https://books.toscrape.com/catalogue/{relative_url}"
            product_urls.append(full_url)
    return product_urls


def scrape_product_satuan(urls: list[str]):
    output = []

    for index, url in enumerate(urls):
        print(url)
        product_info = scrape_product(url)
        if product_info:
            print(f"Scrape_product {index+1}/{len(urls)}")
            output.append(product_info)
    return output


def save_to_sqlite(data):
    # membuat koneksi ke database(atau mebuat database jika belum ada)
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    # membuat tabel jika belum ada
    cursor.execute(
        """
                      CREATE TABLE IF NOT EXISTS products (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      price REAL,
                      stock_availability INTEGER,
                      product_description TExt)"""
    )

    # memasukan data dari dictionary ke dalam tabel
    for product in data:
        cursor.execute(
            """INSERT INTO products (title, price, stock_availability, product_description)
                          VALUES (?, ?, ?, ?)""",
            (
                product["title"],
                product["price"],
                product["stock availability"],
                product["product description"],
            ),
        )

    # menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()


if __name__ == "__main__":
    """
    1. acces url book.toscrape.com
    2. check statuscode for request url
    2a. if status code 200 --> continue, else "error can't access url"
    3. convert html to beautifulsoup
    4. start scrape for 1 product (title, price, stock availability, product description)
    5. construct dictionary info one variable"""

    welcome = opening()

    base_url = "https://books.toscrape.com/"
    html = get_request(base_url)
    soup = get_soup(html)
    max_p = get_max_page(soup)

    urls = get_all_urls(max_p)
    products = scrape_product_satuan(urls)
    for index, product in enumerate(products):
        print(index, product)
