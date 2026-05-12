from .m_gps import m_gps
from pymavlink import mavutil

def getHomeLoc(master):
    # Ask the drone specifically for the HOME_POSITION message
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_HOME_POSITION, 
        0, 0, 0, 0, 0, 0
    )

    # Wait up to 10 seconds for the response
    msg = master.recv_match(type='HOME_POSITION', blocking=True, timeout=10)

    if msg:
        lat = msg.latitude / 1e7
        lon = msg.longitude / 1e7
        alt = msg.altitude / 1000.0 # Altitude comes back in millimeters
        print(f"Home is at: {lat}, {lon}, {alt}m")

        return m_gps(lat=lat, long=lon, alt=alt)

    print("Home position not found, returning 0, 0, 0")
    return m_gps()