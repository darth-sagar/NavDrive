#include <Servo.h>

Servo steering_servo;

// ct6b Receiver Pins
const int throttle_pin = 3;  // CT6B Channel 3 to pin 3
const int steering_pin = 4;  // CT6B Channel 1 to pin 4

#define EN_LEFT 6    // LEFT motor PWM
#define IN1 7        // LEFT motor forward
#define IN2 8        // LEFT motor backward
#define EN_RIGHT 11  // RIGHT motor PWM
#define IN3 9        // RIGHT motor forward
#define IN4 10       // RIGHT motor backward

// Calibration values form the ct6b txr

const long throttle_min = 1090;
const long throttle_max = 1860;
const long steering_min = 1075;
const long steering_max = 1943;

// Dead zone threshold
const float DEAD_ZONE_LOW = -0.05;
const float DEAD_ZONE_HIGH = 0.05;

// Servo parameters
const int SERVO_CENTER = 1515;
const int SERVO_RANGE = 603;  // ±145° range (≈603µs)
const int STEERING_SERVO_PIN = 2;

// for speed control i would call this speed control reduction factor
const float Speed_control = 0.50;

const float DEADZONE_THRESHOLD = 0.10;  // Below this absolute value, no movement
const int MIN_PWM = 100;                // Increased minimum PWM to overcome friction
const float RESPONSE_CURVE = 1.1;       // Exponential response factor (1.0=linear)

void setup() {
  Serial.begin(115200);
  // servo attach
  steering_servo.attach(STEERING_SERVO_PIN);

  // Initialize receiver pins
  pinMode(throttle_pin, INPUT);
  pinMode(steering_pin, INPUT);

  // Initialize motor control pins
  pinMode(EN_LEFT, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(EN_RIGHT, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  // Read raw PWM values
  unsigned long THROTTLE_RAW = pulseIn(throttle_pin, HIGH, 25000);
  unsigned long STEERING_RAW = pulseIn(steering_pin, HIGH, 25000);

  // Check for transmitter disconnection
  if (THROTTLE_RAW == 0 || STEERING_RAW == 0) {
    Serial.println("Transmitter disconnected!");
    stopMotors();
    delay(100);
    return;
  }

  // Normalize values
  float Throttle_Normalised = mapFloat(THROTTLE_RAW, throttle_min, throttle_max, -1.0, 1.0);
  float Steering_Normalised = mapFloat(STEERING_RAW, steering_min, steering_max, 1.0, -1.0);

  // Apply dead zone for noise in the ct6b txr (normalising)
  if (abs(Throttle_Normalised) < DEAD_ZONE_HIGH) {
    Throttle_Normalised = 0;
  }
  if (abs(Steering_Normalised) < DEAD_ZONE_HIGH) {
    Steering_Normalised = 0;
  }

  // Drive motors
  driveMotors(Throttle_Normalised, Steering_Normalised);

  // Print values via the function for the serial Monitor
  printvalues(Throttle_Normalised, Steering_Normalised);
}

void driveMotors(float Throttle_Normalised, float Steering_Normalised) {
  // Handle servo steering
  int servoPos = SERVO_CENTER + (Steering_Normalised * SERVO_RANGE);
  servoPos = constrain(servoPos, SERVO_CENTER - SERVO_RANGE, SERVO_CENTER + SERVO_RANGE);
  steering_servo.writeMicroseconds(servoPos);

// Calculate absolute throttle and apply deadzone
  float absThrottle = abs(Throttle_Normalised);
  int throttle_PWM = 0;

  if (absThrottle > DEADZONE_THRESHOLD) {
    // Apply exponential response curve
    float normalized = (absThrottle - DEADZONE_THRESHOLD) / (1.0 - DEADZONE_THRESHOLD);
    float curved = pow(normalized, RESPONSE_CURVE);
    throttle_PWM = MIN_PWM + (255 - MIN_PWM) * curved;
  }
  
  throttle_PWM = constrain(throttle_PWM, 0, 255);

  // Set motor directions
  if (Throttle_Normalised > DEADZONE_THRESHOLD) {
    // Forward
    forward();
  } else if (Throttle_Normalised < -DEADZONE_THRESHOLD) {
    // Reverse
    reverse();
  } else {
    // Stop
    stop();
  }

  analogWrite(EN_LEFT, throttle_PWM);
  analogWrite(EN_RIGHT, throttle_PWM);
}
void forward(){
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}
void reverse(){
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
}
void stop(){
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}
void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(EN_LEFT, 0);
  analogWrite(EN_RIGHT, 0);
}

// Mapping function to Normalise the values coming form the ct6b Rxr-Txr

float mapFloat(long value, long in_min, long in_max, float out_min, float out_max) {
  return (float)(value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// function to Print values on the Output Screen actaully on the Serial Monitor

void printvalues(float Throttle_Normalised, float Steering_Normalised) {
  Serial.print("THROTTLE : ");
  Serial.print(Throttle_Normalised);
  Serial.print(" | STEERING : ");
  Serial.println(-Steering_Normalised);
  delay(10);  // Reduced delay for python hell ya
}