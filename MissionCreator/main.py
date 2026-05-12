from math import pi
from pymavlink import mavutil

from src.uploader import upload_mission
from src.findWaypoints import generateCommands, findWaypointLoc
from src.m_gps import m_gps
from src.getHomeLoc import getHomeLoc

if __name__ == "__main__":

    write_to_drone = False
    homeloc = None

    # === CONNECT TO THE DRONE
    CONNECTION_STRING = 'COM7'
    BAUD_RATE = 57600

    master = None
    print(f"Connecting to vehicle on {CONNECTION_STRING} at {BAUD_RATE} baud...")
    try:
        master = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)
    except:
        print(f"The port {CONNECTION_STRING} is not open, writing to file -- TODO -- WRITE TO FILE FUNCTIONALITY")
        # exit(1)

    # Wait for the first heartbeat to confirm connection
    if write_to_drone:
        master.wait_heartbeat()
        print(f"Heartbeat received from system (System ID: {master.target_system} Component ID: {master.target_component})")
        homeLoc = getHomeLoc(master)
    else: 
        homeLoc = input("Manually provide coordinates of home location (space seperated): ").split()
        homeLoc = list(map(float, homeLoc))
        homeLoc = m_gps(homeLoc[0], homeLoc[1], 0.0)
    # === Get user input

    # Get home location

    # Get ROI
    rois = [m_gps(lat=39.7529734, long=-105.2280673, alt=1739.38)]

    # Get takeoff altitude
    takeoffAlt = int(input("Takeoff altitude: "))

    # Get radius
    radius = input("Radius from ROI (leave blank for none): ")
    if (radius == ''): radius = None
    else: radius = int(radius)

    # Get thetas (degrees)
    thetas = map(float, input("Angles from the horizontal (degrees, space sep.): ").split())# [pi/4, pi/6]
    thetas = [i * pi/180.0 for i in thetas]

    # time delay
    delay = int(input("How long should the drone wait between commands? "))

    waypoints = findWaypointLoc(homeLoc, rois, radius, thetas)
    locRoiPairs = [(rois[i], waypoints[i]) for i in range(len(rois))]

    commands = generateCommands(locRoiPairs, 20, delay)

    [print(i) for i in commands]
    
    if write_to_drone:
        upload_mission(master, commands)
        # Close the serial connection safely
        master.close()
        print("Connection closed.")
    else: # Write to stdout
        print("TODO: MATCH CORRECT OUTPUT FORMAT FOR FILE")
        # Looks something like
        # [print(f"{cmd['seq']} {cmd['frame']} {cmd['cmd']}") for cmd in commands]