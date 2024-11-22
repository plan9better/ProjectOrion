from flask import Flask, render_template, request, jsonify
import osmnx as ox

app = Flask(__name__)

@app.route('/')
def index():
    center_point = (54.352014, 18.648392)
    radius = 1000


    G = ox.graph_from_point(center_point, dist=radius, network_type='walk')

    # Extract nodes and edges from the graph as GeoDataFrames
    nodes, edges = ox.graph_to_gdfs(G)

    # Convert edge geometries to GeoJSON
    edge_geojson = edges.to_json()

    # Convert node geometries to GeoJSON
    node_geojson = nodes.to_json()

    return render_template('trash.html', center=center_point, edge_geojson=edge_geojson, node_geojson=node_geojson)


@app.route('/select-point', methods=['POST'])
def select_point():
    # Get the data sent from the client
    data = request.get_json()

    # Extract latitude and longitude
    lat = data.get('lat')
    lng = data.get('lng')

    print(f"Received point: Latitude = {lat}, Longitude = {lng}")

    # You can process or save the data as needed here
    # For example, store the coordinates in a database

    # Respond to the client
    return jsonify({"message": "Point received successfully!", "lat": lat, "lng": lng})

@app.route('/draw-rectangle', methods=['POST'])
def draw_rectangle():
    # Get the rectangle data sent from the client
    data = request.get_json()

    # Extract top-left and bottom-right coordinates
    top_left = data.get('topLeft')
    bottom_right = data.get('bottomRight')

    print(f"Rectangle received: Top-Left = {top_left}, Bottom-Right = {bottom_right}")

    # Process or store the coordinates (e.g., in a database)

    # Respond to the client
    return jsonify({"message": "Rectangle received successfully!", "topLeft": top_left, "bottomRight": bottom_right})



app.run(debug=True)

