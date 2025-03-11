import streamlit as st
from page_factory.page_factory import PageFactory
from utils.dynamo_handler import DynamoHandler
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

db_handler = DynamoHandler()


def home():
    factory = PageFactory()
    factory.create_page(db_handler)


page = st.Page(home, title="New Page", icon="🆕")

pg = st.navigation({"Home": [page]})



pg.run()
