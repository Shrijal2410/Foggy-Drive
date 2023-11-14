#include <Arduino.h>

const int motorPin1 = 2;
const int motorPin2 = 4;
const int motorSpeedPin = 3;
const int buzzerPin = 5;
const int trigPin = 10;
const int echoPin = 9;
const int irSensorPin = 7;

const int lowerLimit = 30;
const int upperLimit = 50;
const int maxMotorSpeed = 200;

unsigned long startTime = 0;
int distance, irSensorValue;

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorSpeedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(irSensorPin, INPUT);
  Serial.begin(9600);
}

int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  return pulseIn(echoPin, HIGH) * 0.034 / 2;
}

void motorDir(){
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
}

void controlMotorWithBuzzer() {
  int buzzerSpeed = map(distance, lowerLimit, upperLimit, 0, 255);
  int motorSpeed = constrain((distance >= lowerLimit) * buzzerSpeed, 0, maxMotorSpeed);
  analogWrite(motorSpeedPin, motorSpeed);
  analogWrite(buzzerPin, buzzerSpeed);
}

void stopMotorIfIRDetected() {
  irSensorValue = digitalRead(irSensorPin);
  if (irSensorValue == HIGH && millis() - startTime >= 5000) {
    analogWrite(motorSpeedPin, 0);
  } else if (irSensorValue == LOW) {
    startTime = millis();
  }
}

void loop() {
  distance = measureDistance();
  controlMotorWithBuzzer();
  stopMotorIfIRDetected();
  Serial.println("D: " + String(distance) + "cm | IR: " + irSensorValue);
  delay(500);
}