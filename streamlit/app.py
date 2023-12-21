import streamlit as st

import os
import numpy as np
import pandas as pd

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

current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, "usa_states.csv")
if os.path.exists(file_path):
    usa_states = pd.read_csv(file_path)
    st.dataframe(usa_states)
else:
    st.error(f"El archivo {file_path} no se pudo encontrar.")
st.dataframe(usa_states)

st.markdown("usa_cities")
usa_cities = pd.read_csv("usa_cities.csv")
usa_cities

st.markdown("clients")
clients = pd.read_csv("usa_clients.csv", index_col=0)
clients

st.markdown("usa_attractions")
usa_attractions = pd.read_csv("usa_attractions.csv", index_col=0)
usa_attractions["n_reviews"].fillna(usa_attractions["n_reviews"].mean() ,inplace=True)
usa_attractions

st.markdown("hotels")
hotels = pd.read_csv("usa_hotels.csv", index_col=0)
hotels = pd.merge(hotels, usa_states[['state', 'state_id']], on='state', how="left")
hotels = pd.merge(hotels, usa_cities[['city', 'state_id', 'latitude', 'longitude', 'population']], on=['state_id', 'city'], how='left')
hotels