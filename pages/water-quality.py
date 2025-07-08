import streamlit as st

from create_map import show_map
from gee_data import get_s2_imagery


@st.cache_data
def get_imagery_cache():
    return get_s2_imagery()


s2_imagery = get_imagery_cache()['layers']
dates = get_imagery_cache()['dates']

st.subheader("💦 Wisła Water Quality Indexes")
tab1, tab2 = st.tabs(["🗺️ Map", "📈 Chart"])

with tab1:
    if not "layer" in st.session_state:
        st.session_state["layer"] = dates[-1]

    widget = st.empty()
    col1, col2, col3 = st.columns((1, 9, 0.8))
    with col1:
        if st.button("Previous layer", type="primary"):
            if st.session_state.layer == dates[0]:
                st.session_state["layer"] = dates[-1]
            else:
                st.session_state["layer"] = dates[dates.index(st.session_state.layer) - 1]
    with col3:
        if st.button("Next layer", type="primary"):
            if st.session_state.layer == dates[-1]:
                st.session_state["layer"] = dates[0]
            else:
                st.session_state["layer"] = dates[dates.index(st.session_state.layer) + 1]

    try:
        st.session_state["layer"] = widget.select_slider(
            label="Choose imagery date",
            options=dates,
            value=st.session_state.layer,
        )
    except:
        st.session_state["layer"] = dates[-1]

    with st.spinner("Wait for the map ..."):
        try:
            show_map(
                s2_imagery[st.session_state.layer],
                st.session_state.layer,
                'CDOM'
            )
        except:
            show_map(
                s2_imagery[dates[-1]],
                dates[-1],
                'CDOM',
            )
