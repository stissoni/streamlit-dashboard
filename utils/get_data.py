import streamlit as st
from utils.dynamo_handler import DynamoHandler
from utils.data_parser import DataParser


@st.cache_data(ttl=86400)  # 1 day
def get_data():
    db_handler = DynamoHandler()
    data = db_handler.full_scan("listings")

    data_parser = DataParser()
    df = data_parser.parse(data)

    print("Obtained data from DynamoDB. Total rows:", df.shape[0])

    return df
