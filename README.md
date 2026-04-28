### Directory

 -  `./3DPrint This`: A temporary folder containing items I wish to 3D print -- Should be in gitignore
 - `./DroneGimbalMounts`: A set of CAD files containing the parts for interfacing the gimbal with the drone, the drone with the payload (`./CameraMount`), and the roll cage with the gimbal. Items such as `batteryMount` are related to the drone itself and are reference parts.
 - `./Gimbal`: Contains CAD files for referencing the basic geometry of the gimbal along with arduino scripts to test the movement of the servos. `./testAngleDelta.html` is a website that displays a protractor for an object some variable distance from some monitor with a known diagonal length.
 - `./MissionCreator`: Contains a python project to generate commands to move the drone to waypoints and then point the drone and camera at an ROI. The one current issue is calibrating the gimbal
 - `./SmallDrone`: Contains an archive of reference and 3D printed parts for the smaller drone for mounting the battery, using mock-wings, and an interface with the buttom bars.
 - `./VideoPostProcessing`: Contains tests on tracking objects for some video feed. Good for automating motion tracking things.


### Using the Mission Creator
`python main.py`
The connection is currently set to COM7 on a 57600 baud, which is for a holybro telemetry radio connected via usb to a specific port on a computer. For some other computer, find the correct port by opening Mission Planner and using the dropdown menu in the top right. This will affect the `CONNECTION_STRING` and `BAUD_RATE` variables. Currently, the inputs for the regions of interest are manually through the `rois` variable, and accept a lattitude, longitude, and altitude variable. Setting the home location is quite finnicky, and so it may be necessary to manually set this variable. The rest of the program will prompt for inputs.

Once all inputs have been collected, the program will genereate a set of commands for drone takeoff, waypoint coordinates, servo movement (in the future), and landing. The waypoint coordinates are particularly designed such that the distance from the ROI to the drone is at a constant `radius`, and the angle between the drone

### Using the CAD files
Made in SOLIDWORKS 2025. In order to make a custom mount for the payload, the file `./DroneGimbalMounts/Mount.SLDPRT` can be modified. Note that the arm for rotating the yaw (inner arm) can collide with a bounding box. Folders are used in most CAD files to denote which features corresspond to which element on some part.

### Small Drone
Incomplete. Requires a better battery and an rx reciever compatbile with the radiomaster flight controller. This was the other timesink for this project.