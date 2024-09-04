# https://github.com/ha8tks/Leaflet.Maidenhead
# https://ha8tks.github.io/Leaflet.Maidenhead/examples/
import json
from tiles_util.utils.geocode import maidenhead
import geojson
from shapely.geometry import Polygon, mapping
import numpy as np

def maidenGrid2GeoJSON(*coords):
    if len(coords) < 7:
        raise ValueError("Insufficient coordinates. Provide a center, bounding box coordinates, and a maiden property value.")

    # Extract the center from the first two coordinates
    center = coords[:2]
    
    # Extract the bounding box coordinates
    min_lat, min_lon, max_lat, max_lon = coords[2:6]
    
    # Extract the maiden property value
    maiden_code = coords[6]

    # Create the polygon from the bounding box
    polygon_coords = [
        [min_lon, min_lat],  # Bottom-left
        [max_lon, min_lat],  # Bottom-right
        [max_lon, max_lat],  # Top-right
        [min_lon, max_lat],  # Top-left
        [min_lon, min_lat]   # Closing the polygon
    ]

    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [center[1], center[0]]  # [lon, lat]
                },
                "properties": {
                    "maiden": maiden_code
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygon_coords]  # List of coordinates
                },
                "properties": {
                    "maiden": maiden_code
                }
            }
        ]
    }

    return geojson

maidenhead_code = maidenhead.toMaiden(10.434343,106.23232,4)
maidenhead_grid = maidenhead.maidenGrid(maidenhead_code)

print(maidenhead_code)
print(maidenhead_grid)
output_path = './data/grid/maidenhead/maidenhead.geojson'
geojson_data= maidenGrid2GeoJSON(*maidenhead_grid)
# print (geojson_data)
with open(output_path, 'w') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2)