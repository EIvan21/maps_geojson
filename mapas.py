import xml.etree.ElementTree as ET
import json

def kml_to_geojson(kml_path, geojson_path):
    # Parse the KML file
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Define the GeoJSON base structure
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # XML namespaces used in KML
    ns = {
        'kml': 'http://www.opengis.net/kml/2.2',
        'gx': 'http://www.google.com/kml/ext/2.2'
    }

    # Loop through each Placemark in the KML
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text
        polygon = placemark.find('.//kml:Polygon', ns)
        if polygon is not None:
            # Extract coordinates
            coordinates_raw = polygon.find('.//kml:coordinates', ns).text
            # Process coordinates string into list of lists (lon, lat pairs)
            coordinates = []
            coord_pairs = coordinates_raw.strip().split()
            for pair in coord_pairs:
                lon, lat, _ = map(float, pair.split(','))
                coordinates.append([lon, lat])
            
            # Build the feature
            feature = {
                "type": "Feature",
                "properties": {
                    "name": name
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]  # Polygon coordinates must be a list of lists
                }
            }
            # Append the feature to the GeoJSON structure
            geojson['features'].append(feature)

    # Write the GeoJSON output to a file
    with open(geojson_path, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"GeoJSON has been saved to {geojson_path}")

# Example usage:
kml_to_geojson('Zonas test.kml', 'zonas_test.geojson')
