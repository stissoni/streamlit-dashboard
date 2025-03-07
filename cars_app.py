import streamlit as st


corolla_page = st.Page("corolla.py")
etios_page = st.Page("etios.py")
renegade_page = st.Page("renegade.py")

pg = st.navigation([corolla_page, etios_page, renegade_page])

pg.run()