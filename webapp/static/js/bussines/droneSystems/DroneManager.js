"use strict";

import Drone from "./Drone.js";





export default class DroneManager {
  drones = [];

  constructor() {
    this.drones = [];
  }

  // Create drones from JSON data
  createDronesFromJSON(jsonData) {
    this.drones = jsonData.map(
      (drone) =>
        new Drone(
          drone.id,
          drone.name,
          drone.battery,
          drone.isSelected,
          drone.altitude
        )
    );
  }

  // Convert current drones to JSON
  toJSON() {
    return JSON.stringify(this.drones, null, 2);
  }

  // Render drone list into a given HTML container
  renderDrones(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container with ID "${containerId}" not found.`);
      return;
    }

    container.innerHTML = ""; // Clear existing content

    this.drones.forEach((drone) => {
      const droneElement = document.createElement("li");
      droneElement.className = "drone-item";
      droneElement.innerHTML = `
        <strong>${drone.name}</strong> (ID: ${drone.id})<br>
        Battery: ${drone.battery}%<br>
        Altitude: ${drone.altitude} m<br>
        <label>
          <input type="checkbox" ${drone.isSelected ? "checked" : ""}>
          Selected for mission
        </label>
      `;

      // Add event listener to toggle selection
      const checkbox = droneElement.querySelector('input[type="checkbox"]');
      checkbox.addEventListener("change", () => {
        drone.toggleSelection();
      });

      container.appendChild(droneElement);
    });
  }
}
