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

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((1, 1))

# SEE IF THERE'S A QUERY PARAM IN THE URL (e.g. ?pickup_hour=2)
# THIS ALLOWS YOU TO PASS A STATEFUL URL TO SOMEONE WITH A SPECIFIC HOUR SELECTED,
# E.G. https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main?pickup_hour=2
if not st.session_state.get("url_synced", False):
    try:
        State = st.experimental_get_query_params()["State"][0]
        st.session_state["State"] = State
        st.session_state["url_synced"] = True
    except KeyError:
        pass

# IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
def update_query_params():
    State_selected = st.session_state["State"]
    st.experimental_set_query_params(State=State_selected)

with st.sidebar.form(key="my_form"):
    State_selected = st.selectbox("Select State", options=all_states, key="State")

    pressed = st.form_submit_button("Build Migration Map")

if pressed:
    with row1_1:
        st.title("Starbucks Store Locator Dashboard")

    filterdata = filterdata(data, State_selected)
    with row1_2:
        st.write(
            """
        ##
        The dashboard shows the distribution of current Starbucks locations.
        By selecting the state on the left you can view the Starbucks store location in each state.
        """
        )

    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    row2_1, row2_2 = st.columns((1, 1))

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    midpoint = mpoint(filterdata["lon"],filterdata["lat"])
    allpoint = mpoint(data["lon"],data["lat"])

    with row2_1:
        st.write("**United States Data**")
        # map(data, allpoint[0], allpoint[1], 4)
        all_map(data,2)
    with row2_2:
        st.write(
            f"""**{State_selected}**"""
        )
        map(filterdata, midpoint[0], midpoint[1], 6)
