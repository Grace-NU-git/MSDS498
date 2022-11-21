import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Starbucks Store Locator Dashboard", page_icon=":coffee:")

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    data = pd.read_csv(
        "Final_Counties_Starbucks_dataset.csv",
        nrows=100000,
        names=[
            "State",
            "lon",
            "lat",
            "Starbucks_INDICATOR",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[2,43,44,45],
    )

    return data


# FUNCTION FOR AIRPORT MAPS
def map(data, lon, lat, zoom):
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=zoom,
                pitch=50,
    ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data,
                    get_position='[lon, lat]',
                    auto_highlight=True,
                    get_color='[200, 30, 0, 160]',
                    get_radius=1000,
                    pickable=True
                ),
                pdk.Layer(
                    'HexagonLayer',  # `type` positional argument is here
                    data=data,
                    get_position=['lon', 'lat'],
                    auto_highlight=True,
                    elevation_scale=50,
                    pickable=True,
                    elevation_range=[0, 3000],
                    extruded=True,
                    coverage=1)
            ],
        )
    )

def all_map(data,zoom):
    st.map(data,zoom)

# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.experimental_memo
def filterdata(df, State_selected):
    df_tran = df.dropna(subset=['lon'])
    return df_tran[df_tran['State'] == State_selected]


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lon, lat):
    return (np.average(lon), np.average(lat))

# STREAMLIT APP LAYOUT
data_raw = load_data()
data = data_raw[data_raw['Starbucks_INDICATOR'] == 1]
all_states = data["State"].unique()

def update_query_params():
    State_selected = st.session_state["State"]
    st.experimental_set_query_params(State=State_selected)

with st.sidebar.form(key="my_form"):
    selectbox_state = st.selectbox("Select State", options=all_states, key="State")
    numberinput_threshold = st.number_input(
        """Set top N Migration per state""",
        value=3,
        min_value=1,
        max_value=25,
        step=1,
        format="%i",
    )

    st.markdown(
        '<p class="small-font">Results Limited to top 5 per State in overall US</p>',
        unsafe_allow_html=True,
    )
    pressed = st.form_submit_button("Build Migration Map")

expander = st.sidebar.expander("What is this?")
expander.write(
    """
This app allows users to view migration between states from 2018-2019.
Overall US plots all states with substantial migration-based relationships with other states.
Any other option plots only migration from or to a given state. This map will be updated
to show migration between 2019 and 2020 once new census data comes out.
Incoming: Shows for a given state, the percent of their **total inbound migration from** another state.
Outgoing: Shows for a given state, the percent of their **total outbound migration to** another state.
"""
)