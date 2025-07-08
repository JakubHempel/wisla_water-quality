import streamlit as st
import ee
from water_indexes import water_indexes
import datetime
from datetime import date

# Area of interest
aoi = ee.FeatureCollection("projects/jakub-hempel/assets/wisla-boundary-rzwg")

normalized_indexes = ['Turbidity']
dynamic_indexes = ['CDOM', 'DOC', 'Cyanobacteria', 'SABI', 'CGI']  # Add others if needed


def set_stretch_and_clip(image):
    # Set fixed min/max for normalized indexes
    for name in normalized_indexes:
        image = image.set(f"{name}_min", -1).set(f"{name}_max", 1)

    # Compute 5–95% percentile range for dynamic indexes
    for name in dynamic_indexes:
        percentiles = image.select(name).reduceRegion(
            reducer=ee.Reducer.percentile([5, 95]),
            geometry=aoi.geometry(),
            scale=10,
            bestEffort=True
        )
        image = image.set({
            f"{name}_min": percentiles.get(f"{name}_p5"),
            f"{name}_max": percentiles.get(f"{name}_p95")
        })

    # Clip to AOI after stats
    return image.clip(aoi)


# Cloud masking function
def mask_clouds(imagery):
    qa = imagery.select('QA60')
    cloud_mask = qa.bitwiseAnd(1 << 10).eq(0).And(qa.bitwiseAnd(1 << 11).eq(0))
    return imagery.updateMask(cloud_mask).copyProperties(imagery, imagery.propertyNames())


# Sentinel-2 images
@st.cache_resource
def get_s2_imagery():
    # Set date range: from March 1st of this year to today
    start_date = f"2025-03-01"
    end_date = f"2025-07-07"

    # Load and filter the Sentinel-2 collection
    s2_collection = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .sort('system:time_start')
    )

    # Apply cloud mask
    s2_masked = s2_collection.map(mask_clouds)

    # Create a list of distinct acquisition dates (server-side)
    date_list = ee.List(
        s2_masked.aggregate_array("system:time_start")
        .map(lambda t: ee.Date(t).format("YYYY-MM-dd"))
    ).distinct()

    # Function to compute median image per date
    def compute_median_by_date(date_str):
        date_obj = ee.Date(date_str)
        next_day = date_obj.advance(1, 'day')
        filtered = s2_masked.filterDate(date_obj, next_day)
        median_img = (
            filtered.median()
            .divide(10000)
            .set("date_acquired", date_str)
        )

        # Add water indexes
        index_img = water_indexes(median_img)

        # Select only the water index bands
        index_bands = ee.List(normalized_indexes + dynamic_indexes + ['B2', 'B3', 'B4'])
        return index_img.select(index_bands)

    # Map over dates to create an ImageCollection of per-date medians
    median_images_ic = ee.ImageCollection(date_list.map(compute_median_by_date))

    # Convert to dictionary: client-side with limited .getInfo() usage
    median_images_list = median_images_ic.toList(median_images_ic.size())
    dates = date_list.getInfo()

    # Create dictionary: {date: ee.Image}
    median_images_dict = {
        dates[i]: ee.Image(median_images_list.get(i)) for i in range(len(dates))
    }

    # Create new dictionary with processed images
    stretched_images_dict = {}

    for date, image in median_images_dict.items():
        stretched_images_dict[date] = set_stretch_and_clip(image)

    return {'dates': dates, 'layers': stretched_images_dict}


