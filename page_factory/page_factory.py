import pandas as pd
from .price_histogram import PriceHistogram
from .price_linechart import PriceLineChart
import streamlit as st


class PageFactory:

    def create_page(self, page_query):
        title = page_query.replace("-", " ").replace(".csv", "")
        st.set_page_config(page_title=title, layout="wide")

        path = page_query
        data = pd.read_csv("data/" + path)

        st.title(f"🚗 Análisis de {title}")

        # Set slider for car years
        min_year = data["year"].min()
        max_year = data["year"].max()

        st.sidebar.markdown("## Filtros")
        year_range = st.sidebar.slider(
            "Años de los autos",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
        )

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
        data = data[
            (data["kilometers"] >= kilometers_range[0])
            & (data["kilometers"] <= kilometers_range[1])
        ]

        columns = st.columns(5)

        columns[0].metric("Autos encontrados", data.shape[0])
        columns[1].metric("Autos encontrados $", data[data["currency"] == "$"].shape[0])
        columns[2].metric(
            "Precio promedio $",
            round(data[data["currency"] == "$"]["price"].mean(), 2),
        )
        columns[3].metric(
            "Autos encontrados en US$", data[data["currency"] == "US$"].shape[0]
        )
        columns[4].metric(
            "Precio promedio en US$",
            round(data[data["currency"] == "US$"]["price"].mean(), 2),
        )

        factory = PriceLineChart()
        fig = factory.plot(data, "$", "Precio promedio por año en $")

        st.plotly_chart(fig)

        factory = PriceLineChart()

        fig = factory.plot(data, "US$", "Precio promedio por año en US$")

        st.plotly_chart(fig)

        ars_data = data[data["currency"] == "$"]

        factory = PriceHistogram()
        fig = factory.plot(ars_data, "price", "Distribucion de precios en $")

        st.plotly_chart(fig)

        usd_data = data[data["currency"] == "US$"]

        fig = factory.plot(usd_data, "price", "Distribucion de precios en US$")

        st.plotly_chart(fig)

        fig = factory.plot(data, "kilometers", "Distribucion de kilometros")

        st.plotly_chart(fig)

        # Clean year outliers
        data = data[(data["year"] > 1900) & (data["year"] < 2026)]

        fig = factory.plot(data, "year", "Distribucion de años", nbins=20)

        st.plotly_chart(fig)
