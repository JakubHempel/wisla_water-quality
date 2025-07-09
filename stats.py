import streamlit as st
import ee
from gee_data import aoi
import pandas as pd


def get_median_values(image, index):
    value = image.select(index).reduceRegion(reducer=ee.Reducer.median(), geometry=aoi, scale=10, bestEffort=True).get(
        index)
    return image.set('date', image.get('date_acquired')).set(index, value)


def get_median_stats(image_collection, index):
    valuesS2 = image_collection.select(index)
    chart_dataS2 = valuesS2.reduceColumns(
        reducer=ee.Reducer.toList(2),
        selectors=['date_acquired', index]
    ).getInfo()

    datesS2 = [item[0] for item in chart_dataS2['list']]
    index_valuesS2 = [round(item[1], 2) for item in chart_dataS2['list']]

    return {'dates': datesS2, 'medians': index_valuesS2}


def stats_imagery(ic, index_name):
    values = ic.map(lambda img: get_median_values(img, index_name))
    medians = get_median_stats(values, index_name)

    return medians


@st.cache_data
def get_images_stats():
    stats = {'Turbidity': {'2025-03-17': {'median': 0.04},
                      '2025-03-19': {'median': 0.1},
                      '2025-03-22': {'median': 0.06},
                      '2025-03-26': {'median': 0.02},
                      '2025-04-03': {'median': 0.03},
                      '2025-04-13': {'median': 0.01},
                      '2025-04-16': {'median': -0.02},
                      '2025-04-23': {'median': -0.1},
                      '2025-04-26': {'median': -0.17},
                      '2025-04-28': {'median': -0.14},
                      '2025-05-03': {'median': -0.13},
                      '2025-06-10': {'median': -0.24},
                      '2025-06-12': {'median': -0.21},
                      '2025-06-14': {'median': -0.12},
                      '2025-06-15': {'median': -0.21},
                      '2025-06-22': {'median': -0.14},
                      '2025-06-30': {'median': -0.07},
                      '2025-07-02': {'median': -0.04},
                      '2025-07-05': {'median': -0.03}},
            'CDOM': {'2025-03-17': {'median': 36.45},
                      '2025-03-19': {'median': 47.77},
                      '2025-03-22': {'median': 41.25},
                      '2025-03-26': {'median': 32.24},
                      '2025-04-03': {'median': 34.21},
                      '2025-04-13': {'median': 31.2},
                      '2025-04-16': {'median': 25.18},
                      '2025-04-23': {'median': 15.24},
                      '2025-04-26': {'median': 8.25},
                      '2025-04-28': {'median': 10.67},
                      '2025-05-03': {'median': 12.26},
                      '2025-06-10': {'median': 4.76},
                      '2025-06-12': {'median': 6.26},
                      '2025-06-14': {'median': 13.23},
                      '2025-06-15': {'median': 6.25},
                      '2025-06-22': {'median': 11.2},
                      '2025-06-30': {'median': 18.27},
                      '2025-07-02': {'median': 23.21},
                      '2025-07-05': {'median': 24.71}},
            'DOC': {'2025-03-17': {'median': 55.52},
                    '2025-03-19': {'median': 67.53},
                    '2025-03-22': {'median': 60.76},
                    '2025-03-26': {'median': 50.24},
                    '2025-04-03': {'median': 52.34},
                    '2025-04-13': {'median': 48.82},
                    '2025-04-16': {'median': 41.67},
                    '2025-04-23': {'median': 28.18},
                    '2025-04-26': {'median': 17.67},
                    '2025-04-28': {'median': 21.72},
                    '2025-05-03': {'median': 24.22},
                    '2025-06-10': {'median': 11.21},
                    '2025-06-12': {'median': 14.24},
                    '2025-06-14': {'median': 25.2},
                    '2025-06-15': {'median': 13.75},
                    '2025-06-22': {'median': 22.23},
                    '2025-06-30': {'median': 32.69},
                    '2025-07-02': {'median': 38.77},
                    '2025-07-05': {'median': 40.73}},
            'Cyanobacteria': {'2025-03-17': {'median': 223.87},
                    '2025-03-19': {'median': 813.52},
                    '2025-03-22': {'median': 653.83},
                    '2025-03-26': {'median': 656.1},
                    '2025-04-03': {'median': 751.2},
                    '2025-04-13': {'median': 861.99},
                    '2025-04-16': {'median': 529.52},
                    '2025-04-23': {'median': 540.25},
                    '2025-04-26': {'median': 297.0},
                    '2025-04-28': {'median': 414.2},
                    '2025-05-03': {'median': 671.26},
                    '2025-06-10': {'median': 237.01},
                    '2025-06-12': {'median': 366.23},
                    '2025-06-14': {'median': 829.47},
                    '2025-06-15': {'median': 290.5},
                    '2025-06-22': {'median': 479.31},
                    '2025-06-30': {'median': 479.1},
                    '2025-07-02': {'median': 985.67},
                    '2025-07-05': {'median': 860.23}},
            'SABI': {'2025-03-17': {'median': 0.84},
                     '2025-03-19': {'median': 1.08},
                     '2025-03-22': {'median': 0.85},
                     '2025-03-26': {'median': 0.85},
                     '2025-04-03': {'median': 1.24},
                     '2025-04-13': {'median': 1.33},
                     '2025-04-16': {'median': 1.74},
                     '2025-04-23': {'median': 2.2},
                     '2025-04-26': {'median': 2.85},
                     '2025-04-28': {'median': 2.72},
                     '2025-05-03': {'median': 2.26},
                     '2025-06-10': {'median': 2.99},
                     '2025-06-12': {'median': 3.01},
                     '2025-06-14': {'median': 1.71},
                     '2025-06-15': {'median': 3.29},
                     '2025-06-22': {'median': 2.49},
                     '2025-06-30': {'median': 2.11},
                     '2025-07-02': {'median': 1.89},
                     '2025-07-05': {'median': 1.86}},
            'CGI': {'2025-03-17': {'median': 1.41},
                    '2025-03-19': {'median': 1.92},
                    '2025-03-22': {'median': 1.73},
                    '2025-03-26': {'median': 1.68},
                    '2025-04-03': {'median': 2.24},
                    '2025-04-13': {'median': 2.33},
                    '2025-04-16': {'median': 2.91},
                    '2025-04-23': {'median': 3.41},
                    '2025-04-26': {'median': 4.03},
                    '2025-04-28': {'median': 3.85},
                    '2025-05-03': {'median': 3.41},
                    '2025-06-10': {'median': 4.47},
                    '2025-06-12': {'median': 4.41},
                    '2025-06-14': {'median': 2.7},
                    '2025-06-15': {'median': 4.72},
                    '2025-06-22': {'median': 3.91},
                    '2025-06-30': {'median': 3.47},
                    '2025-07-02': {'median': 3.16},
                    '2025-07-05': {'median': 3.09}}}

    chart_data = {}

    for key, value in stats.items():
        df = pd.DataFrame.from_dict(value).transpose()
        df = df[["median"]]
        chart_data[key] = df

    return chart_data
