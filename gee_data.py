import ee
import geemap.foliumap as geemap
import streamlit as st
from water_indexes import water_indexes
from datetime import date


@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


ee_authenticate(token_name="EARTHENGINE_TOKEN")


# Area of interest
aoi = ee.FeatureCollection("projects/jakub-hempel/assets/water_welna")


@st.cache_resource(max_entries=1)
def get_s2_imagery(indexes=None):
    """
    Downloads and processes Sentinel-2 imagery with selected water indexes.
    Parameters:
        indexes: List of water index band names to compute (e.g., ['CDOM', 'SABI']).
                 If None, compute all available.
    Returns:
        A dict with imagery by date and list of available dates.
    """

    indexes = ['Turbidity', 'CDOM', 'DOC', 'Cyanobacteria', 'SABI', 'CGI']

    start_date = "2025-03-01"
    end_date = str(date.today())

    s2_collection = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .sort('system:time_start')
    )

    def mask_clouds(image):
        qa = image.select('QA60')
        cloud_mask = qa.bitwiseAnd(1 << 10).eq(0).And(qa.bitwiseAnd(1 << 11).eq(0))
        return image.updateMask(cloud_mask).copyProperties(image, image.propertyNames())

    s2_masked = s2_collection.map(mask_clouds)

    def compute_median_by_date(date_str):
        date_obj = ee.Date(date_str)
        filtered = s2_masked.filterDate(date_obj, date_obj.advance(1, 'day'))
        median_img = filtered.median().divide(10000).set("date", date_str)
        image_with_indexes = water_indexes(median_img, only=indexes).set("system:time_start", date_obj.millis())
        index_bands = image_with_indexes.bandNames().filter(ee.Filter.inList("item", indexes))
        return image_with_indexes.select(index_bands).clip(aoi)

    # Generate unique date strings
    date_list = ee.List(
        s2_masked.aggregate_array("system:time_start")
        .map(lambda t: ee.Date(t).format("YYYY-MM-dd"))
    ).distinct()

    # Map computation and collect images
    median_images_ic = ee.ImageCollection(date_list.map(compute_median_by_date))
    median_images_list = median_images_ic.toList(median_images_ic.size())
    dates = date_list.getInfo()

    median_images_dict = {
        dates[i]: ee.Image(median_images_list.get(i)) for i in range(len(dates))
    }

    return {"layers": median_images_dict, "dates": dates, "collection": median_images_ic}

