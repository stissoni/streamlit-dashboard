import streamlit as st


corolla_page = st.Page("corolla.py")
etios_page = st.Page("etios.py")
renegade_page = st.Page("renegade.py")
a1_page = st.Page("a1.py")
a3_page = st.Page("a3.py")
focus_page = st.Page("focus.py")

pg = st.navigation(
    [corolla_page, etios_page, renegade_page, a1_page, a3_page, focus_page]
)

pg.run()
