import streamlit as st
from data_utils.get_data import get_data
from page_factory.utils import set_sidebar_filters
from page_factory.charts import PriceLineChart, PriceHistogram


def home():
    st.set_page_config(page_title="Home page", layout="wide")

    data = get_data()

    manufacturer, model, currency, year_range, kilometers_range, date = (
        set_sidebar_filters(data, "home")
    )

    print(
        "Filters:",
        manufacturer,
        model,
        currency,
        year_range,
        kilometers_range,
        date,
    )

    data = data[
        (data["date"] == date)
        & (data["manufacturer"] == manufacturer)
        & (data["model"] == model)
        & (data["year"] >= year_range[0])
        & (data["year"] <= year_range[1])
        & (data["kilometers"] >= kilometers_range[0])
        & (data["kilometers"] <= kilometers_range[1])
        & (data["currency"] == currency)
    ]

    page_query = f"{manufacturer} {model}"
    st.title(f"{page_query}")

    # Show KPIs
    columns = st.columns(4)

    columns[0].metric(f"Autos encontrados en {currency}", data.shape[0])
    columns[1].metric(
        f"Autos encontrados en {currency}",
        data.shape[0],
    )
    columns[2].metric(
        f"Precio promedio en {currency}",
        int(data["price"].mean()),
    )
    # Get average price for 2020 cars and 2025 cars
    data_2020 = data[data["year"] == year_range[1] - 5]
    data_2024 = data[data["year"] == year_range[1]]

    print("2020:", data_2020.shape[0], "2025:", data_2024.shape[0])

    precio_promedio_2020 = (
        int(data_2020["price"].mean()) if data_2020.shape[0] > 0 else None
    )
    precio_promedio_2024 = (
        int(data_2024["price"].mean()) if data_2024.shape[0] > 0 else None
    )
    prctg = (
        ((precio_promedio_2024 - precio_promedio_2020) / precio_promedio_2020)
        if precio_promedio_2020 is not None
        and precio_promedio_2024 is not None
        else None
    )

    columns[3].metric(
        f"Depreciacion promedio en {currency} a 5 años",
        f"{prctg:.2%}" if prctg is not None else "N/A",
    )

    # Price line charts
    factory = PriceLineChart()

    # In $
    fig = factory.plot(data, f"Precio promedio por año en {currency}")
    st.plotly_chart(fig)

    # Histograms
    factory = PriceHistogram()

    # Price
    fig = factory.plot(data, "price", f"Distribucion de precios en {currency}")
    st.plotly_chart(fig)

    # Kilometers
    fig = factory.plot(
        data,
        "kilometers",
        f"Distribucion de kilometros de autos en {currency}",
    )
    st.plotly_chart(fig)

    # Years
    fig = factory.plot(
        data, "year", f"Distribucion de años de autos en {currency}", nbins=20
    )
    st.plotly_chart(fig)

    # Show data
    st.write(data)
