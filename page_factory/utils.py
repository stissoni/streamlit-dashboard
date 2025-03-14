import streamlit as st


def set_sidebar_filters(df, page_type="home"):
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

    if page_type == "price_history":
        currency = st.sidebar.selectbox("Select Currency", ["$", "US$"])

        return manufacturer, model, currency
    elif page_type == "home":
        if model:
            date = st.sidebar.selectbox(
                "Select Data Date",
                car_data[manufacturer][model]["dates"],
            )
        else:
            date = None

        return manufacturer, model, date
    else:
        raise ValueError("Invalid page type")
