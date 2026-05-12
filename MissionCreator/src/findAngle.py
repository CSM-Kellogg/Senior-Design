import numpy as np

PITCH_LOWEST = 1100
PITCH_MIDDLE = 1500
PITCH_HIGHEST = 1950
ANGLE_TO_PWM = 11.2580727418

# degrees, returns the desired PWM for the pitch of the gimbal
def PWMFromTheta2_pitch(theta_2):
    # Go to radians
    theta_2 *= np.pi / 180.0

    r_1 = 15; r_2 = 18; L = 42; P_x = L

    A = 2*r_1*r_2
    B = 2*P_x*r_1
    C = A*A + B*B - 2*A*B*np.sin(theta_2)
    D = P_x**2 + r_1**2 + r_2**2 - L*L - 2*P_x*r_1*np.sin(theta_2)

    theta_1 = np.arcsin(D/C) + theta_2
    # Back to degrees
    theta_1 *= 180.0 / np.pi

    PWM_out = ANGLE_TO_PWM * theta_1 + PITCH_MIDDLE
    if (PWM_out > PITCH_HIGHEST): PWM_out = PITCH_HIGHEST
    if (PWM_out < PITCH_LOWEST): PWM_out = PITCH_LOWEST

    return PWM_out

def PWMFromTheta1_yaw(theta_1):
    pass # Not immediately necessar

if __name__ == "__main__":
    print(PWMFromTheta2_pitch(-35))