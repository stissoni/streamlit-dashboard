import streamlit as st
from page_factory.page_factory import PageFactory


def corolla():
    path = "Toyota-Corolla.csv"

    factory = PageFactory()
    factory.create_page(path)


def etios():
    path = "Toyota-Etios.csv"

    factory = PageFactory()
    factory.create_page(path)


def renegade():
    path = "Jeep-Renegade.csv"

    factory = PageFactory()
    factory.create_page(path)


def a1():
    path = "Audi-A1.csv"

    factory = PageFactory()
    factory.create_page(path)


def a3():
    path = "Audi-A3.csv"

    factory = PageFactory()
    factory.create_page(path)


def focus():
    path = "Ford-Focus.csv"

    factory = PageFactory()
    factory.create_page(path)


def compass():
    path = "Jeep-Compass.csv"

    factory = PageFactory()
    factory.create_page(path)


def cruze():
    path = "Chevrolet-Cruze.csv"

    factory = PageFactory()
    factory.create_page(path)


def mondeo():
    path = "Ford-Mondeo.csv"

    factory = PageFactory()
    factory.create_page(path)


corolla_page = st.Page(corolla, title="Toyota Corolla", icon="🇯🇵")
etios_page = st.Page(etios, title="Toyota Etios", icon="🇯🇵")
a1_page = st.Page(a1, title="Audi A1", icon="🇩🇪")
a3_page = st.Page(a3, title="Audi A3", icon="🇩🇪")
renegade_page = st.Page(renegade, title="Jeep Renegade", icon="🇺🇸")
compass_page = st.Page(compass, title="Jeep Compass", icon="🇺🇸")
focus_page = st.Page(focus, title="Ford Focus", icon="🇺🇸")
mondeo_page = st.Page(mondeo, title="Ford Mondeo", icon="🇺🇸")
cruze_page = st.Page(cruze, title="Chevrolet Cruze", icon="🇺🇸")

pg = st.navigation(
    [
        corolla_page,
        etios_page,
        a1_page,
        a3_page,
        renegade_page,
        compass_page,
        focus_page,
        mondeo_page,
        cruze_page,
    ]
)

pg.run()
