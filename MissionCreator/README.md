### Contents
`main.py` The entry point for the program. Example input shown below

`src` Contains all helper files for generating the mission planner script
    `m_types` Contains a custom data type (tuple, mostly) object for a gps location with some alitude
    `findAngle.py` -- The algorithms to point the gimbal servos
    `findWaypoints.py` -- Generates waypoints and commands for an automated drone flight (untested)
    `getHomeLoc.py` -- Gets the home location of the drone
    `uploader.py` -- Automatically uploads the missions onto the drone software. Not a great success rate