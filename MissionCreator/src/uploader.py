"""
Example code on how to send missions to the drone
The important thing to note is that for relative coordinates, a GPS lock is required. The above won't run in a benchtop test
"""

from pymavlink import mavutil

def upload_mission(master, waypoints):
    # --- CLEAR EXISTING MISSION ---
    print("Clearing existing missions...")
    master.mav.mission_clear_all_send(master.target_system, master.target_component)
    
    # Wait for the drone to acknowledge the clear command
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if not ack or ack.type != mavutil.mavlink.MAV_MISSION_ACCEPTED:
        print("Failed to clear mission.")
        return

    # --- START MISSION UPLOAD HANDSHAKE ---
    print(f"Sending mission count: {len(waypoints)}")
    master.mav.mission_count_send(master.target_system, master.target_component, len(waypoints), mavutil.mavlink.MAV_MISSION_TYPE_MISSION)

    # Loop to respond to the drone's requests for each waypoint
    for _ in range(len(waypoints)):
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
            int(wp["seq"]),
            int(wp["frame"]),
            int(wp["cmd"]),
            0, # current (0 = false)
            1, # autocontinue (1 = true)
            float(wp["p1"]), float(wp["p2"]), float(wp["p3"]), float(wp["p4"]),
            int(wp["lat"]), int(wp["lon"]), float(wp["alt"]),
            mavutil.mavlink.MAV_MISSION_TYPE_MISSION
        )

    # --- AWAIT FINAL ACKNOWLEDGEMENT ---
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
    if ack and ack.type == mavutil.mavlink.MAV_MISSION_ACCEPTED:
        print("Mission upload successful!")
    else:
        print(f"Mission upload failed. ACK status: {ack.type if ack else 'Timeout'}")