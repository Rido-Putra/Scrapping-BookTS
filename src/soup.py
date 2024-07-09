from bs4 import BeautifulSoup
import re


class BSoup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")

    def get_max_page(self):
        max_page = self.find("li", class_="current")
        max_page = str(max_page.get_text())
        max_page = max_page.strip()
        # max_page = get_max_page_manual(max_page)
        max_page = self.get_max_p_re(max_page)
        if max_page is not None:
            return max_page
        else:
            return None

    def get_max_p_re(self, max_page: str):
        pattern = r"Page \d+ of (\d+)"

        match = re.search(pattern, max_page)

        if match:
            out = int(match.group(1))
        else:
            out = None
        return out  # Output: 150

    def get_urls(self):
        urls = []
        products: list[BeautifulSoup] = self.find_all(
            "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
        )
        for index, i in enumerate(products):
            relative_url = i.find("a")["href"]
            full_url = f"https://books.toscrape.com/catalogue/{relative_url}"
            urls.append(full_url)
        return urls

    def scrape_product(self):
        title = self.find("h1").get_text()
        price = self.find("p", class_="price_color").get_text()
        price_fix = float(price.replace("£", ""))
        stock_availability = self.regexpression(
            self.find("p", class_="instock availability").get_text()
        )
        description = self.find("div", id="content_inner").find_all("p")
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

    def regexpression(self, string: str):
        """Extract availability number using regular expression."""
        pattern = r"\((\d+) available\)"
        matches = re.search(pattern, string)
        if matches:
            availability = matches.group(1)
            return availability
        else:
            return None
