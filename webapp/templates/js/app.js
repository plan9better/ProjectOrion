"use strict";

import DroneManager from "./bussines/droneSystems/DroneManager.js";

let map = L.map("map", { zoomControl: false }).setView(
  [54.352433, 18.647782],
  16
); // Default center and zoom
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
];

const droneManager = new DroneManager();
droneManager.createDronesFromJSON(exampleDroneJSON);
droneManager.renderDrones("drone-status");

console.log(droneManager.toJSON());

let popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}

map.on("click", onMapClick);
