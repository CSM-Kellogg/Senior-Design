"""
Inputs: home location, region(s) of interest, desired radius (optional), desired angle with horizontal plane
"""

from pymavlink import mavutil
from m_types.gps import m_gps
from math import asin, sqrt, sin, cos, tan, atan2, asin, pi

from findAngle import PWMFromTheta2_pitch

"""
homeLoc is the location of the home of the drone (from takeoff)
ROIs are the regions of interest to observe
radius is how far away the point should be from the ROI
theta is how far above from the horizontal the drone should be (the horizontal is relative to the ROI)
"""

EARTH_RAD = 6_371_000 # meters

"""
Generates waypoints and rotations of the gimbal if specified
"""
def generateCommands(GPSPoints: list[tuple[m_gps, m_gps]]=None, takeoffAlt=20, delayTime=4):
    # Add 0 and 1, these are reserved by ardupilot somewhat
    commands = [
        {"seq": 0, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
         "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 0},
        
        # Sequence 1: Takeoff to 20 meters
        {"seq": 1, "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
         "cmd": mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": takeoffAlt},
    ]

    for loc, roi in GPSPoints:
        # Location waypoint
        waypoint = {
            "seq": len(commands), "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": int(loc.lat * 1e7), "lon": int(loc.long * 1e7), "alt": -loc.alt
        }; commands.append(waypoint) # Move to location
        
        # Point drone
        setROI = {
            "seq": len(commands), "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_DO_SET_ROI_LOCATION,
            "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": int(roi.lat * 1e7), "lon": int(roi.long * 1e7), "alt": -roi.alt
        }; commands.append(setROI) # Set ROI

        # Point camera
        setServo = {

        }; commands.append(setServo) # Set pitch angle

        # Loiter
        loiter = {
            "seq": len(commands), "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,
            "p1": delayTime, "p2": 0, "p3": 0, "p4": 0, "lat": int(loc.lat * 1e7), "lon": int(loc.long * 1e7), "alt": loc.alt
        }; commands.append(loiter) # Wait for a minute

        # Clear ROI
        clearROI = {
            "seq": len(commands), "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_DO_SET_ROI_LOCATION,
            "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 0
        }; commands.append(clearROI) # Clear ROI
    
    # Land the drone with a command
    commands.append({
        "seq": len(commands), "frame": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, "cmd": mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
        "p1": 0, "p2": 0, "p3": 0, "p4": 0, "lat": 0, "lon": 0, "alt": 0
    })

    return commands

def findWaypointLoc(homeLoc: m_gps, ROIs: list[m_gps], radius: float, thetas: list[float]):
    points = []

    for roi in ROIs:
        D_home_roi = distGPS(homeLoc, roi)

        if thetas == None:points.append(homeLoc)
        for theta in thetas:
            # If no radius was provided, use the home location.
            if radius == None: points.append(m_gps(long=homeLoc.long, lat=homeLoc.lat, alt=20))
            else:
                D_long = roi.long - homeLoc.long
                alpha = atan2(sin(D_long) * cos(roi.lat), (cos(homeLoc.lat) * sin(roi.lat) - sin(homeLoc.lat) * cos(roi.lat) * cos(D_long)))
                delta = radius / EARTH_RAD

                lat3 = asin((sin(homeLoc.lat) * cos(delta) + cos(homeLoc.lat) * sin(delta) * cos(alpha)))
                long3 = homeLoc.long + atan2(sin(alpha) * sin(delta) * cos(homeLoc.lat), (cos(delta) - sin(homeLoc.lat) * sin(lat3)))

                points.append(m_gps(long=long3, lat=lat3, alt=radius*sin(theta)))
    
    return points

"""
Gets the PWM value to set the pitch of the drone gimbal using the alt value in the m_gps object. Assumes the drone is already facing the target
"""
def getPitchPWM(currentLoc: m_gps, target: m_gps):
    dist = distGPS(currentLoc, target)
    Delta_alt = currentLoc.alt - target.alt # Should always be positive
    
    theta = atan2(Delta_alt, dist / 100)

    print(theta * 180.0 / pi)

    # Offset because the mount angle is at 45 degrees
    theta += pi/4

    return PWMFromTheta2_pitch(theta * 180.0 / pi)

"""
Returns distance between two gps points
"""
def distGPS(a: m_gps, b: m_gps):
    D_lat = b.lat - a.lat
    D_long = b.long - a.long
    return 2*EARTH_RAD * asin( sqrt( sin(D_lat / 2)**2 + cos(a.lat) * cos(b.lat) * sin(D_long / 2)**2 ) )

"""
Figure out the values to send to the servos for the specific gimbal I was given in order to point at some object

Input to servos: 1100 - 1900
PWM11: Servo for pitch: (High points up, low points down, is likely 1 to 1)
PWM12: Servo for yaw (not horizontal yaw) (low points right, high points left) Design prohibits pointing left i think
"""


if __name__ == "__main__":
    # rois = [m_gps(5,5,5)]
    # locs = findWaypointLoc(m_gps(10, 10, 0), rois, 10, [pi/6.0, pi/4.0])

    # locRoiPairs = [(rois[i], locs[i]) for i in range(len(rois))]

    # commands = generateCommands(locRoiPairs, 10, 3)

    # [print(i) for i in commands]

    print(getPitchPWM(m_gps(39.751996, -105.2268044, 1769), m_gps(39.7529734, -105.2280673, 1745.47)))