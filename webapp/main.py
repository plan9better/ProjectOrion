from flask import Flask, render_template, request, jsonify
import osmnx as ox
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)



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
    pass

@socketio.on('broadcast')
def update_map():
    emit({"drones" : "2"})

def send_drones():
    pass

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

