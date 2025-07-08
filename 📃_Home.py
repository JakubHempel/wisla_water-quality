import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide", page_title="📃 Home | HydroPix 💧🛰️")

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

ee_authenticate(token_name="EARTHENGINE_TOKEN")


st.title("Welcome in HydroPix! 💧🛰️")

st.markdown("""
---
### 🚀 Suggested Actions to Explore:
""")

st.markdown("""
#### 📃 1. Start on the *Home* Page
- Get familiar with the **aim and scope** of the application.
- Learn about the use of **radar satellite data (Sentinel-1)**.
- Understand how **wetland areas are monitored** using **automated classification methods**.

---

#### 📊 2. Explore the *Data* Page
- **Sentinel-1 and Sentinel-2** satellite datasets used in the analysis.
- **Precipitation data** from meteorological stations.
- **Spatial and temporal scope** of the Area of Interest (AOI).

---

#### 🧠 3. Learn on the *Methodology* Page
- Overview of the **Otsu thresholding algorithm** for water detection.
- Understand the **calculation of wetland occurrence** and **probability index**.
- Technologies used: **Google Earth Engine, Python, geemap, FME**.

---

#### 🌊 4. Dive into the *Flood 2024 Analysis* Section
- 🛰️📡 *Sentinel-1*:
    - View **water detection results** from radar imagery before, during, and after the flood.
- 🛰️📷 *Sentinel-2*:
    - Explore **optical imagery** in **RGB** and **False Color** compositions.
    - **Compare water extent** across key flood dates.
- 🌍 *Spectral Indices – Water Quality*:
    - Browse **AWEI, CGI, CDOM, DOC** indices related to water quality.
    - Analyze changes across flood timelines.
- 💦 *Water Masks*:
    - Visualize **binary water masks** generated using **Otsu classification**.

---

#### 💦 5. Visit the *Water and Wetness Layer* Page
- Explore an **aggregated water occurrence map** based on multiple Sentinel-1 acquisitions (2018–2025).
- Identify:
    - Areas with **frequent wetness**.
    - **Temporary** and **permanent wetland** zones.

---

#### 💦 6. Analyze the *Water and Wetness Probability Index* Page
- Discover the **likelihood of water presence** at each pixel.
- Understand which areas are **consistently** or **occasionally wet** over time.

---

### 🧭 Navigation Tip
> **You can explore the pages in any order depending on your interest — from flood event case studies to long-term wetland monitoring.**

> 💡 **To begin, we recommend starting with the 📃 *Home* and 🧠 *Methodology* pages to better understand the analytical background.**

---

##### 🎉 Enjoy your exploration of HydroPix! 💦
""")
