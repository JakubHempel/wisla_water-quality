import streamlit as st
from create_map import show_map
from gee_data import get_s2_imagery
from stats import get_images_stats
from water_indexes import indices_description

st.markdown("""
<style>
.index-font-1 {
    font-size: 17px;
    color: #20B2AA;
}
.index-font-2 {
    font-size: 17px;
    color: #B6D79A;    
}
.align-text {
    text-align: justify;
}
li {
    color: lightgray;
}
</style>
""", unsafe_allow_html=True)


# Cache imagery and stats
@st.cache_data
def get_imagery_cache():
    return get_s2_imagery()


@st.cache_data
def get_stats_cache():
    return get_images_stats()


# Load imagery
temp = get_imagery_cache()
s2_imagery = temp['layers']
dates = temp['dates']

with st.sidebar.container():
    st.markdown("### 🗓️ Available Image Dates")

    st.markdown(
        """
        <div style='
            height: 250px;
            overflow-y: auto;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 10px 15px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        '>
        <ul style='padding-left: 18px; margin: 0; list-style-type: disc; color: #ffffffd9;'>
        """ +
        "\n".join([f"<li>{date}</li>" for date in dates]) +
        """
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


# App title
st.subheader("💦 Wisła Water Quality Indexes")

# Define water indexes
tab_names = {
    "🦠 Surface Algal Bloom Index": "SABI",
    "🦠 Chlorophyll Green Index": "CGI",
    "🦠 Colored Dissolved Organic Matter": "CDOM",
    "🦠 Dissolved Organic Carbon": "DOC",
    "🦠 Cyanobacteria": "Cyanobacteria",
    "💦 Turbidity": "Turbidity"
}

# Selector container in a box-like UI
with st.container():
    with st.expander("*Selectors ✅*", expanded=True):
        selected_tab = st.segmented_control(
            "**Select water indexes**",
            tab_names.keys(),
            selection_mode="single",
            default="🦠 Surface Algal Bloom Index",
            key="index_selector"
        )

        selected_index = tab_names[selected_tab]

        # Unique session key per index
        date_key = f"{selected_index}_date"
        if date_key not in st.session_state:
            st.session_state[date_key] = dates[-1]

        widget = st.empty()
        col1, col2, col3 = st.columns((1, 9, 0.8))

        with col1:
            if st.button("Previous layer", key=f"{selected_index}_prev", type="primary"):
                idx = dates.index(st.session_state[date_key])
                st.session_state[date_key] = dates[idx - 1] if idx > 0 else dates[-1]

        with col3:
            if st.button("Next layer", key=f"{selected_index}_next", type="primary"):
                idx = dates.index(st.session_state[date_key])
                st.session_state[date_key] = dates[(idx + 1) % len(dates)]

        # Capture selected date before rendering
        current_date = widget.select_slider(
            label="**Choose imagery date**",
            options=dates,
            value=st.session_state[date_key],
            key=f"{selected_index}_slider"
        )

        # Lock value
        st.session_state[date_key] = current_date

# Unified container for description + map
content_container = st.container()

with content_container:
    map1, map2, map3 = st.columns([1, 0.05, 1.95])

    with map1:
        desc = indices_description[selected_index]
        st.subheader(desc["name"])
        st.info(desc["description"])
        st.latex(desc["formula"])
        st.divider()
        st.markdown(desc["ref"], unsafe_allow_html=True)

    with map3:
        st.markdown("")
        with st.spinner("Wait for the map ..."):
            st.markdown(
                f"<div style='text-align: left; font-size: 0.95em; color: gray;'>"
                f"🛰️📆 Sentinel-2 Imagery Date: <b>{current_date}</b></div>",
                unsafe_allow_html=True
            )
            try:
                show_map(
                    s2_imagery[current_date],
                    current_date,
                    selected_index
                )
            except Exception as e:
                st.error(f"Map display error: {e}")
