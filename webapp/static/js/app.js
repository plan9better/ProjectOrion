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

const exampleDroneJSON = [
  {
    id: 1,
    name: "Drone Alpha",
    battery: 100,
    isSelected: false,
    altitude: 0,
  },
  {
    id: 2,
    name: "Drone Beta",
    battery: 100,
    isSelected: false,
    altitude: 0,
  },
  {
    id: 3,
    name: "Drone Gamma",
    battery: 100,
    isSelected: false,
    altitude: 0,
  },
    {
    id: 4,
    name: "Drone Delta",
    battery: 100,
    isSelected: false,
    altitude: 0,
  },
];

const droneManager = new DroneManager();
const socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('drone_info', function(data) {
    console.log("Received updated drone info:", data);

    // Use the existing droneManager methods to process and display the drone data
    droneManager.createDronesFromJSON(data);  // Create or update drones
    droneManager.renderDrones("drone-status");  // Render drones in the specified container
});


let popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}

map.on("click", onMapClick);
