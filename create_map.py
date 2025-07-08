import geemap.foliumap as geemap
from folium import plugins

colorScaleHex = [
    '#496FF2',
    '#82D35F',
    '#FEFD05',
    '#FD0004',
    '#8E2026',
    '#D97CF5'
]

vis_params = {
    'NDWI': {'min': -1, 'max': 1, 'palette': 'ndwi', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
    'NDVI': {'min': -1, 'max': 1, 'palette': 'ndvi', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
    'NDSI': {'min': -1, 'max': 1, 'palette': 'RdYlBu_r', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
    'SABI': {'min': -1, 'max': 1, 'palette': 'jet_r', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
    'CGI': {'min': 1, 'max': 5, 'palette': 'PuBuGn'},
    'CDOM': {'min': 5, 'max': 50, 'palette': colorScaleHex},
    'DOC': {'min': 10, 'max': 70, 'palette': colorScaleHex},
    'Cyanobacteria': {'min': 100, 'max': 1000, 'palette': colorScaleHex},
    'Turbidity': {'min': -1, 'max': 1, 'palette': ['blue', 'green', 'yellow', 'orange', 'red']},
    'AWEI': {'min': -1, 'max': 1, 'palette': ['#f5f5dc', '#ffffcc', '#a1dab4', '#41b6c4', '#225ea8'], 'breaks': [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]}
}

def show_map(cache_image, layer_name, index_name):
    Map = geemap.Map(
        layer_ctrl=True, basemap="HYBRID", control_scale=True
    )
    minimap = plugins.MiniMap()
    Map.add_child(minimap)
    Map.addLayer(cache_image, {'min': 0, 'max': 0.3, 'bands': ['B4', 'B3', 'B2'], 'gamma': 1.3}, f"RGB - {layer_name}")
    Map.addLayer(cache_image.select(index_name), vis_params[index_name], f"{index_name} - {layer_name}")

    if index_name in ['CDOM', 'DOC']:
        label_name = f"{index_name} Colorbar [mg/l]"
    elif index_name == 'Cyanobacteria':
        label_name = f"{index_name} Colorbar [10^3 cell/ml]"
    elif index_name == 'Turbidity':
        label_name = f"{index_name} Colorbar [NTU]"
    else:
        label_name = f"{index_name} Colorbar"

    Map.add_colorbar(vis_params[index_name], label=label_name)

    Map.setCenter(19.93, 50.05, 14)
    Map.to_streamlit(height=800)
