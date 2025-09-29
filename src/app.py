# imports

import pandas as pd

import h3

import folium
import streamlit as st
from streamlit_folium import st_folium

# Data

df_gpx = pd.read_csv('data/gpx_treated_data.csv')


## Convert GPX track points to H3 indices
def add_h3_to_gpx_dataframe(df, resolution=9):
    """Add H3 index and boundaries to the GPX DataFrame"""
    h3_data = []
    for _, row in df.iterrows():
        h3_index = row['h3_index']
        boundaries = h3.cell_to_boundary(h3_index)
        h3_data.append({
            'h3_boundaries': boundaries
        })
    
    h3_df = pd.DataFrame(h3_data)
    return pd.concat([df, h3_df], axis=1)

## Add H3 data to the GPX DataFrame
df_to_map = add_h3_to_gpx_dataframe(df_gpx)

st.dataframe(df_to_map)

## Display map

m = folium.Map(zoom_start=15, tiles="Cartodb dark_matter")

# Add the H3 cells to the map
for _, row in df_to_map.iterrows():
    boundaries = row['h3_boundaries']

    # Convert tuple of tuples to list of [lat, lon] for folium
    locations = [[lat, lon] for lat, lon in boundaries]
    folium.Polygon(
        locations=locations,
        color='#EFBF04',
        weight=1,
        fill=True,
        fill_opacity=0.5,
        popup=f"H3 Index: {row['h3_index']}"
    ).add_to(m)

st_folium(m, width=800)
