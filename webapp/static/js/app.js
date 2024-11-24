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
});

connectionManager.on("point_response", (data) => {
  console.log("Point received:", data.point);
});

// Add event listeners for UI interactions
document.addEventListener("DOMContentLoaded", () => {
  let toolSelection = document.getElementById("tool-select");
  const startDronesButton = document.getElementById("start_drones");
  console.log(toolSelection.value);

  map.on("mousedown", (e) => {
    if (toolSelection.value == "add-point") {
      console.log("add-point");
      if (mapManager.getRectangle != null) {
        mapManager.clearRectangle();
      }
      if (mapManager.points.length > 0) {
        mapManager.clearPoints();
      }
      mapManager.addPoint(e.latlng);
    } else {
      console.log("start-rectangle");
      mapManager.disableInteractions();
      let startPoint = e.latlng;
      if (mapManager.rectangle != null) {
        mapManager.clearRectangle();
      }
      map.on("mouseup", (f) => {
        console.log("add-rectangle");
        let endPoint = f.latlng;
        mapManager.addRectangle(startPoint, endPoint);
        endPoint = null;
      });
    }
  });

  // Enable point mode
  // pointButton.addEventListener("click", () => {
  //   if (mapManager.getRectangle()) {
  //     mapManager.clearRectangle();
  //   }
  //   console.log("Point mode enabled.");
  //   mapManager.disableInteractions();

  //   map.on("click", (e) => {
  //     console.log("Point clicked at:", e.latlng);
  // mapManager.addPoint(e.latlng);
  //   });
  //   map.on("mouseup", () => {
  //     mapManager.enableInteractions();
  //   });
  // });

  // // Enable area selection mode
  // areaButton.addEventListener("click", () => {
  //   console.log("Area mode enabled.");
  //   mapManager.disableInteractions();
  //   mapManager.clearPoints();
  //   let startPoint = null;

  //   map.on("mousedown", (e) => {
  //     startPoint = e.latlng; // Top-left corner of the rectangle
  //   });

  //   map.on("mouseup", (e) => {
  //     if (startPoint) {
  //       const endPoint = e.latlng; // Bottom-right corner
  //       mapManager.addRectangle(startPoint, endPoint);
  //       console.log("Rectangle Coordinates:", mapManager.getRectangleBounds());

  //       startPoint = null; // Reset for next selection
  //       mapManager.enableInteractions();
  //     }
  //   });
  // });

  // Start drones
  startDronesButton.addEventListener("click", () => {
    console.log("Start Drones button clicked!");
    connectionManager.emit(
      MapManager.getRectangle
        ? MapManager.getRectangleBounds
        : MapManager.getPoints
    );
  });
});
