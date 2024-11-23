from flask import Flask, render_template, request, jsonify
import osmnx as ox
from flask_socketio import SocketIO, emit
# from sitl.controler import DroneController

app = Flask(__name__)
socketio = SocketIO(app)

mission_data = []

point = [0,0]

def start_mission():
    #algos.get_drones_data()
    #hive_controller.start_mission()
    pass



@app.route('/')
def index():
    test_ss = {"abc": "abc"}
    return render_template('index.html', test_ss=test_ss)


@app.route("/mission_data")
def get_mission_data():
    # nodes_list = cacluclate_points(altitude,no_drones,starting posints,mission_coordinates)
    pass



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


@socketio.on("add_point")
def add_point(point):

    print(point)
    point = []
    emit('point_response', {'point': point})


@socketio.on("send_drones")
def send_drones(data):
    print("the drones have been sent")
    emit('drone_response', {'message': 'The drones have been sent successfully!'})

@socketio.on('connect')
def handle_connect():

    drone_info = example_drone_data = [
    {"id": 1, "name": "Drone Alpha", "battery": 100, "isSelected": False, "altitude": 0},
    {"id": 2, "name": "Drone Beta", "battery": 100, "isSelected": False, "altitude": 0},
    {"id": 3, "name": "Drone Gamma", "battery": 100, "isSelected": False, "altitude": 0},
    {"id": 4, "name": "Drone Delta", "battery": 100, "isSelected": False, "altitude": 0},
]
    # Send data to the client (browser)
    emit('drone_info', drone_info)


app.run(debug=True)

