from meli_scrapper import MercadoLibreScraper
from utils.dynamo_handler import DynamoHandler
from utils.data_cleaner import DataCleaner
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv(override=True)

# Create a DBHandler object
db_handler = DynamoHandler()

# Initialize scraper
scraper = MercadoLibreScraper(country_domain="com.ar")

# Initialize data cleaner
data_cleaner = DataCleaner()

# Query search term from command line
search = sys.argv[1]
max_pages = 99
manufacturer = search.split("-")[0]
model = search.split("-")[1]

# Search for products
results = scraper.search_products(search, max_pages)

# Clean results
results = data_cleaner.clean(results, manufacturer, model)

# Export results to MySQL database
db_handler.insert_listings_df(results)

print("Done!")
