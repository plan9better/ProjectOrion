from pymavlink import mavutil
import time
import math
from math import radians, cos, sin, sqrt, atan2

class DroneController:
    def __init__(self, connection_string="udp:127.0.0.1:14550"):
        """
        Initialize the drone controller and establish connection.
        """
        self.master = mavutil.mavlink_connection(connection_string)
        print("Waiting for heartbeat...")
        self.master.wait_heartbeat()
        print("Heartbeat received. Connected to drone.")

    def set_mode(self, mode):
        """
        Set the drone's flight mode.
        """
        mode_id = self.master.mode_mapping().get(mode)
        if mode_id is None:
            raise ValueError(f"Mode '{mode}' not supported.")
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            mode_id,
        )
        print(f"Flight mode changed to: {mode}")

    def _pre_arm_checks_passed(self):
        # Query system status and check relevant flags
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,  # Confirmation
            mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS,  # Message ID for SYS_STATUS
            0, 0, 0, 0, 0, 0,
        )
        while True:
            msg = self.master.recv_match(type='SYS_STATUS', blocking=True)
            if msg:
                # Check system health and sensors
                sensors_health = msg.onboard_control_sensors_health
                sensors_present = msg.onboard_control_sensors_present

                # Check if all required sensors are present and healthy
                if sensors_health & sensors_present == sensors_present:
                    print("Pre-arm checks passed: All required sensors healthy.")
                    return True
                else:
                    print(f"Pre-arm checks not passed: Sensors health: {bin(sensors_health)}")
                    return False

    def arm(self):
        """
        Arm the drone.
        """
        self.master.arducopter_arm()

    def disarm(self):
        """
        Disarm the drone.
        """
        self.master.arducopter_disarm()
        print("Disarming motors...")
        self._wait_for_arm_status(armed=False)


    def _wait_for_arm_status(self, armed, timeout=240):
        """
        Wait until the drone is armed/disarmed.
        """
        start = time.time()
        while True:
            if self.master.motors_armed() == armed:
                print("Drone is now armed." if armed else "Drone is now disarmed.")
                return
            if time.time() - start > timeout:
                raise TimeoutError("Timeout while waiting for arming/disarming.")
            time.sleep(1)

    def takeoff(self, altitude):
        """
        Command the drone to take off to a specified altitude.
        """
        print(f"Taking off to {altitude} meters...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0,
            altitude,
        )
        
    def wait_takeoff(self, altitude):
        alt = 0
        while alt < altitude - 5 or alt > altitude + 5:
            msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                # Extract position data from the message
                lat = msg.lat / 1e7  # Convert from degrees * 10^7 to degrees
                lon = msg.lon / 1e7  # Convert from degrees * 10^7 to degrees
                alt = msg.relative_alt / 1000  # Convert from mm to meters
        print("Reached target altitude of {}", altitude)
        

    def go_to(self, latitude, longitude, altitude):
        """
        Command the drone to go to a specific GPS location.
        """
        print(f"Navigating to lat: {latitude}, lon: {longitude}, alt: {altitude}...")
        self.master.mav.set_position_target_global_int_send(
            0,
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            int(0b110111111000),  # Position only
            int(latitude * 1e7),
            int(longitude * 1e7),
            altitude,
            0, 0, 0,  # Velocity
            0, 0, 0,  # Acceleration
            0, 0,     # Yaw, Yaw rate
        )

    def land(self):
        """
        Command the drone to land.
        """
        print("Landing...")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0,
        )
        # msg = self.master.recv_match(type="EXTENDED_SYS_STATE", blocking=True)
        while self.get_altitude() > 2:
            time.sleep(2)
        print("Landed")
            

    def get_position(self):
        """
        Get the current position of the drone.
        """
        print("Fetching current position...")
        msg = self.master.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
        latitude = msg.lat / 1e7
        longitude = msg.lon / 1e7
        altitude = msg.relative_alt / 1e3  # Convert from mm to meters
        print(f"Current Position: lat={latitude}, lon={longitude}, alt={altitude}")
        return latitude, longitude, altitude

    def is_within_radius(self, current_lat, current_lon, target_lat, target_lon, radius=15):
        """
        Check if the current position is within a radius around the target position.
        Assumes a flat Earth for small distances.
        
        Args:
            current_lat (float): Current latitude in degrees.
            current_lon (float): Current longitude in degrees.
            target_lat (float): Target latitude in degrees.
            target_lon (float): Target longitude in degrees.
            radius (float): Radius in meters. Default is 15 meters.
        
        Returns:
            bool: True if within radius, False otherwise.
        """
        # Differences in latitude and longitude
        d_lat = (target_lat - current_lat) * 111320  # Convert latitude difference to meters
        d_lon = (target_lon - current_lon) * 111320 * math.cos(math.radians(current_lat))  # Adjust for latitude
        
        # Euclidean distance
        distance = math.sqrt(d_lat**2 + d_lon**2)
        return distance <= radius
    def get_flight_mode(self):
        """
        Retrieve the current flight mode of the drone.
        """
        msg = self.master.recv_match(type="HEARTBEAT", blocking=True, timeout=5)
        if not msg:
            return None
        mode = mavutil.mode_string_v10(msg)
        return mode

    def get_altitude(self):
        """
        Retrieve the current altitude of the drone using VFR_HUD.
        """
        msg = self.master.recv_match(type="GLOBAL_POSITION_INT", blocking=True)
        if not msg:
            return None
        return msg.relative_alt

    def get_vertical_speed(self):
        """
        Retrieve the vertical speed of the drone using VFR_HUD.
        """
        msg = self.master.recv_match(type="VFR_HUD", blocking=True, timeout=5)
        if not msg:
            return None
        return msg.climb

    def is_taking_off(self):
        """
        Check if the drone is currently taking off.
        """
        flight_mode = self.get_flight_mode()
        if flight_mode not in ["GUIDED", "TAKEOFF"]:
            return False

        altitude = self.get_altitude()
        vertical_speed = self.get_vertical_speed()

        if altitude is not None and vertical_speed is not None:
            # Consider taking off if vertical speed is positive and altitude is increasing
            if vertical_speed > 0.1:
                print(f"Taking off: Altitude = {altitude}m, Climb Rate = {vertical_speed}m/s")
                return True
        return False

    def has_arrived(self, target_lat, target_lon, target_alt, tolerance=0.5):
        """
        Check if the drone has arrived at the target location.

        Parameters:
        - target_lat: Target latitude in degrees.
        - target_lon: Target longitude in degrees.
        - target_alt: Target altitude in meters.
        - tolerance: Acceptable distance to the target in meters (default 0.5m).

        Returns:
        - True if within tolerance, False otherwise.
        """
        current_lat, current_lon, current_alt = self.get_position()

        # Calculate the horizontal distance (Haversine formula for simplicity)

        R = 6371000  # Earth radius in meters
        d_lat = radians(target_lat - current_lat)
        d_lon = radians(target_lon - current_lon)
        a = (sin(d_lat / 2) ** 2 +
            cos(radians(current_lat)) * cos(radians(target_lat)) * sin(d_lon / 2) ** 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        horizontal_distance = R * c

        # Calculate vertical distance
        vertical_distance = abs(current_alt - target_alt)

        # Check if both horizontal and vertical distances are within tolerance
        if horizontal_distance <= tolerance and vertical_distance <= tolerance:
            print("Drone has arrived at the target location.")
            return True
        else:
            print(f"Drone is not at target. Horizontal: {horizontal_distance:.2f}m, "
                f"Vertical: {vertical_distance:.2f}m")
            return False

    def pre_arm_checks_passed(self):
        """
        Verify pre-arm checks by monitoring system status and health.
        """
        print("Checking pre-arm status...")
        # Request system status
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,  # Confirmation
            mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS,
            0, 0, 0, 0, 0, 0,
        )
        i = 0
        while True:
            msg = self.master.recv_match(type="SYS_STATUS", blocking=True, timeout=5)
            if not msg:
                print("Timeout waiting for SYS_STATUS.")
                continue

            sensors_health = msg.onboard_control_sensors_health
            sensors_present = msg.onboard_control_sensors_present

            # Ensure all required sensors are healthy
            if sensors_health & sensors_present == sensors_present:
                print("Pre-arm checks passed: All required sensors are healthy.")
                return True
            else:
                # print(f"Pre-arm checks failed: Sensor health bitmask: {bin(sensors_health)}")
                print('.' * ((i%3) + 1))
                print(bin(sensors_health), bin(sensors_present))
                i+=1
                time.sleep(1)


    def try_arm(self):
        self.arm()
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
        # while msg.system_status != mavutil.mavlink.MAV_STATE_ACTIVE:
        while not msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
            self.arm()
            msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
            print(msg)

    def from_disarm_to_point(self, takeoff_alt,lat, lon, alt):
        self.set_mode("GUIDED")
        msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
        i = 0
        print("MAV STATE: {}", msg.system_status)
        while msg.system_status != mavutil.mavlink.MAV_STATE_STANDBY:
            print("Waiting for pre-arm checks to pass", end="")
            print('.' * (i%4 + 1))
            i+=1
            msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
            time.sleep(1)

        self.try_arm()
        while not self.is_taking_off():
            self.set_mode("GUIDED")
            if not msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
                self.try_arm()
            print("taking off: ", self.is_taking_off())
            self.takeoff(takeoff_alt)
        self.wait_takeoff(takeoff_alt)

        self.go_to(lat, lon, alt)
        drone_lat, drone_lon, drone_alt = self.get_position()
        print("Flying", end='')
        while not self.has_arrived(lat, lon, alt):
            print('.',end="")
            time.sleep(2)
            msg = self.master.recv_match(type='HEARTBEAT', blocking=True)
            print(msg)
        print("Drone arrived")
        self.land()
        self.disarm()

def main():
    controler = DroneController()
    lat=54.34712607259228
    lon=18.63670854829568
    alt = 100
    controler.from_disarm_to_point(70, lat, lon, alt)
    input("alskdjf")
    lat = 54.35434358145789
    lon = 18.594050652439748
    controler.from_disarm_to_point(70, lat, lon, alt)



if __name__=="__main__":
    main()