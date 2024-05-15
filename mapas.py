import xml.etree.ElementTree as ET
import json

# URL EARTH https://earth.google.com/earth/d/1EZm0gdxRJSdQdkzRHrIXDp1ROVBhTMkt?usp=sharing

def kml_to_geojson(kml_path, geojson_path):
    
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Definir estructura geojson
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    ns = {
        'kml': 'http://www.opengis.net/kml/2.2',
        'gx': 'http://www.google.com/kml/ext/2.2'
    }

    # iterar en cada placemark del knml
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text
        polygon = placemark.find('.//kml:Polygon', ns)
        if polygon is not None:
            # Extrae coordenadas
            coordinates_raw = polygon.find('.//kml:coordinates', ns).text
            # procesa los pares coordenadas lon lat
            coordinates = []
            coord_pairs = coordinates_raw.strip().split()
            for pair in coord_pairs:
                lon, lat, _ = map(float, pair.split(','))
                coordinates.append([lon, lat])
            
            # construye el feature
            feature = {
                "type": "Feature",
                "properties": {
                    "name": name
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]  # poligono lista de coordenadas en lista
                }
            }
            # añade la iteración en la estructura global
            geojson['features'].append(feature)

    # escribe el archivo geojson
    with open(geojson_path, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"GeoJSON has been saved to {geojson_path}")

# Lo usé en este test 
# pasar la ruta del archivo kml y la ruta de destino del  geojson
kml_to_geojson('Zonas test.kml', 'zonas_test.geojson')
