import streamlit as st


def set_sidebar_filters(df, page_type="home"):
    st.sidebar.markdown("## Filtros")
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
            dates = df[
                (df["manufacturer"] == manufacturer) & (df["model"] == model)
            ]["date"].unique()
            car_data[manufacturer][model] = {"dates": dates}

    manufacturer = st.sidebar.selectbox(
        "Select Manufacturer", list(car_data.keys())
    )

    if manufacturer:
        model = st.sidebar.selectbox(
            "Select Model", car_data[manufacturer]["models"]
        )
    else:
        model = None

    currency = st.sidebar.selectbox("Select Currency", ["$", "US$"])

    if page_type == "home":
        date = st.sidebar.selectbox(
            "Select Data Date",
            car_data[manufacturer][model]["dates"],
        )
    else:
        date = None

    # Set slider for car years
    min_year = df[(df["model"] == model) & (df["currency"] == currency)][
        "year"
    ].min()
    max_year = df[(df["model"] == model) & (df["currency"] == currency)][
        "year"
    ].max()

    year_range = st.sidebar.slider(
        "Años de los autos",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    # Set slider for car kilometers
    min_kilometers = df["kilometers"].min()
    max_kilometers = df["kilometers"].max()

    kilometers_range = st.sidebar.slider(
        "Kilometros de los autos",
        min_value=min_kilometers,
        max_value=max_kilometers,
        value=(min_kilometers, max_kilometers),
    )

    return manufacturer, model, currency, year_range, kilometers_range, date
