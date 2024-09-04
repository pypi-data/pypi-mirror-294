import geohash
from shapely.geometry import Polygon, mapping
import geojson

#Referece: https://geohash.softeng.co/b

def geohash_to_bbox(gh):
    # Decode geohash to get the central latitude and longitude
    lat, lon = geohash.decode(gh)
    
    # Decode the geohash to get the bounding box
    lat_err, lon_err = geohash.decode_exactly(gh)[2:]
    
    # Calculate the bounding box coordinates
    bbox = {
        'w': max(lon - lon_err, -180),
        'e': min(lon + lon_err, 180),
        's': max(lat - lat_err, -85.051129),
        'n': min(lat + lat_err, 85.051129)
    }
    
    return bbox

def geohash_to_polygon(gh):
    # Get bounding box coordinates for the geohash
    bbox = geohash_to_bbox(gh)
    
    # Create a polygon from the bounding box
    polygon = Polygon([
        (bbox['w'], bbox['s']),
        (bbox['w'], bbox['n']),
        (bbox['e'], bbox['n']),
        (bbox['e'], bbox['s']),
        (bbox['w'], bbox['s'])
    ])
    
    return polygon

def generate_geohashes(precision):
    # Generate geohashes for the given precision
    geohashes = set()
    
    # Starting geohashes for the entire world
    initial_geohashes = ["b", "c", "f", "g", "u", "v", "y", "z", "8", "9", "d", "e", "s", "t", "w", "x", "0", "1", "2", "3", "p", "q", "r", "k", "m", "n", "h", "j", "4", "5", "6", "7"]
    
    # Expand each initial geohash to the desired precision
    def expand_geohash(gh, target_length):
        if len(gh) == target_length:
            geohashes.add(gh)
            return
        for char in "0123456789bcdefghjkmnpqrstuvwxyz":
            expand_geohash(gh + char, target_length)
    
    for gh in initial_geohashes:
        expand_geohash(gh, precision)
    
    return geohashes

def create_world_polygons_at_precision(precision):
    geohash_polygons = []
    
    # Generate geohashes for the given precision
    geohashes = generate_geohashes(precision)
    
    for gh in geohashes:
        polygon = geohash_to_polygon(gh)
        geohash_polygons.append(geojson.Feature(
            geometry=mapping(polygon),
            properties={"geohash": gh}
        ))
    
    # Create a FeatureCollection
    feature_collection = geojson.FeatureCollection(geohash_polygons)
    
    return feature_collection

def save_to_geojson(feature_collection, filename):
    # Write GeoJSON to file
    with open(filename, 'w') as f:
        geojson.dump(feature_collection, f)

# Example usage
precision = 2   # Precision level for the entire world grid
world_polygons = create_world_polygons_at_precision(precision)
output_filename = f'./data/world_geohash_polygons_precision_{precision}.geojson'
save_to_geojson(world_polygons, output_filename)

print(f"GeoJSON file saved as: {output_filename}")
