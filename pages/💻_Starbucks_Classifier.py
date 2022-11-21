import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import leafmap.foliumap as leafmap

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Starbucks Store Classifier Dashboard", page_icon=":coffee:")

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    data = pd.read_csv(
        "county_clustering.csv",
        nrows=100000,
        names=[
            "State",
            "Latitude",
            "Longitude",
            "Cluster_Groups",
            "Cluster_Names",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0,2,3,4,5],
    )

    return data

# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.experimental_memo
def filterdata(df, group_selected):
    df_tran = df.dropna(subset=['Longitude'])
    return df_tran[df_tran['Cluster_Names'] == selected_cluster_names]


# STREAMLIT APP LAYOUT
data = load_data()
all_clusters = data["Cluster_Names"].unique()

def update_query_params():
    selected_cluster_names = st.session_state["Cluster_Names"]
    st.experimental_set_query_params(Cluster_Names=selected_cluster_names)

with st.sidebar.form(key="my_form"):
    selected_cluster_names = st.selectbox("Select Cluster Group", options=all_clusters, key="cluster")

    pressed = st.form_submit_button("Build Classifier Map")

if pressed:
    row1_1, row1_2 = st.columns((1, 1))
    with row1_1:
        st.title("Starbucks Store Clusters Dashboard")

    filterdata = filterdata(data, selected_cluster_names)
    # with row1_2:
    #     st.write(
    #         """
    #     ##
    #     The dashboard shows the distribution of current Starbucks locations.
    #     By selecting the state on the left you can view the Starbucks store location in each state.
    #     """
    #     )
    st.write(
        f"""The following map shows all clusters distribution:"""
    )
    m = leafmap.Map(center=[40, -100], zoom=4)
    regions = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson'

    m.add_geojson(regions, layer_name='US Regions')
    m.add_points_from_xy(
        data,
        x="Longitude",
        y="Latitude",
        color_column='Cluster_Names',
        layer_name='Marker Cluster',
        icon_colors=['white'],
        icon_names=['gear', 'map', 'leaf', 'globe'],
        add_legend=True,
    )
    m.to_streamlit(height=500)

    st.write(
        f"""The following map shows **{selected_cluster_names}** distribution:"""
    )
    m2 = leafmap.Map(center=[40, -100], zoom=4)
    regions = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson'

    m2.add_geojson(regions, layer_name='US Regions')
    m2.add_points_from_xy(
        filterdata,
        x="Longitude",
        y="Latitude",
        # color_column='Cluster_Names',
        # layer_name='Marker Cluster',
        # icon_colors=['white'],
        # icon_names=['gear', 'map', 'leaf', 'globe'],
        # add_legend=True,
    )
    m2.to_streamlit(height=500)