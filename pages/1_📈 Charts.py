import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from stats import (
    get_sabi_stats, get_cgi_stats, get_cdom_stats,
    get_doc_stats, get_cyanobacteria_stats, get_turbidity_stats
)

st.set_page_config(page_title="Water Quality Indices | Wisła-WQ 💧", layout="wide")

tab1, tab2, tab3 = st.tabs(["📊 Water Index Medians Over Time", "📈 Monthly Median Trends", "🔗 Correlation Matrix"])

# Short and full names
index_funcs = {
    'SABI': get_sabi_stats,
    'CGI': get_cgi_stats,
    'CDOM': get_cdom_stats,
    'DOC': get_doc_stats,
    'Cyanobacteria': get_cyanobacteria_stats,
    'Turbidity': get_turbidity_stats,
}

full_names = {
    'SABI': '🦠 Surface Algal Bloom Index',
    'CGI': '🦠 Chlorophyll Green Index',
    'CDOM': '🦠 Colored Dissolved Organic Matter',
    'DOC': '🦠 Dissolved Organic Carbon',
    'Cyanobacteria': '🦠 Cyanobacteria',
    'Turbidity': '💦 Turbidity',
}

with st.spinner("Processing indices..."):
    all_data = {abbr: func() for abbr, func in index_funcs.items()}

with tab1:
    for index, get_func in index_funcs.items():
        st.markdown(f"### {full_names[index]}")
        with st.spinner(f"Generating line chart ..."):
            stats_df = get_func()
            col1, col2 = st.columns((3, 1))
            with col1:
                st.line_chart(stats_df)
            with col2:
                st.dataframe(stats_df)


def plot_line_with_labels(df, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['median'],
        mode='lines+markers+text',
        text=df['median'].round(2),
        textposition='top center',
        line=dict(width=2),
        marker=dict(size=7)
    ))
    fig.update_layout(
        height=400,
        title=dict(text=title, font=dict(size=22)),
        margin=dict(l=10, r=10, t=70, b=50),
        showlegend=False
    )
    return fig


with tab2:
    # Trend section
    cols = st.columns(2)
    for i, (abbr, df) in enumerate(all_data.items()):
        df.index = pd.to_datetime(df.index)
        monthly = df.resample("M").median().dropna()
        monthly.index = monthly.index.strftime("%b")
        with cols[i % 2]:
            st.plotly_chart(plot_line_with_labels(monthly, full_names[abbr]), use_container_width=True)

with tab3:
    # Correlation matrix with Streamlit DataFrame
    merged = pd.concat(
        [df.rename(columns={'median': abbr}) for abbr, df in all_data.items()],
        axis=1
    ).dropna()

    corr = merged.corr().round(2)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr_lower = corr.mask(mask)

    st.dataframe(
        corr_lower.style
        .background_gradient(cmap='coolwarm', axis=None)
        .format("{:.2f}")
    )
