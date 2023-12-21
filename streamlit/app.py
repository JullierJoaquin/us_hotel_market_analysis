import streamlit as st
import numpy as np
import pandas as pd
import psycopg2

import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

# GENERAL SETTINGS

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Tu Aplicación",
    page_icon=":chart_with_upwards_trend:",
    )

color_palette = {
    'Ecstasy': '#FB6D10',
    'Pomegranate': '#EB3E1B',
    'claret': '#86112E',
    }


# Mostrar la imagen con tamaño y alineación personalizados
st.markdown("## US hotel market analysis:")
st.markdown("***") # Línea de división     
st.markdown("Description...")

st.markdown("usa_states")
usa_states = pd.read_csv("../files/data/usa_states.csv")
usa_states

st.markdown("usa_cities")
usa_cities = pd.read_csv("../files/data/usa_cities.csv")
usa_cities

st.markdown("clients")
clients = pd.read_csv("../files/data/usa_clients.csv", index_col=0)
clients

st.markdown("usa_attractions")
usa_attractions = pd.read_csv("../files/data/usa_attractions.csv", index_col=0)
usa_attractions["n_reviews"].fillna(usa_attractions["n_reviews"].mean() ,inplace=True)
usa_attractions

st.markdown("hotels")
hotels = pd.read_csv("../files/data/usa_hotels.csv", index_col=0)
hotels = pd.merge(hotels, usa_states[['state', 'state_id']], on='state', how="left")
hotels = pd.merge(hotels, usa_cities[['city', 'state_id', 'latitude', 'longitude', 'population']], on=['state_id', 'city'], how='left')
hotels