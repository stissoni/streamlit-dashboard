import streamlit as st
from .price_histogram import PriceHistogram
from .price_linechart import PriceLineChart
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


@st.cache_data(ttl=86400)  # 1 day
def get_sidebar_filters(df):
    # Get distinct manufacturers
    manufacturers = df["manufacturer"].unique()

    # Get distinct models by manufacturer
    car_data = {}
    for manufacturer in manufacturers:
        models = df[df["manufacturer"] == manufacturer]["model"].unique()
        car_data[manufacturer] = {"models": models}

    # Get distinct dates by manufacturer and model
    for manufacturer in manufacturers:
        for model in car_data[manufacturer]["models"]:
            dates = df[(df["manufacturer"] == manufacturer) & (df["model"] == model)][
                "date"
            ].unique()
            car_data[manufacturer][model] = {"dates": dates}

    return car_data


class PageFactory:
    def __init__(self):
        pass

    def create_page(self, db_handler: DynamoHandler):
        st.set_page_config(page_title="Home page", layout="wide")

        data = get_data()

        car_data = get_sidebar_filters(data)

        manufacturer = st.sidebar.selectbox(
            "Select Manufacturer", list(car_data.keys())
        )

        if manufacturer:
            model = st.sidebar.selectbox(
                "Select Model", car_data[manufacturer]["models"]
            )
        else:
            model = None

        if model:
            date = st.sidebar.selectbox(
                "Select Data Date", car_data[manufacturer][model]["dates"]
            )
        else:
            date = None

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
        data = data[(data["year"] >= year_range[0]) & (data["year"] <= year_range[1])]
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
            "Autos encontrados en US$", int(data[data["currency"] == "US$"].shape[0])
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
