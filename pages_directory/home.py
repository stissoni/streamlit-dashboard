import streamlit as st
from data_utils.get_data import get_data
from page_factory.utils import set_sidebar_filters
from page_factory.charts import PriceLineChart, PriceHistogram


def home():
    st.set_page_config(page_title="Home page", layout="wide")

    data = get_data()

    manufacturer, model, date = set_sidebar_filters(data, "home")

    data = data[
        (data["date"] == date)
        & (data["manufacturer"] == manufacturer)
        & (data["model"] == model)
    ]

    page_query = f"{manufacturer} {model}"

    st.title(f"{page_query}")

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
    data = data[
        (data["year"] >= year_range[0]) & (data["year"] <= year_range[1])
    ]
    # Filter data by kilometers
    data = data[
        (data["kilometers"] >= kilometers_range[0])
        & (data["kilometers"] <= kilometers_range[1])
    ]

    # Show KPIs
    columns = st.columns(5)

    columns[0].metric("Autos encontrados", data.shape[0])
    columns[1].metric(
        "Autos encontrados en $", data[data["currency"] == "$"].shape[0]
    )
    columns[2].metric(
        "Precio promedio en $",
        int(data[data["currency"] == "$"]["price"].mean()),
    )
    columns[3].metric(
        "Autos encontrados en US$",
        int(data[data["currency"] == "US$"].shape[0]),
    )
    columns[4].metric(
        "Precio promedio en US$",
        int(data[data["currency"] == "US$"]["price"].mean()),
    )

    # Price line charts
    factory = PriceLineChart()

    # In $
    fig = factory.plot(data, "$", "Precio promedio por año en $")
    st.plotly_chart(fig)

    # In US$
    fig = factory.plot(data, "US$", "Precio promedio por año en US$")
    st.plotly_chart(fig)

    # Histograms
    factory = PriceHistogram()

    # Price in $
    ars_data = data[data["currency"] == "$"]
    fig = factory.plot(ars_data, "price", "Distribucion de precios en $")
    st.plotly_chart(fig)

    # Price in US$
    usd_data = data[data["currency"] == "US$"]
    fig = factory.plot(usd_data, "price", "Distribucion de precios en US$")
    st.plotly_chart(fig)

    # Kilometers
    fig = factory.plot(data, "kilometers", "Distribucion de kilometros")
    st.plotly_chart(fig)

    # Years
    fig = factory.plot(data, "year", "Distribucion de años", nbins=20)
    st.plotly_chart(fig)

    # Show data
    st.write(data)
