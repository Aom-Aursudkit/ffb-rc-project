#include <WiFi.h>

// ======= HARDWARE CONFIGURATION ======
const int SERVO_PIN = 15;
const int CURRENT_PIN = 4;

const char* SSID = "ESP32-RC-CAR";
const char* PASSWORD = "12345678";
const int UDP_PORT = 4210;

// ======= TEST MODE ======
// 0 = IDLE test (servo at middle)
// 1 = SWEEP test (steering sweep left-right-middle)
#define TEST_MODE 0

// ======= PWM CONFIGURATION ======
const int PWM_FREQ = 50;
const int PWM_RESOLUTION = 14;
const int PWM_MIN = 410;
const int PWM_MAX = 1966;

// ======= STEERING CONFIGURATION ======
const int STEERING_MIDDLE = 90;
const int STEERING_LEFT = 30;
const int STEERING_RIGHT = 150;

const unsigned long CYCLE_PERIOD = 3000;

// ======= GLOBAL VARIABLES ======
WiFiUDP udp;
unsigned long cycleStartTime = 0;
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL = 20;

int analogOffset = 0;
int targetAngle = STEERING_MIDDLE;
bool done = false;

// ======= FUNCTIONS ======

void setSteeringAngle(int angle) {
  angle = constrain(angle, 0, 180);
  int duty = map(angle, 0, 180, PWM_MIN, PWM_MAX);
  ledcWrite(SERVO_PIN, duty);
}

void calibrateCurrentSensor() {
  long sum = 0;
  for (int i = 0; i < 100; i++) {
    sum += analogRead(CURRENT_PIN);
    delay(10);
  }
  analogOffset = sum / 100;
  Serial.print("Current sensor offset: ");
  Serial.println(analogOffset);
}

float readCurrent() {
  int rawADC = analogRead(CURRENT_PIN);
  float voltage = (rawADC / 4095.0) * 3.3;
  float current = (voltage - 1.65) / 0.185;
  return current;
}

void sendTelemetryUDP(int angle, float current) {
  char packet[128];
  sprintf(packet, "S%dI%.3f", angle, current);
  udp.beginPacket(udp.remoteIP(), UDP_PORT);
  udp.print(packet);
  udp.endPacket();
}

void logToSerial(int angle, float current, unsigned long timestamp) {
  Serial.print(timestamp);
  Serial.print(",");
  Serial.print(angle);
  Serial.print(",");
  Serial.println(current, 3);
}

void updateSteeringPhase(unsigned long elapsed) {
  float progress = (float)elapsed / CYCLE_PERIOD;
  int newAngle = STEERING_MIDDLE;

  if (progress < 0.15) {
    float t = progress / 0.15;
    newAngle = STEERING_MIDDLE + (STEERING_LEFT - STEERING_MIDDLE) * t;
  }
  else if (progress < 0.25) {
    newAngle = STEERING_LEFT;
  }
  else if (progress < 0.40) {
    float t = (progress - 0.25) / 0.15;
    newAngle = STEERING_LEFT + (STEERING_RIGHT - STEERING_LEFT) * t;
  }
  else if (progress < 0.50) {
    newAngle = STEERING_RIGHT;
  }
  else if (progress < 0.65) {
    float t = (progress - 0.50) / 0.15;
    newAngle = STEERING_RIGHT + (STEERING_MIDDLE - STEERING_RIGHT) * t;
  }
  else {
    newAngle = STEERING_MIDDLE;
  }

  targetAngle = (int)newAngle;
}

void setup() {
  Serial.begin(115200);
  delay(500);

  analogReadResolution(12);
  pinMode(CURRENT_PIN, INPUT);

  ledcAttach(SERVO_PIN, PWM_FREQ, PWM_RESOLUTION);
  calibrateCurrentSensor();

  setSteeringAngle(STEERING_MIDDLE);
  delay(500);

  WiFi.softAP(SSID, PASSWORD);
  Serial.println("WiFi AP started");
  Serial.print("IP: ");
  Serial.println(WiFi.softAPIP());

  udp.begin(UDP_PORT);

  cycleStartTime = millis();
  lastTelemetryTime = cycleStartTime;

#if TEST_MODE == 0
  Serial.println("mode,time_ms,current_A");
#else
  Serial.println("timestamp_ms,angle_deg,current_A");
#endif
}

void loop() {
  if (done) return;

  unsigned long currentTime = millis();
  unsigned long elapsed = currentTime - cycleStartTime;

#if TEST_MODE == 0
  // IDLE test - just measure current at middle
  if (elapsed >= 5000) {  // 5 seconds
    done = true;
    return;
  }

  float current = readCurrent();
  logToSerial(0, current, elapsed);

#else
  // SWEEP test - steering sweep
  if (elapsed >= CYCLE_PERIOD) {
    done = true;
    setSteeringAngle(STEERING_MIDDLE);
    return;
  }

  updateSteeringPhase(elapsed);
  setSteeringAngle(targetAngle);

  float current = readCurrent();

  if (currentTime - lastTelemetryTime >= TELEMETRY_INTERVAL) {
    sendTelemetryUDP(targetAngle, current);
    lastTelemetryTime = currentTime;
  }

  logToSerial(targetAngle, current, elapsed);
#endif

  delay(10);
}