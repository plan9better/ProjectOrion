from cachecontrol import controller
from flask import Flask, render_template, request, jsonify
import osmnx as ox
from flask_socketio import SocketIO, emit
import asyncio
import sitl.controler
import sitl.listener
import json

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
    # nodes_list = cacluclate_points(altitude,no_drones,starting posints,mission_coordinates)
    pass

# @app.route('/draw-rectangle', methods=['POST'])
# def draw_rectangle():
#     # Get the rectangle data sent from the client
#     data = request.get_json()
#
#     # Extract top-left and bottom-right coordinates
#     top_left = data.get('topLeft')
#     bottom_right = data.get('bottomRight')
#
#     print(f"Rectangle received: Top-Left = {top_left}, Bottom-Right = {bottom_right}")
#
#     # Process or store the coordinates (e.g., in a database)
#
#     # Respond to the client
#     return jsonify({"message": "Rectangle received successfully!", "topLeft": top_left, "bottomRight": bottom_right})

pt1lat =  None
pt2lat =  None
pt1lon =  None
pt2lon =  None
number_of_drones = None
@socketio.on("get_data")
def parse_data(data):
    if data['data_type'] == 'point':
        lat = data['lat']
        lon = data['lon']
    if data['data_type'] == 'area':
        # example = {'area1' : {'top_left' : {'lat' : 1, 'lon' : 1}}, 'area1' : {'bottom_right' : {'lat' : 1, 'lon' : 1}}}
        pt1lat = data['area1']['top_left']['lat']
        pt1lon = data['area1']['bottom_right']['lon']
        pt2lat = data['area2']['top_left']['lat']
        pt2lon = data['area2']['bottom_right']['lon']
        number_of_drones = data['number_of_drones']

    emit('data_response', {'status': 'ok'})

async def update_drone_data():
        pt1lat = 54.5321
        pt2lat = 54.5321
        pt1lon = 54.5321
        pt2lon = 54.5221
        number_of_drones = 5
        data = sitl.controler.start_drones((pt1lat, pt1lon), (pt2lat, pt2lon), number_of_drones)
        while True:

            # string_data  = await sitl.listener.listen_for_messages()
            # json_obj = json.loads(string_data)
            json_obj = {'a' : 'a'}
            socketio.emit('drone_info', json_obj)
            await asyncio.sleep(2)




@socketio.on("send_drones")
def send_drones(data):
    print("the drones have been sent")
    asyncio.run_coroutine_threadsafe(update_drone_data(), asyncio.get_event_loop())
    emit('drone_response', {'message': 'The drones have been sent successfully!'})

@socketio.on('connect')
def handle_connect():

    drone_info = example_drone_data = [
    {"id": 1, "name": "Drone Alpha", "battery": 100, "isSelected": False, "altitude": 0 , "on_mission" : False,'lat' : 0, 'lon' : 0},
    {"id": 2, "name": "Drone Beta", "battery": 100, "isSelected": False, "altitude": 0,"on_mission" : False,'lat' : 0, 'lon' : 0},
    {"id": 3, "name": "Drone Gamma", "battery": 100, "isSelected": False, "altitude": 0,"on_mission" : False,'lat' : 0, 'lon' : 0},
    {"id": 4, "name": "Drone Delta", "battery": 100, "isSelected": False, "altitude": 0,"on_mission" : False,'lat' : 0, 'lon' : 0},
]


    emit('drone_info', drone_info)


app.run(debug=True)

