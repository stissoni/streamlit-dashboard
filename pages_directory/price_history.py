import streamlit as st
from page_factory.utils import set_sidebar_filters
from data_utils.get_data import get_data
import plotly.graph_objects as go


def price_history():
    st.set_page_config(page_title="History", layout="wide")

    data = get_data()

    manufacturer, model, currency, year_range, kilometers_range, _ = (
        set_sidebar_filters(data, "price_history")
    )

    title = f"Evolucion del precio promedio {manufacturer} {model}"
    st.title(title)

    data = data[
        (data["manufacturer"] == manufacturer)
        & (data["model"] == model)
        & (data["currency"] == currency)
        & (data["year"] >= year_range[0])
        & (data["year"] <= year_range[1])
        & (data["kilometers"] >= kilometers_range[0])
        & (data["kilometers"] <= kilometers_range[1])
    ]

    # Group data by date and calculate the average price
    price_by_date = data.groupby("date")["price"].mean().reset_index()

    # Get latest price
    latest_price = price_by_date.iloc[-1]["price"]

    # Function to calculate percentage change
    def calculate_change(df, days):
        import pandas as pd

        df = df.copy()
        # Cast date column to datetime
        df["date"] = pd.to_datetime(df["date"])
        past_date = df["date"].max() - pd.Timedelta(days=days)
        past_data = df[df["date"] <= past_date]

        if past_data.empty:
            return None, None  # Avoid errors if there's no data

        past_price = past_data.iloc[-1]["price"]

        change = latest_price - past_price
        prctg = ((latest_price - past_price) / past_price) * 100
        return int(change), prctg

    # Compute price changes
    change_1d, prctg_change_1d = calculate_change(price_by_date, 1)
    change_7d, prctg_change_7d = calculate_change(price_by_date, 7)
    change_30d, prctg_change_30d = calculate_change(price_by_date, 30)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latest Price", f"{int(latest_price):,}")
    col2.metric(
        "Last Day Change",
        f"{change_1d:,}" if change_1d is not None else "N/A",
        f"{prctg_change_1d:.2f}%" if prctg_change_1d is not None else "N/A",
    )
    col3.metric(
        "Last 7 Days Change",
        f"{change_7d:,}" if change_7d is not None else "N/A",
        f"{prctg_change_7d:.2f}%" if prctg_change_7d is not None else "N/A",
    )
    col4.metric(
        "Last 30 Days Change",
        f"{change_30d:,}" if change_30d is not None else "N/A",
        f"{prctg_change_30d:.2f}%" if prctg_change_30d is not None else "N/A",
    )

    # Make Plotly  chart with the price history of the selected car by date
    fig = go.Figure()

    # Add line plot
    fig.add_trace(
        go.Scatter(
            x=price_by_date["date"],
            y=price_by_date["price"],
            mode="lines",
            line=dict(color="#636EFA", width=3),
            name="Price Trend",
        )
    )

    # Improve layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        font=dict(size=14),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.1)"),
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Display only the date (no time)
            tickangle=-45,  # Optional: Rotate labels for readability
            showgrid=True,  # Optional: Show gridlines
            tickmode="array",  # Use the same tickvals as the data
            tickvals=price_by_date[
                "date"
            ],  # Use only actual dates from the dataset
        ),
    )

    st.plotly_chart(fig)

    st.write(price_by_date.set_index("date"))

    # Group data by date and calculate the count of cars
    cars_by_date = data.groupby("date").size()

    print(cars_by_date.head())

    # Make a Plotly bar chart with the number of cars by year
    fig = go.Figure()

    # Plot histogram from cars_by_date Series
    fig.add_trace(
        go.Bar(
            x=cars_by_date.index,
            y=cars_by_date.values,
            marker_color="#EF553B",
            name="Number of Cars",
        )
    )

    # Improve layout
    fig.update_layout(
        title=f"Cantidad de {manufacturer} {model} publicados por fecha",
        xaxis_title="Fecha",
        yaxis_title="Nummero de autos publicados",
        template="plotly_dark",
        font=dict(size=14),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.1)"),
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Display only the date (no time)
            tickangle=-45,  # Optional: Rotate labels for readability
            showgrid=True,  # Optional: Show gridlines
            tickmode="array",  # Use the same tickvals as the data
            tickvals=cars_by_date.index,
        ),
    )

    st.plotly_chart(fig)

    cars_by_date = cars_by_date.reset_index()
    cars_by_date.columns = ["date", "count"]
    st.write(cars_by_date.set_index("date"))

    print("Price History Page loaded")
