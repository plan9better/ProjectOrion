"use strict";

export default class MapManager {
  constructor(map) {
    this.map = map;
    this.rectangle = null;
    this.rectangle_bounds = null;
    this.points = new Array();
    this.markers = new Array();
  }

  // Disable map interactions
  disableInteractions() {
    this.map.dragging.disable();
    this.map.doubleClickZoom.disable();
    this.map.scrollWheelZoom.disable();
    this.map.boxZoom.disable();
  }

  // Enable map interactions
  enableInteractions() {
    this.map.dragging.enable();
    this.map.doubleClickZoom.enable();
    this.map.scrollWheelZoom.enable();
    this.map.boxZoom.enable();
  }

  // Add a point to the map and list
  addPoint(latlng) {
    let marker = L.marker(latlng).addTo(this.map);
    this.markers.push(marker);
    this.points.push(latlng);
  }

  clearPoints() {
    this.markers.forEach((marker) => {
      marker.remove();
    });
    this.points = [];
  }

  getPoints() {
    return this.points;
  }

  // Draw a rectangle
  addRectangle(startPoint, endPoint) {
    if (this.rectangle) {
      this.clearRectangle();
    }
    this.rectangle = L.rectangle([startPoint, endPoint], {
      color: "red",
      weight: 2,
    }).addTo(this.map);
    this.rectangle_bounds = this.rectangle.getBounds();
  }

  getRectangle() {
    return this.rectangle;
  }

  getRectangleBounds() {
    return this.rectangle_bounds;
  }

  clearRectangle() {
    if (this.rectangle) {
      this.rectangle.remove();
      this.rectangle = null;
      this.rectangle_bounds = null;
    }
  }
}
