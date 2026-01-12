
import streamlit as st

# Entry Point for the Application
# Uses st.navigation to manage pages and sidebar titles

st.set_page_config(page_title="AI News Intelligence", layout="wide")

pg = st.navigation([
    st.Page("dashboard.py", title="News Dashboard"),
    st.Page("pages/1_Analytics.py", title="Analytics"),
])

pg.run()
