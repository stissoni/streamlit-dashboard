import streamlit as st
from data_utils.dynamo_handler import DynamoHandler
import pandas as pd


def parse_data(data):
    df = pd.DataFrame(data)

    df["price"] = pd.to_numeric(
        df["price"], errors="coerce", downcast="unsigned"
    )
    df["year"] = pd.to_numeric(
        df["year"], errors="coerce", downcast="unsigned"
    )
    df["kilometers"] = pd.to_numeric(
        df["kilometers"], errors="coerce", downcast="unsigned"
    )

    # Sort by date
    df = df.sort_values(by="date", ascending=True)

    return df


@st.cache_data(ttl=86400)  # 1 day
def get_data():
    db_handler = DynamoHandler()

    data = db_handler.full_scan("listings")

    df = parse_data(data)

    print("Obtained data from DynamoDB. Total rows:", df.shape[0])

    return df
