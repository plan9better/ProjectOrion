"use strict";

export default class ConnectionManager {
  constructor(socketUrl) {
    this.socket = io.connect(socketUrl);
  }

  // Emit an event
  emit(event, data) {
    this.socket.emit(event, data);
  }

  // Register an event listener
  on(event, callback) {
    this.socket.on(event, callback);
  }
}
