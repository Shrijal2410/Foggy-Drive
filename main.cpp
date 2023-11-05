#include <Arduino.h>
// Define the pin numbers for the LED, motor, buzzer, ultrasonic sensor, and IR sensor
int motorPin1 = 2;  // Motor input 1
int motorPin2 = 4;  // Motor input 2
int motorSpeedPin = 3;  // Motor speed control pin (PWM)
int buzzerPin = 5;  // Buzzer pin
int trigPin = 10;  // Ultrasonic sensor trigger pin
int echoPin = 9;  // Ultrasonic sensor echo pin
int irSensorPin = 7;  // IR sensor pin

// Variables for ultrasonic sensor and IR sensor
long duration;
int distance;
int irSensorValue;

// Setup function runs once when the board starts up
void setup() {
  pinMode(motorPin1, OUTPUT);  // Initialize motor input 1 as an output.
  pinMode(motorPin2, OUTPUT);  // Initialize motor input 2 as an output.
  pinMode(motorSpeedPin, OUTPUT);  // Initialize motor speed control pin as an output.
  pinMode(buzzerPin, OUTPUT);  // Initialize buzzer pin as an output.
  pinMode(trigPin, OUTPUT);  // Initialize ultrasonic sensor trigger pin as an output.
  pinMode(echoPin, INPUT);  // Initialize ultrasonic sensor echo pin as an input.
  pinMode(irSensorPin, INPUT);  // Initialize IR sensor pin as an input.
  Serial.begin(9600);  // Initialize Serial communication at 9600 baud.
}

// Loop function runs repeatedly as long as the Arduino is powered on
void loop() {
  // Ultrasonic sensor: Measure distance in centimeters
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

// Adjust buzzer and motor based on distance
int buzzerSpeed = map(distance, 30, 50, 255, 0);  // Map distance to buzzer speed with inverse relationship
if (distance>50) buzzerSpeed = 0;
if (distance < 30) {
  // Stop the motor and turn on the buzzer to maximum when distance is less than 30 cm+
  analogWrite(motorSpeedPin, 0);  // Stop the motor
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  analogWrite(buzzerPin, 255);  // Turn on the buzzer to maximum
} else {
  // Adjust motor speed and buzzer sound based on distance
  analogWrite(motorSpeedPin, 200);  // Motor speed adjusted inversely to buzzer sound
  analogWrite(buzzerPin, buzzerSpeed);  // Set the buzzer speed
  digitalWrite(motorPin1, HIGH); // Set motor input 1 to HIGH (clockwise rotation)
  digitalWrite(motorPin2, LOW); // Set motor input 2 to LOW (clockwise rotation)
}

  // IR sensor: Read IR sensor value
  irSensorValue = digitalRead(irSensorPin);
  Serial.print("IR Sensor Output: ");
  Serial.println(irSensorValue);

  delay(500);  // Delay between readings
}