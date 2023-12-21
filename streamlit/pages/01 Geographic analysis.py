import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# DATA IMPORTATION
    
usa_states = pd.read_csv("../files/data/usa_states.csv")
usa_cities = pd.read_csv("../files/data/usa_cities.csv")

clients = pd.read_csv("../files/data/usa_clients.csv", index_col=0)

usa_attractions = pd.read_csv("../files/data/usa_attractions.csv", index_col=0)
usa_attractions.dropna(subset=['new_categories'], inplace=True)
usa_attractions["n_reviews"].fillna(usa_attractions["n_reviews"].mean() ,inplace=True)
usa_attractions.rename(columns={'latitud': 'latitude'}, inplace=True)

hotels = pd.read_csv("../files/data/usa_hotels.csv", index_col=0)
hotels = pd.merge(hotels, usa_states[['state', 'state_id']], on='state', how="left")
hotels = pd.merge(hotels, usa_cities[['city', 'state_id', 'latitude', 'longitude', 'population']], on=['state_id', 'city'], how='left')


# GENERAL SETTINGS

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Geographic analysis",
    page_icon="🌐",
    )

color_palette = {
    'attractions_color': '#547980',
    'hotels_color': '#87C696',
    'cities_color': '#FFFFFF',
    }


# CREATE FILTERS

st.sidebar.markdown("### Filters")

all_regions = usa_attractions["region"].unique()
selected_regions = st.sidebar.multiselect('Regions:', all_regions, default=all_regions)
st.markdown("""
    <style>
        .custom-multiselect {
            color: red;
            /* Add more custom styles here */
        }
    </style>
""", unsafe_allow_html=True)

all_categories = usa_attractions['new_categories'].unique()
selected_attractions_categories = st.sidebar.multiselect('Attraction categories:', all_categories, default=all_categories)


# FILTRATE DATA

filtered_attractions = usa_attractions[(usa_attractions["new_categories"].isin(selected_attractions_categories) & (usa_attractions["region"].isin(selected_regions)))]

state_ids = filtered_attractions["state_id"].unique()
filtered_hotels = hotels[hotels["state_id"].isin(state_ids)]

hotel_count_by_city = filtered_hotels.groupby(['city', 'state']).size().reset_index(name='hotel_count')
hotel_count_by_city = pd.merge(hotel_count_by_city, usa_states[['state', 'state_id']], on='state', how="left")
hotel_count_by_city = pd.merge(hotel_count_by_city, usa_cities[['city', 'state_id', 'latitude', 'longitude', 'population']], on=['state_id', 'city'], how='left')
hotel_count_by_city = hotel_count_by_city.sort_values(by=['hotel_count'], ascending=False)


# VISUALIZATIONS

# Scatterplot map
mapscatter_cities = px.scatter_geo(usa_cities, lat="latitude", lon="longitude", size="population",
    color_discrete_sequence=['black'], title="Geographic distribution",
    width=1000, height=900, scope="usa")
mapscatter_cities.update_traces(marker=dict(line=dict(width=0)), opacity=0.25)
mapscatter_cities.update_layout(title=dict(text='Geographic distribution', font=dict(color='black')))
mapscatter_hotels = px.scatter_geo(hotel_count_by_city, lat="latitude", lon="longitude", size="hotel_count",
    color_discrete_sequence=[f"{color_palette['hotels_color']}"],
    width=1000, height=900, scope="usa")
mapscatter_hotels.update_traces(marker=dict(line=dict(width=0)))
mapscatter_attractions = px.scatter_geo(usa_attractions, lat="latitude", lon="longitude", size="n_reviews",
    color_discrete_sequence=[f"{color_palette['attractions_color']}"],
    width=1000, height=900, scope="usa")
mapscatter_attractions.update_traces(marker=dict(line=dict(width=0)))
geographic_analyysis_map = mapscatter_cities
for trace in mapscatter_hotels.data:
    geographic_analyysis_map.add_trace(trace)
for trace in mapscatter_attractions.data:
    geographic_analyysis_map.add_trace(trace)

# Attractions categories barplot
top_attractions = filtered_attractions['new_categories'].value_counts().nlargest(10)
bar_chart = px.bar(y=top_attractions.values, x=top_attractions.index,
    orientation='v', title="Top attractions:",
    color_discrete_sequence=[f"{color_palette['attractions_color']}"],
    width=300, height=400)
bar_chart.update_layout(margin=dict(b=1)) 

hotel_count_by_city_barchart = px.bar(x=hotel_count_by_city.head(10).city, y=hotel_count_by_city.head(10).hotel_count,
                    color_discrete_sequence=[f"{color_palette['hotels_color']}"],
                    height=400, width=300, title='Top cities with most hotels:')


# DIAGRAMATION

col1, col2 = st.columns((5, 2))
with col1:
    st.plotly_chart(geographic_analyysis_map, use_container_width=True)

with col2:
   
    st.plotly_chart(bar_chart, use_container_width=True)
    st.plotly_chart(hotel_count_by_city_barchart, use_container_width=True)