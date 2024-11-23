"use strict";

export default class Drone {
  id;
  name;
  battery;
  isSelected;
  altitude;

  constructor(id, name, battery, isSelected = false, altitude = 0) {
    this.id = id;
    this.name = name;
    this.battery = battery;
    this.isSelected = isSelected;
    this.altitude = altitude;
  }

  toggleSelection() {
    this.isSelected = !this.isSelected;
  }
}
