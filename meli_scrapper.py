import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import sys


class MercadoLibreScraper:
    def __init__(self, country_domain="com.mx"):
        """
        Initialize the scraper with country domain.
        Examples: 'com.mx' (Mexico), 'com.ar' (Argentina), 'com.br' (Brazil)
        """
        self.base_url = f"https://listado.mercadolibre.{country_domain}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    def search_products(self, query, max_pages=10):
        """
        Search for products and extract basic information
        """
        results = []
        prev_query_len = None
        for page in range(1, max_pages + 1):
            # MELI url looks like this https://listado.mercadolibre.com.ar/laptop-dell#D[A:laptop%20dell]
            if prev_query_len is None:
                url = f"{self.base_url}/{query}"
            else:
                url = f"{self.base_url}/{query}_Desde_{prev_query_len}_NoIndex_True"
            print(url)
            response = self._make_request(url)

            if not response:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            product_containers = soup.select("li.ui-search-layout__item")

            if not product_containers:
                break

            for container in product_containers:
                print()
                print(container)
                print()

                try:
                    # Extract product data
                    price = container.select_one(
                        ".poly-price__current .andes-money-amount__fraction"
                    ).text
                    print("This is the price: ", price)
                    year = container.select_one(
                        ".poly-attributes-list__item:nth-of-type(1)"
                    ).text
                    print("This is the year: ", year)
                    title = container.select_one(".poly-component__title").text.strip()
                    print("This is the title: ", title)
                    kilometers = container.select_one(
                        ".poly-attributes-list__item:nth-of-type(2)"
                    ).text
                    print("This is the kilometers: ", kilometers)
                    price_element = container.select_one(
                        ".poly-price__current .andes-money-amount"
                    )
                    currency = price_element.select_one(
                        ".andes-money-amount__currency-symbol"
                    ).text.strip()
                    print("This is the currency: ", currency)
                    import re

                    url = container.select_one(".poly-component__title")["href"]
                    print("This is the url: ", url)
                    match = re.search(r"MLA-(\d+)", url)

                    publication_id = match.group(1) if match else None
                    print("This is the publication_id: ", publication_id)

                    product = {
                        "url": url,
                        "publication_id": publication_id,
                        "title": title,
                        "year": year,
                        "kilometers": kilometers.replace("Km", "")
                        .strip()
                        .replace(".", ""),
                        "currency": currency,
                        "price": price.replace(".", ""),
                    }

                    results.append(product)
                except Exception as e:
                    print(f"Error extracting product: {e}")

            # Update query length for next page
            prev_query_len = len(results) + 1
            print("Se han agregado ", len(results), " resultados")
            # Respectful delay between requests
            self._random_delay(2, 5)

        return pd.DataFrame(results)

    def get_product_details(self, product_url):
        """
        Scrape detailed information about a specific product
        """
        response = self._make_request(product_url)
        if not response:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Initialize product details dictionary
        details = {"url": product_url, "id": self._extract_product_id(product_url)}

        # Extract title
        title_elem = soup.select_one("h1.ui-pdp-title")
        if title_elem:
            details["title"] = title_elem.text.strip()

        # Extract price
        price_elem = soup.select_one(
            ".ui-pdp-price__second-line .andes-money-amount__fraction"
        )
        if price_elem:
            details["price"] = price_elem.text.strip()

        # Extract seller info
        seller_elem = soup.select_one(".ui-pdp-seller__link-trigger")
        if seller_elem:
            details["seller"] = seller_elem.text.strip()

        # Extract ratings
        rating_elem = soup.select_one(".ui-pdp-reviews__rating")
        if rating_elem:
            details["rating"] = rating_elem.text.strip()

        # Extract specifications
        specs = {}
        spec_rows = soup.select(".ui-pdp-specs__table .andes-table__row")
        for row in spec_rows:
            header = row.select_one(".andes-table__header h3")
            data = row.select_one(".andes-table__column--value")
            if header and data:
                specs[header.text.strip()] = data.text.strip()

        details["specifications"] = specs

        # Extract images
        image_elems = soup.select(".ui-pdp-gallery__figure img")
        details["images"] = [
            img.get("data-zoom", img.get("src"))
            for img in image_elems
            if img.get("data-zoom") or img.get("src")
        ]

        return details

    def export_to_csv(self, dataframe, filename="mercadolibre_data.csv"):
        """
        Export scraped data to CSV
        """
        dataframe.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data exported to {filename}")

    def _make_request(self, url):
        """
        Make a request with error handling and retries
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                # Print response headers, payload, etc.
                print(response)
                print(response.headers)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    self._random_delay(5, 15)
                else:
                    return None

    def _random_delay(self, min_seconds=1, max_seconds=3):
        """
        Add a random delay between requests to avoid being blocked
        """
        time.sleep(random.uniform(min_seconds, max_seconds))

    def _extract_product_id(self, url):
        """
        Extract product ID from URL
        """
        try:
            if "MLA" in url or "MLB" in url or "MLM" in url:
                import re

                match = re.search(r"(MLA|MLB|MLM)\d+", url)
                if match:
                    return match.group(0)
            return url.split("-")[-1]
        except:
            return None


# Example usage
if __name__ == "__main__":
    # Initialize scraper (default is Mexico)
    scraper = MercadoLibreScraper(country_domain="com.ar")

    search = sys.argv[1]
    max_pages = 10
    # Search for products
    results = scraper.search_products(search, max_pages)

    # Print results summary
    print(f"Found {len(results)} products")
    print(results.head())

    # Check results id column has unique values
    if results["publication_id"].nunique() == len(results):
        print("All IDs are unique")
    else:
        print(
            "There is ",
            len(results["publication_id"]) - results["publication_id"].nunique(),
            " duplicated",
        )

    # Data cleaning: remove duplicates
    results = results.drop_duplicates(subset="publication_id")

    # Data cleaning: remove rows with year < 2000 or year > 2025
    results = results[
        (results["year"].astype(int) >= 2000) & (results["year"].astype(int) <= 2025)
    ]

    print("Se han eliminado los duplicados. Ahora hay ", len(results), " resultados")

    # Export results to CSV
    scraper.export_to_csv(results, f"data/{search}.csv")

    # Show entire results DataFrame
    print(results)
