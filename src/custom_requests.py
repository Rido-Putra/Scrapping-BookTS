from requests import Session

# from bs4 import BeautifulSoup
from src.soup import BSoup
from requests.exceptions import ConnectionError


class CustomRequests(Session):  # readability lebih bagus
    def __init__(self) -> None:
        super().__init__()

    def get_status_code(self, url: str):
        """Get status code of url"""
        return self.get(url).status_code

    def get_html_soup(self, url: str):
        """Get html content of url"""
        html = self.get(url)
        if html.status_code == 200:
            return BSoup(html.content)
        else:
            raise ConnectionError("can't access url, status code is not 200")

    def get_all_urls(self, max_page: int):
        product_urls = []
        for p in range(1, max_page + 1):  # max_page+1
            url = f"https://books.toscrape.com/catalogue/page-{p}.html"
            print(f"Accessing {url}...")
            soup = self.get_html_soup(url)
            urls = soup.get_urls()
            product_urls.extend(urls)
        return product_urls
