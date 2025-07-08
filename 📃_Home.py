import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide", page_title="📃 Home | Wisła-WQ 💧")

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

ee_authenticate(token_name="EARTHENGINE_TOKEN")


st.title("Welcome in Wisła Water Quality App! 💧")
