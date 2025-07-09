import streamlit as st
from stats import get_images_stats


@st.cache_data
def get_stats_cache():
    return get_images_stats()


st.subheader("Water Index Medians Over Time")

stats = get_stats_cache()  # This should return the nested dictionary
all_indexes = ['SABI', 'CGI', 'CDOM', 'DOC', 'Cyanobacteria', 'Turbidity']
indexes_fullname = ['Surface Algal Bloom Index', 'Chlorophyll Green Index',
                    'Colored Dissolved Organic Matter', 'Dissolved Organic Carbon', '', '']

for index, fullname in zip(all_indexes, indexes_fullname):
    if index not in ('Cyanobacteria', 'Turbidity'):
        st.markdown(f"### {index} - {fullname}")
    else:
        st.markdown(f"### {index}")

    # Extract data for plotting
    data = stats[index]

    col1, col2 = st.columns((3, 1))

    with col1:
        # Create line chart
        st.line_chart(data)

    with col2:
        st.write(data)
