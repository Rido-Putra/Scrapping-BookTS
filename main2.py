from src.custom_requests import CustomRequests
from src.utils import opening, save_to_sqlite

# modularisasi

if __name__ == "__main__":
    # req = requests.get("https://books.toscrape.com/").status_code # Get status code of url
    opening()
    r = CustomRequests()
    base_url = "https://books.toscrape.com/"
    print(r.get_status_code(base_url))
    soup = r.get_html_soup(base_url)
    max_p = soup.get_max_page()
    print(max_p, type(max_p))
    urls = r.get_all_urls(4)

    output = []
    for i, url in enumerate(urls):
        print(f"scraping {url}")

        soup = r.get_html_soup(url)
        product = soup.scrape_product()

        output.append(product)
        # print(product)

    save_to_sqlite(output)

    #    for o in output:
    #        save_to_sqlite(o)

    print(output)
