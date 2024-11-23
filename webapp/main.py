from flask import Flask, render_template, request, jsonify
import osmnx as ox
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# hive_controller = new HiveController()


def start_mission():
    #algos.get_drones_data()
    #hive_controller.start_mission()
    pass


@app.route('/')
def index():
    pass


@app.route("/mission_data")
def get_mission_data():
    pass

@socketio.on('broadcast')
def update_map():
    emit({"drones"})

def send_drones():
    pass




app.run(debug=True)

