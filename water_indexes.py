import streamlit as st


def water_indexes(image):
    NDWI = False
    NDVI = False
    NDSI = False
    SABI = True
    CGI = True
    CDOM = True
    DOC = True
    Cya = True
    Turb = True
    AWEI = False

    if NDWI:
        ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
        image = image.addBands(ndwi)

    if NDVI:
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        image = image.addBands(ndvi)

    if NDSI:
        ndsi = image.normalizedDifference(['B11', 'B12']).rename('NDSI')
        image = image.addBands(ndsi)

    if SABI:
        sabi = image.expression('(NIR - RED) / (BLUE + GREEN)',
                                {'NIR': image.select('B8'),
                                 'RED': image.select('B4'),
                                 'BLUE': image.select('B2'),
                                 'GREEN': image.select('B3')}).rename('SABI')
        image = image.addBands(sabi)

    if CGI:
        cgi = image.expression('((SWIR / GREEN) - 1)',
                               {'SWIR': image.select('B9'), 'GREEN': image.select('B3')}).rename('CGI')
        image = image.addBands(cgi)

    if CDOM:
        cdom = image.expression('537 * exp(-2.93 * GREEN / RED)',
                                {'GREEN': image.select('B3'),
                                 'RED': image.select('B4')}).rename('CDOM')
        image = image.addBands(cdom)

    if DOC:
        doc = image.expression('432 * exp(-2.24 * GREEN / RED)',
                               {'GREEN': image.select('B3'),
                                'RED': image.select('B4')}).rename('DOC')
        image = image.addBands(doc)

    if Cya:
        cya = image.expression('115530.31 * (GREEN * RED / BLUE) ** 2.38',
                               {'RED': image.select('B4'),
                                'BLUE': image.select('B2'),
                                'GREEN': image.select('B3')}).rename('Cyanobacteria')
        image = image.addBands(cya)

    if Turb:
        turb = image.normalizedDifference(['B4', 'B3']).rename('Turbidity')
        image = image.addBands(turb)

    if AWEI:
        awei = image.expression('4*(GREEN - SWIR1) - (0.25*NIR + 2.75*SWIR2)',
                                {'GREEN': image.select('B3'),
                                 'NIR': image.select('B8'),
                                 'SWIR1': image.select('B11'),
                                 'SWIR2': image.select('B12')}).rename('AWEI')
        image = image.addBands(awei)

    return image
