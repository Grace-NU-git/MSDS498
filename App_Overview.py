import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide", page_title="Starbucks_App_Overview", page_icon=":coffee:")

st.sidebar.title("About")
st.sidebar.info(
    """
    Web App URL: <https://team54-starbucks.streamlit.app/>
    
    GitHub repository: <https://github.com/Grace-NU-git/MSDS498>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Team 54 Research Group
    - Donjo Lau
    - Maximilian Dabek
    - Mengyuan Han
    - Ruben Fontes
    - Zahid Khalil
    """
)

# Customize page title
st.title("Expanding Starbucks Locations in the U.S.")

st.markdown(
    """
The Starbucks store locator web application is created to integrate location analytics functionalities, enrich search functionalities on websites and get detailed data under each scenarios based on filter selection. 
    """
)

m = leafmap.Map(center=[40, -100], zoom=4 , minimap_control=True)
regions = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson'
m.add_geojson(regions, layer_name='US Regions')
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)