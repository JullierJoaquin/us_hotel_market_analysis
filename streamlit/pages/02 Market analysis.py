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

usa_states = pd.read_csv("../files/data/usa_states.csv")
usa_cities = pd.read_csv("../files/data/usa_cities.csv")
clients = pd.read_csv("../files/data/usa_clients.csv", index_col=0)
california_hotels = pd.read_csv("../files/data/booking/california_hotels.csv", index_col=0)
matrix = pd.read_csv("../files/data/booking/california_hotels_similarity_matrix.csv", index_col=0)
california_hotels = california_hotels[california_hotels["avg_score"] > 10]

# GENERAL SETTINGS

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Geographic analysis",
    page_icon="🌐",
    )

color_palette = {
    'main_color': '#547980',
    'secondary_color': '#87C696',
    'white': '#FFFFFF',
    }


# CREATE FILTERS

selected_state = st.sidebar.selectbox('State', ["California"])
california = usa_states[usa_states["state_id"] == "CA"]

selected_client = st.sidebar.selectbox('Client hotel', california_hotels['name'].unique())

filtered_hotel = california_hotels.loc[california_hotels['name'] == selected_client]

#california_hotels['similarity'] = matrix[f"{filtered_hotel.index[0]}"]
#california_hotels = california_hotels.sort_values(by='similarity', ascending=False)



# VISUALZIATIONS

import ast
from collections import Counter
df_copy = california_hotels.copy()
df_copy['attributes'] = df_copy['attributes'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
all_attributes = [attribute for sublist in df_copy['attributes'] for attribute in sublist]
attribute_counts = Counter(all_attributes)
df_attribute_counts = pd.DataFrame(list(attribute_counts.items()), columns=['Attribute', 'Count'])
df_attribute_counts = df_attribute_counts.sort_values(by='Count', ascending=False)
cat_count = px.bar(df_attribute_counts.head(10), x='Attribute', y='Count',
             title='Atributos populares',
             labels={'Count': 'Cantidad de Hoteles'},
             template='plotly_white')
cat_count.update_xaxes(showticklabels=False)

# Plot the 3D scatter plot with color mapping
color_map = {True: color_palette['main_color'], False: color_palette['secondary_color']}
california_hotels['top_100'] = california_hotels.index.isin(california_hotels.head(100).index) # Define color mapping
scatter = px.scatter_3d(california_hotels, x='price', y='stars', z="avg_score",
                    color="top_100", color_discrete_map=color_map)
scatter.update_layout(scene=dict(xaxis=dict(autorange="reversed")))
scatter.update_traces(marker=dict(size=3, sizemode='diameter'))
scatter.update_traces(marker=dict(line=dict(width=0)), opacity=0.75)
scatter.update_layout(width=1000, height=1000, margin=dict(t=5))  # Adjust the top margin
scatter.update(layout_coloraxis_showscale=False)
















score_columns = ['Personal', 'Instalaciones y servicios', 'Limpieza', 'Confort', 'Relación calidad-precio', 'Ubicación', 'WiFi Gratis']
hotel_data = california_hotels[california_hotels['name'] == selected_client][score_columns].transpose()
hotel_data.columns = ['Hotel Score']
hotel_data['Categoria'] = hotel_data.index

state_avg_scores = california_hotels[score_columns].mean().reset_index()
state_avg_scores.columns = ['Categoria', 'State Average Score']

combined_data = pd.merge(hotel_data, state_avg_scores, on='Categoria')
score_compare = px.bar(combined_data, x='Categoria', y=['Hotel Score', 'State Average Score'],
             labels={'value': 'Puntuación', 'variable': 'Categoría'},
             title=f'Comparación:',
             height=500,
             template='plotly_white',
             barmode='group')  # Utilizar 'group' para agrupar las barras
score_compare.update_xaxes(showticklabels=False)
score_compare.update_layout(showlegend=False)






default_center = {"lat": 36.7783, "lon": -119.4179}  # Example center for California
california_bbox = {"lon_min": -125, "lon_max": -114.13, "lat_min": 30, "lat_max": 42.0,}

cities_map = px.scatter_geo(
    california_hotels, lat="latitude", lon="longitude", #color="top_100",
    color_discrete_map={False: color_palette['secondary_color'], True: color_palette['main_color']},
    width=600, height=500,
    scope="usa", center=default_center, title='California')
cities_map.update_traces( marker=dict(line=dict(width=0)), opacity=1)


cities_map.update_geos(
    center_lon=default_center["lon"],
    center_lat=default_center["lat"],
    lonaxis_range=[california_bbox["lon_min"], california_bbox["lon_max"]],
    lataxis_range=[california_bbox["lat_min"], california_bbox["lat_max"]],)












# DIAGRAMTION

col1, col2= st.columns((2, 5))
with col1:
    st.plotly_chart(cities_map, use_container_width=True)

with col2:


    st.plotly_chart(scatter, use_container_width=True)




