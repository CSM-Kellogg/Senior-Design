"""
main python script to figure out the pwm input to servo angle output for the gimbal (units in mm, rad)

Boilerplate by gemini
The rest by Liam Kellogg
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, Data, RealData

def fit_yaw(P, x):
    return P[0] + P[1] * x + P[2] * x**2

""" Unable to get this one to work in time, using a polynomial fit
def fit_yaw(P, x):
    # Convert x to some linearly related-theta
    # Middle of yaw is at PWM 1562.5
    theta_1 = P[2] * (x - 1562.5)

    # Measured constants
    r_1 = 15.0
    r_2 = 48.0
    L = 26.5
    P[0] = L

    # Constructing the function with a variable point P
    A = 2*P[0]*r_2
    B = 2*r_2*(P[0] + r_1*np.sin(theta_1))
    C = P[0] + P[1]
    alpha = np.arctan2(A, B)
    
    return np.arcsin(C / np.sqrt(A**2 + B**2)) - alpha
"""

# P[1] was found to be 0.08882515
def fit_pitch(P, x):
    theta_1 = P[1] * (x - 1500) # Get angle from PWM
    # Measured constants (different from pitch)
    r_1 = 15
    r_2 = 18
    L = 42
    P[0] = 42

    # Construct the function
    A = 2*r_1*r_2
    B = 2*r_2*P[0]
    C = A**2 + B**2 - 2*A*B*np.cos(theta_1)

    theta_2 = np.arcsin( (P[0]**2 + r_1**2 + r_2**2 - 2*r_1*P[0]*np.sin(theta_1)) / C ) + theta_1

    return theta_2

# 2. Generate or Load your data
data = np.genfromtxt('data.csv', delimiter=', ', skip_header=1)
x = data[:,2]
y = data[:,0]

# Define the error/standard deviation in your measurements
x_err = 0.5
y_err = 2.0

# 3. Set up the ODR framework
# Create a Model object based on your function
model = Model(fit_pitch)

# Create a RealData object (includes the errors in x and y)
data = RealData(x, y, sx=x_err, sy=y_err)

# Set up ODR with the data, model, and initial parameter guesses
odr = ODR(data, model, beta0=[42, 0.088])

# 4. Run the regression
output = odr.run()
output.pprint() # Prints a summary of the results

# Extract the fitted parameters
fitted_params = output.beta

# 5. Visualization
x_fit = np.linspace(min(x), max(x), 100)
y_fit = fit_pitch(fitted_params, x_fit)

plt.figure(figsize=(10, 6))
plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', label='Measured Data', alpha=0.6)
plt.plot(x_fit, y_fit, color='red', lw=2, label='ODR Fit')

plt.title('PWM Input to Gimbal Angle (Pitch)', fontsize=30)
plt.xlabel('Angle Measured (Degrees)', fontsize=20)
plt.ylabel('PWM Input (Servo Pitch)', fontsize=20)
plt.legend()
plt.grid(True)
plt.show()