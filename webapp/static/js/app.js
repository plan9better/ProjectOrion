"use strict";

import DroneManager from "./bussines/droneSystems/DroneManager.js";


let map = L.map("map", { zoomControl: false }).setView(
  [54.352433, 18.647782],
  16
);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

const socket = io.connect('http://' + document.domain + ':' + location.port);

document.addEventListener('DOMContentLoaded', function () {



    var startDronesBtn = document.getElementById('start_drones');
    var selectAreaBtn = document.getElementById('add-area')
    var selectPointBtn = document.getElementById('add-point')
    selectAreaBtn.addEventListener('click', function() {
        map.off()
        defineAreaModeBehaviour()
    });
    selectPointBtn.addEventListener('click', function() {
        map.off()
        map.on("click", onMapClickPointMode);

    });








    startDronesBtn.addEventListener('click', function() {
        console.log("Start Drones button clicked!");

        socket.emit('send_drones', { message: 'Start the drones' });

        socket.on('drone_response', function(data) {
                    console.log("Response received!");

        });
    });






    const droneManager = new DroneManager();

    socket.on('drone_info', function(data) {
    console.log("Received updated drone info:", data);

    droneManager.createDronesFromJSON(data);
    droneManager.renderDrones("drone-status");
});


});






let popup = L.popup();

function onMapClickPointMode(e) {

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


function defineAreaModeBehaviour(e) {
    console.log("area mode")

    let startPoint = null; // To store the starting corner of the rectangle
        let rectangle = null; // To store the drawn rectangle

        // Capture the mousedown event (start drawing)
        map.on('mousedown', function (e) {
            startPoint = e.latlng; // Store the top-left corner
        });

        // Capture the mouseup event (finish drawing)
        map.on('mouseup', function (e) {
            if (startPoint) {
                let endPoint = e.latlng; // Bottom-right corner

                // Remove the previous rectangle (if any)
                if (rectangle) {
                    map.removeLayer(rectangle);
                }

                // Draw a rectangle
                rectangle = L.rectangle([startPoint, endPoint], {
                    color: 'red',
                    weight: 2,
                }).addTo(map);

                // Send rectangle coordinates to the server
                const rectangleBounds = {
                    topLeft: { lat: startPoint.lat, lng: startPoint.lng },
                    bottomRight: { lat: endPoint.lat, lng: endPoint.lng }
                };

                console.log('Rectangle Coordinates:', rectangleBounds);

                fetch('/draw-rectangle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(rectangleBounds),
                })
                .then(response => response.json())
                .then(data => console.log('Response from server:', data))
                .catch(error => console.error('Error:', error));

                // Reset startPoint for the next rectangle
                startPoint = null;
            }
        });
}
