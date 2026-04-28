int servoPin = 9;      // The digital pin connected to the servo signal wire
int pulseWidth = 1500; // Variable to store the current pulse width (starts at center)

void setup() {
  pinMode(servoPin, OUTPUT); // Set the servo pin as an output
}

void loop() {
  // Sweep from 1100µs to 1900µs
  for (pulseWidth = 1100; pulseWidth <= 1900; pulseWidth += 5) { 
    sendServoPulse(servoPin, pulseWidth);
    delay(20);
  }
  
  // Sweep back from 1900µs to 1100µs
  for (pulseWidth = 1900; pulseWidth >= 1100; pulseWidth -= 5) { 
    sendServoPulse(servoPin, pulseWidth);
    delay(20);
  }
}

// Custom function to manually generate the PWM signal
void sendServoPulse(int pin, int highTime) {
  digitalWrite(pin, HIGH);              // Turn the signal HIGH
  delayMicroseconds(highTime);          // Keep it HIGH for the target microseconds (1100-1900)
  
  digitalWrite(pin, LOW);               // Turn the signal LOW
  
  // The total cycle needs to be 20,000 microseconds (20ms)
  // So we wait for the remainder of the 20ms cycle before sending the next pulse
  delayMicroseconds(20000 - highTime); 
}