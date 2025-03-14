import streamlit as st
from page_factory.page_factory import get_sidebar_filters
from utils.get_data import get_data
import plotly.graph_objects as go


def price_history():
    st.set_page_config(page_title="History", layout="wide")

    data = get_data()
    car_data = get_sidebar_filters(data)

    manufacturer = st.sidebar.selectbox("Select Manufacturer", list(car_data.keys()))

    if manufacturer:
        model = st.sidebar.selectbox("Select Model", car_data[manufacturer]["models"])
    else:
        model = None

    currency = st.sidebar.selectbox("Select Currency", ["$", "US$"])

    data = data[
        (data["manufacturer"] == manufacturer)
        & (data["model"] == model)
        & (data["currency"] == currency)
    ]

    title = f"Evolucion del precio promedio {manufacturer} {model}"
    st.title(title)

    st.sidebar.markdown("## Filtros")

    # Set slider for car years
    min_year = data["year"].min()
    max_year = data["year"].max()

    year_range = st.sidebar.slider(
        "Años de los autos",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    # Set slider for car kilometers
    min_kilometers = data["kilometers"].min()
    max_kilometers = data["kilometers"].max()

    kilometers_range = st.sidebar.slider(
        "Kilometros de los autos",
        min_value=min_kilometers,
        max_value=max_kilometers,
        value=(min_kilometers, max_kilometers),
    )

    # Filter data by year
    data = data[(data["year"] >= year_range[0]) & (data["year"] <= year_range[1])]

    # Filter data by kilometers
    data = data[
        (data["kilometers"] >= kilometers_range[0])
        & (data["kilometers"] <= kilometers_range[1])
    ]

    # Sort data by date
    data = data.sort_values(by="date")

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

    print(price_by_date.head())

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
            tickvals=price_by_date["date"],  # Use only actual dates from the dataset
        ),
    )

    st.plotly_chart(fig)

    st.write(price_by_date.set_index("date"))

    # Group data by date and calculate the count of cars
    cars_by_date = data.groupby("date")["price"].count().reset_index()

    # Make a Plotly bar chart with the number of cars by year
    fig = go.Figure()

    # Add bar plot
    fig.add_trace(
        go.Bar(
            x=cars_by_date["date"],
            y=cars_by_date["price"],
            marker_color="#EF553B",
            name="Number of Cars",
        )
    )

    # Improve layout
    fig.update_layout(
        title="Number of Cars by Year",
        xaxis_title="Year",
        yaxis_title="Number of Cars",
        template="plotly_dark",
        font=dict(size=14),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.1)"),
        xaxis=dict(
            tickformat="%Y-%m-%d",  # Display only the date (no time)
            tickangle=-45,  # Optional: Rotate labels for readability
            showgrid=True,  # Optional: Show gridlines
            tickmode="array",  # Use the same tickvals as the data
            tickvals=cars_by_date["date"],  # Use only actual dates from the dataset
        ),
    )

    st.plotly_chart(fig)

    st.write(cars_by_date.set_index("date"))

    print("Price History Page loaded")
