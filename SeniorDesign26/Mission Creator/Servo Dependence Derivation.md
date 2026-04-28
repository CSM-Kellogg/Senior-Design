## Yaw Arm
For the yaw arm of the servo, the apparatus can be reduced to $P_1$, the center of the servo arm, $P_2$, the inner frames' point of rotation, and the arm connecting the two segments L.
![[Diagram Servo.png]]
_I realized I may have been trolling with the use of A and B._
That probably doesn't make a lot of sense, so look at the servo that controls the inner part of the gimbal. That should probably make this image make more sense. Hopefully.

The problem with trying to orient the gimbal to a certain angle is that some servo input (Range of `[1175, 1950]`) has some non-linear dependence on the output angle of the gimbal. For the sake of this derivation, I am assuming that I know the exact linear dependence from the servo input PWM to its rotation in $\theta_1$. Using analytical geometry, the resultant rotation $\theta_2$ can be solved for. Below is a derivation assuming a known $\theta_1$ from the dashed-line, the location of $P_1$, and the length of the connecting arm $L$. Setting the origin at $P_2$ makes this derivation the easiest.

The length of the arm is constant from $A$ to $B$
$$L^2 = |B-A|^2 \ \text{ where } \ A = r_2 \left(\cos\theta_2, 0, \sin\theta_2\right) \text{ and } B=P_1 + r_1(0, \cos\theta_1, \sin\theta_1)$$
Expanding the terms and reducing them gives:
$$\large2P_{1x}r_2\cos\theta_2 + 2r_2\sin\theta_2(P_{1z} + r_1\sin\theta_1) = |P|^2+r_1 - L^2 + 2r_1(P_{1y}\cos\theta_1 + P_{1z}\sin\theta_1)$$
This has the form for harmonic addition [Harmonic Addition](https://en.wikipedia.org/wiki/List_of_trigonometric_identities#Linear_combinations) (thx chat)
So, the following constants are defined as:
$$\begin{matrix}
A = 2P_{1x}r_2 \\
B = 2r_2(P_{1z} + r_1\sin\theta_1) \\
C = |P|^2+r_1 - L^2 + 2r_1(P_{1y}\cos\theta_1 + P_{1z}\sin\theta_1) \\
R=\sqrt{A^2 + B^2} \\
\alpha = \text{atan2}(A, B)
\end{matrix}$$
atan2 gives back the correct quadrant (where arc tangent is bound by `[-pi/2, pi]`)
$$\theta_2 = \arcsin\left(\frac{C}{R}\right) - \alpha$$
So, for the yaw, an angular dependence exists. A similar calculation can be done for the pitch, which is in-plane.
## Pitch Arm

$$2r_1r_2\cos(\theta_2 - \theta_1) + 2r_2P_x\cos\theta_2 = P_x^2 + r_1^2+r_2^2 + 2r_1P_x\cos\theta_1$$
Arbitrary phase shift
$$\begin{matrix}
a\sin\left(\theta + \phi_1\right)+b\sin\left(\theta + \phi_2\right) = c\sin(\theta+\phi)\\
\text{where} \\
c=a^2+b^2 - 2ab\cos\left(\phi_1 - \phi_2\right) \\
\tan(\phi)=\Large\frac{a\sin\phi_1 + b\sin\phi_2}{a\cos\phi_1 + b\cos\phi_2}
\end{matrix}$$
This yields
$$\begin{matrix}
a = 2r_1r_2 \\
b = 2r_2P_x \\
c = a^2 + b^2 - 2ab\cos(\theta_1) \\
\tan\phi = \Large\frac{a\sin(-\theta_1)}{a\cos(\theta_1)}=-tan(\theta_1)\\
\phi=-\theta_1 \\
c\sin(\theta_2 - \theta_1)=P_x^2 + r_1^2 + r_2^2 + 2r_1P_x\cos\theta_1\\
\end{matrix}$$
## Final Equations and Curve Fitting
__Yaw arm:__
$$\begin{matrix}
A=2P_{1x}r_2 \\
B = 2r_2(P_{1z} + r_1\sin\theta_1) \\
C = |P|^2+r_1 - L^2 + 2r_1(P_{1y}\cos\theta_1 + P_{1z}\sin\theta_1) \\
\alpha = \text{atan2}(A, B) \\
\theta_2 = \arcsin\left(\frac{C}{\sqrt{A^2 + B^2}}\right) - \alpha
\end{matrix}$$

__Pitch arm:__
$$\begin{matrix}
a = 2r_1r_2 \\
b = 2r_2P_x \\
c = a^2 + b^2 - 2ab\cos(\theta_1) \\
\phi=-\theta_1 \\
c\sin(\theta_2 - \theta_1)=P_x^2 + r_1^2 + r_2^2 + 2r_1P_x\cos\theta_1\\
\end{matrix}$$
Using the data collected in [[Angle Dependence Data Collection]], a regression model was used to find constants for both functions.
