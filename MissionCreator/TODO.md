### Gimbal Pointing

Mount the gimbal. Retrieve the home location of the drone

Try pointing manually

Try pointing using Set ROI

https://ardupilot.org/copter/docs/common-mount-targeting.html



### Gimbal calibration
__1. Find limits__
 - 1100 to 1900 for pitch (5 to 173 degrees)
 - 1175 to 1925 for yaw?

__2. Functions to point the gimbal at some coordinate__

__3. Record what angles corresspond to what servo input__
For starters, 1500 is the center for both motors (due to the mounting angle of the gimbal, this means -45 and 0)

Use tape to represent angles onto the high bay door
    tan(theta) = wall dist / normal dist to wall
    Harder to setup
    More directly programmable
    Works for both pitch and yaw

Or, use the field goal outside
 - Less controlled
 - Higher accuracy because its further away
 - Relies on GPS data for angle measurements

Side note: See if a recording is possible if the camera is disconnected from the hotspot

### Math for pitch/yaw

Pitch is 1 to 1, so input angle is output angle

Yaw is related to the ratios of the lever arms

Lever arm (servo) = L_s Measured with a caliper to be 16 mm
Lever arm (gimbal) = L_g Measured to be 24.5 mm

The servo arm turns circular motion into circular motion in another plane
The delta x of the servo arm equals the delta x of the gimbal (dx_s = dx_g)


## Attempts that didn't work with an arduino board


### Attempt one -- not linear
dx_s / (2*L_s) = tan(theta_s/2)    =>    dx_s = tan(theta_s/2) * (2 * L_s)
dx_g / (2*L_g) = tan(theta_g/2)    =>    dx_g = tan(theta_g/2) * (2 * L_g)

tan(theta_s/2) * (2 * L_s) = tan(theta_g/2) * (2 * L_g)
theta_s = 2 * arctan(tan(theta_g/2) * L_g / L_s)

Let the distance from the vertical to the current position of the arm be Dx

### Attempt 2 -- Not linear
// => theta_2 = theta_1 * L_2/L_1 = theta_1 * 25.5/16.0

### Do an analytic derivation
L_s = 16mm
theta_s ??? Calculated using bar length and distance between points
L_g = 24mm
bar = 48.12mm

