#include <Servo.h>
#include <math.h>

/** For Pitch servo
Range is 1100 to 2000

Angle sweep is allegedly from the map(angle, 0, 180, 544, 2400)
So, this is 53 to 141 in angle

Midpoint is now 97
*/

Servo myServo;  // Create a servo object to control a servo

int pos = 0;    // Variable to store the servo position

const int testAngles[] = {-10, -5, 0, 5, 10};

const int sweep = 5;

const int midpoint = 97;

const double YAW_ARM_RATIO = 24.0 / 16.0;

const double PITCH_ARM_RATIO = 2.0;

void setup() {
  myServo.attach(9);  // Attaches the servo on pin 9 to the servo object

  myServo.write(97);

  Serial.begin(9600);

  Serial.println(getNewTheta(midpoint - sweep));
  Serial.println(getNewTheta(midpoint));
}

void loop() {
  for (int i = 0; i < 5; i ++) {
    // myServo.write(getNewTheta(i));
    myServo.write(midpoint + testAngles[i]);
    delay(1000);
  }

  for (int i = 5; i > 0; i --) {
    // myServo.write(getNewTheta(i));
    myServo.write(midpoint + testAngles[i]);
    delay(1000);
  }
}

int getNewTheta(int theta1) {
  int diff = theta1 - midpoint;
  // double tmp =  360.0 / PI * atan(tan(diff * PI / 360.0) * YAW_ARM_RATIO);
  double tmp = diff * 27.5/16.0;
  return (int) (tmp + midpoint);
}