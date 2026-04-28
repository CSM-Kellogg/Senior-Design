from pymavlink import mavutil
import time

# --- 1. CONNECT TO THE DRONE ---
CONNECTION_STRING = 'COM7'
BAUD_RATE = 57600

print(f"Connecting to vehicle on {CONNECTION_STRING} at {BAUD_RATE} baud...")
master = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)

# Wait for the first heartbeat to confirm connection
master.wait_heartbeat()
print(f"Heartbeat received from system (System ID: {master.target_system} Component ID: {master.target_component})")

def upload_mission(master):
    """Handles the MAVLink handshake to clear and upload a new mission."""
    
    # --- 2. DEFINE THE MISSION ITEMS ---
    # We use MISSION_ITEM_INT where coordinates are scaled by 1e7 (10,000,000) 
    # to avoid floating-point errors over the telemetry link.
    
    waypoints = [
        # Sequence 0: In ArduPilot, Seq 0 is always reserved for the "Home" location.
        # We send dummy data (0s) here; the flight controller will automatically overwrite 
        # it with the drone's actual home location when it arms.
        {"seq": 0, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 0},
        
        # Sequence 1: Takeoff to 20 meters
        {"seq": 1, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 20},
        
        # Sequence 2: Waypoint 1 (Notice the coordinates are multiplied by 1e7 and cast to int)
        {"seq": 2, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": int(37.79283 * 1e7), "lon": int(-122.39544 * 1e7), "alt": 20},
        
        # Sequence 3: Waypoint 2
        {"seq": 3, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": int(37.79295 * 1e7), "lon": int(-122.39555 * 1e7), "alt": 20},
        
        # Sequence 4: Return to Launch (RTL)
        {"seq": 4, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 0},
    ]

    # --- 3. CLEAR EXISTING MISSION ---
    print("Clearing existing missions...")
    master.mav.mission_clear_all_send(master.target_system, master.target_component)
    
    # Wait for the drone to acknowledge the clear command
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if not ack or ack.type != mavutil.mavlink.MAV_MISSION_ACCEPTED:
        print("Failed to clear mission.")
        return

    # --- 4. START MISSION UPLOAD HANDSHAKE ---
    print(f"Sending mission count: {len(waypoints)}")
    master.mav.mission_count_send(master.target_system, master.target_component, len(waypoints), mavutil.mavlink.MISSION_TYPE_MISSION)

    # Loop to respond to the drone's requests for each waypoint
    for i in range(len(waypoints)):
        # Wait for the drone to ask for a specific sequence number
        msg = master.recv_match(type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True, timeout=5)
        
        if not msg:
            print("Timeout waiting for mission request from drone.")
            return
            
        print(f"Drone requested Sequence {msg.seq}. Sending...")
        
        # Grab the requested waypoint from our dictionary
        wp = waypoints[msg.seq]
        
        # Send the requested waypoint
        master.mav.mission_item_int_send(
            master.target_system,
            master.target_component,
            wp["seq"],
            wp["frame"],
            wp["cmd"],
            0, # current (0 = false)
            1, # autocontinue (1 = true)
            wp["p1"], wp["p2"], wp["p3"], wp["p4"],
            wp["lat"], wp["lon"], wp["alt"],
            mavutil.mavlink.MISSION_TYPE_MISSION
        )

    # --- 5. AWAIT FINAL ACKNOWLEDGEMENT ---
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if ack and ack.type == mavutil.mavlink.MAV_MISSION_ACCEPTED:
        print("Mission upload successful!")
    else:
        print(f"Mission upload failed. ACK status: {ack.type if ack else 'Timeout'}")

# Execute the upload
upload_mission(master)

# Close the serial connection safely
master.close()
print("Connection closed.")