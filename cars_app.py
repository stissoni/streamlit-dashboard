import streamlit as st

from dotenv import load_dotenv

from pages_directory.price_history import price_history
from pages_directory.home import home

load_dotenv(override=True)

home_page = st.Page(home, title="Home Page", icon="🏠")
price_history_page = st.Page(price_history, title="Price History", icon="📈")

pg = st.navigation({"Pages": [home_page, price_history_page]})

pg.run()
