import streamlit as st
from stats import (
    get_sabi_stats, get_cgi_stats, get_cdom_stats,
    get_doc_stats, get_cyanobacteria_stats, get_turbidity_stats
)

st.subheader("📊 Water Index Medians Over Time")

index_funcs = {
    'SABI': get_sabi_stats,
    'CGI': get_cgi_stats,
    'CDOM': get_cdom_stats,
    'DOC': get_doc_stats,
    'Cyanobacteria': get_cyanobacteria_stats,
    'Turbidity': get_turbidity_stats,
}

index_labels = {
    'SABI': 'Surface Algal Bloom Index',
    'CGI': 'Chlorophyll Green Index',
    'CDOM': 'Colored Dissolved Organic Matter',
    'DOC': 'Dissolved Organic Carbon',
    'Cyanobacteria': 'Cyanobacteria',
    'Turbidity': 'Turbidity'
}

for index, get_func in index_funcs.items():
    st.markdown(f"### {index_labels[index]}")
    with st.spinner(f"Generating line chart ..."):
        stats_df = get_func()
        col1, col2 = st.columns((3, 1))
        with col1:
            st.line_chart(stats_df)
        with col2:
            st.dataframe(stats_df)
