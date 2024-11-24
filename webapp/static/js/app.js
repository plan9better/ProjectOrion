"use strict";

import DroneManager from "./bussines/droneSystems/DroneManager.js";
import ConnectionManager from "./bussines/ConnectionManager.js";
import MapManager from "./bussines/MapManager.js";

// Initialize map
const map = L.map("map", { zoomControl: false }).setView(
  [54.352433, 18.647782],
  16
);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

// Initialize managers
const droneManager = new DroneManager();
const connectionManager = new ConnectionManager(
  `http://${document.domain}:${location.port}`
);

const mapManager = new MapManager(map);

// WebSocket listeners
connectionManager.on("drone_info", (data) => {
  console.log("Received updated drone info:", data);
  droneManager.createDronesFromJSON(data);
  droneManager.renderDrones("drone-status");

  for(let i = 0; i < 5, i++){
  dict_key = data[i].toString()
  console.log(data[disct_key])
  }


});

connectionManager.on("point_response", (data) => {
  console.log("Point received:", data.point);
});

// Add event listeners for UI interactions
document.addEventListener("DOMContentLoaded", () => {
  let toolSelection = document.getElementById("tool-select");
  const startDronesButton = document.getElementById("start_drones");
  console.log(toolSelection.value);

  let startPoint = null;
  let endPoint = null;

  map.on("mousedown", (e) => {
    mapManager.disableInteractions();
    if (toolSelection.value === "add-point") {
      if (mapManager.getRectangle()) mapManager.clearRectangle();
      mapManager.addPoint(e.latlng);
    } else {
      console.log("AAAAA");
      if (mapManager.getPoints()) mapManager.clearPoints();
      startPoint = e.latlng; // Persist the startPoint for later use
    }
  });

  map.on("mouseup", (e) => {
    console.log("WWWW");
    mapManager.enableInteractions();
    console.log("Start point" + startPoint);
    if (startPoint != null) {
      endPoint = e.latlng;
      console.log("End point" + endPoint);
      mapManager.addRectangle(startPoint, endPoint);
      startPoint = null; // Reset after use
      endPoint = null;
    }
  });

  // Start drones
  startDronesButton.addEventListener("click", () => {
    const rectangleBounds = mapManager.getRectangle()
      ? mapManager.getRectangle().getBounds()
      : null;
    const points = mapManager.getPoints();
    console.log(rectangleBounds);
    console.log(points);
    connectionManager.emit("send_drones", rectangleBounds || points);
  });
});
