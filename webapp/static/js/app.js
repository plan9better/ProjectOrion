"use strict";

import DroneManager from "./bussines/droneSystems/DroneManager.js";



document.addEventListener('DOMContentLoaded', function () {
const socket = io.connect('http://' + document.domain + ':' + location.port);


    var startDronesBtn = document.getElementById('start_drones');
    var addPointsBtn = document.getElementById('add-points');


    function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
    socket.emit('add_point', { point: e.latlng });
      socket.on('point_response', function(data) {
                    console.log("point received!");
                    console.log(data.point)

        });
}

map.on("click", onMapClick);




    startDronesBtn.addEventListener('click', function() {
        console.log("Start Drones button clicked!");

        socket.emit('send_drones', { message: 'Start the drones' });

        socket.on('drone_response', function(data) {
                    console.log("Response received!");

        });
    });

    addPointsBtn.addEventListener('click', function() {
        console.log("Add point clicked!");

        socket.emit('start_drones_event', { message: 'Start the drones' });

        socket.on('drone_response', function(data) {
            document.getElementById('result').textContent = data.message;
        });
    });




    const droneManager = new DroneManager();

    socket.on('drone_info', function(data) {
    console.log("Received updated drone info:", data);

    droneManager.createDronesFromJSON(data);
    droneManager.renderDrones("drone-status");
});


});



let map = L.map("map", { zoomControl: false }).setView(
  [54.352433, 18.647782],
  16
);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);





let popup = L.popup();


