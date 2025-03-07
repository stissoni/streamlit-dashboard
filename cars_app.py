import streamlit as st


corolla_page = st.Page("corolla.py")
etios_page = st.Page("etios.py")
renegade_page = st.Page("renegade.py")
a1_page = st.Page("a1.py")
a3_page = st.Page("a3.py")
focus_page = st.Page("focus.py")
compass_page = st.Page("compass.py")
cruze_page = st.Page("cruze.py")
mondeo_page = st.Page("mondeo.py")

pg = st.navigation(
    [
        corolla_page,
        etios_page,
        renegade_page,
        compass_page,
        a1_page,
        a3_page,
        focus_page,
        mondeo_page,
        cruze_page,
    ]
)

pg.run()
