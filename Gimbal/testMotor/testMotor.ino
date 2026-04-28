#include <Servo.h>

Servo myServo;  // Create a servo object to control a servo

int pos = 0;    // Variable to store the servo position

void setup() {
  myServo.attach(9);  // Attaches the servo on pin 9 to the servo object

  myServo.write(30);
}

void loop() {
  // The range for the servo library is 0 to 180
  // test limits rq
  
  // Ratio if doing yaw movement


  // myServo.write(30);
  // delay(30);
  // Sweep from 0 to 180 degrees
  for (int i = 1100; i <= 2000; i += 8) {
    pos = map(i, 544, 2400, 0, 180);
    myServo.write(pos);              // Tell servo to go to position in variable 'pos'
    delay(10);                       // Wait 15ms for the servo to reach the position
  }
  
  // Sweep back from 180 to 0 degrees
  for (int i = 2000; i >= 1100; i -= 8) {
    pos = map(i, 544, 2400, 0, 180);
    myServo.write(pos);             // Tell servo to go to position in variable 'pos'
    delay(10);                       // Wait 15ms for the servo to reach the position
  }
}