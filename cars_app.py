import streamlit as st
import datetime
from page_factory.page_factory import PageFactory
from utils.dynamo_handler import DynamoHandler
from dotenv import load_dotenv
from pages_directory.price_history import price_history

# Load environment variables
load_dotenv(override=True)

db_handler = DynamoHandler()


# Function to determine if cache should be cleared
def should_clear_cache():
    print("Checking if cache should be cleared...")
    now = datetime.datetime.now()
    today_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)

    # Check if last refresh date is before today at 8 AM
    last_refresh = st.session_state.get("last_refresh", None)

    print(f"Last refresh was at {last_refresh}")
    if last_refresh is None or last_refresh < today_8am:

        st.session_state["last_refresh"] = now  # Update last refresh time
        return True

    print("Cache should not be cleared.")
    return False


def home():
    factory = PageFactory()

    factory.create_page(db_handler)


home_page = st.Page(home, title="Home Page", icon="🆕")
history_page = st.Page(price_history, title="Price History", icon="📈")

pg = st.navigation({"Home": [home_page], "Price History": [history_page]})

if should_clear_cache():
    st.cache_data.clear()

pg.run()
