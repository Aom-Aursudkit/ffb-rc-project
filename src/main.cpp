#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <Adafruit_BNO08x.h>
#include "HX711.h"

// --- AP Configuration ---
const char *ssid = "ESP32-RC-CAR";
const char *password = "12345678";
unsigned int localPort = 4210;

WiFiUDP udp;
char packetBuffer[255];

// --- IMU Configuration ---
#define SDA_PIN 6
#define SCL_PIN 7
#define BNO08X_ADDR 0x4A
Adafruit_BNO08x bno08x(-1);
sh2_SensorValue_t sensorValue;

// IMU Data variables
float linAccX, linAccY, linAccZ; 
float gyroX, gyroY, gyroZ;       

// --- Load Cell Configuration ---
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 18;
HX711 scale;
const float LOADCELL_SCALE = 210; // Calculated from your test

float steerValue = 90.0;   // Default Neutral
float throttleValue = 0.0; // Default Stop
int steerLimit = 20;       // Degrees to trim off each end
int throttleLimit = 90;    // Percent to trim off each end
const int PWM_MIN = 410;   // Theoretical 0 degree duty
const int PWM_MAX = 1966;  // Theoretical 180 degree duty
int steerMin = 410;
int steerMax = 1966;
int throttleMin = 410;
int throttleMax = 1966;

// Pins
#define SERVO_PIN 15
#define ESC_PIN 23
#define RGB_PIN 8 // Built-in LED pin for C6
#define NUMPIXELS 1
#define CURRENT_PIN 4

// PWM Properties
const int freq = 50;
const int resolution = 14;

Adafruit_NeoPixel pixels(NUMPIXELS, RGB_PIN, NEO_GRB + NEO_KHZ800);

// Current Sensor
float currentAmps = 0.0;

float readCurrent()
{
    int rawADC = analogRead(CURRENT_PIN);
    float voltage = (rawADC / 4095.0) * 3.3;
    float offsetVoltage = 1.65;
    float sensitivity = 0.185;
    float Amps = (voltage - offsetVoltage) / sensitivity;
    return Amps;
}

// Function to move to a target slowly and measure every degree
void slowMoveAndMeasure(int targetAngle) {
    int startAngle = (int)steerValue;
    int step = (startAngle < targetAngle) ? 1 : -1;
    
    unsigned long lastStepTime = 0;
    const int stepDelay = 25; // How often to change the angle (ms)

    while (startAngle != targetAngle) {
        if (millis() - lastStepTime >= stepDelay) {
            startAngle += step;
            steerValue = startAngle;
            int duty = map(startAngle, 0, 180, steerMin, steerMax);
            ledcWrite(SERVO_PIN, duty);
            lastStepTime = millis();
        }

        float amps = readCurrent();
        Serial.print(millis());
        Serial.print(",");
        Serial.print(startAngle);
        Serial.print(",");
        Serial.println(amps, 3);
        yield(); 
    }
}

void test_current_sensor(){
    int duty = map(90, 0, 180, steerMin, steerMax);
    ledcWrite(SERVO_PIN, duty);
    delay(100);
    // SEQUENCE: Middle(90) -> Right(180) -> Left(0) -> Middle(90)
    slowMoveAndMeasure(180);
    delay(500); // Pause at extreme
    slowMoveAndMeasure(0);
    delay(500); // Pause at extreme
    slowMoveAndMeasure(90);
}

void setup()
{
    Serial.begin(115200);
    while (!Serial) delay(10); // Wait for Serial
    pixels.begin();
    pixels.setBrightness(30);
    pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // RED
    pixels.show();

    // 1. Initialize IMU
    Wire.begin(SDA_PIN, SCL_PIN);
    delay(500);
    if (!bno08x.begin_I2C(BNO08X_ADDR)) {
        Serial.println("Failed to find BNO08x chip at 0x4A!");
    } else {
        Serial.println("BNO08x Found!");
        bno08x.enableReport(SH2_LINEAR_ACCELERATION);
        bno08x.enableReport(SH2_GYROSCOPE_CALIBRATED);
    }
    
    // 2. Initialize Load Cell
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale.set_scale(LOADCELL_SCALE);
    scale.tare();

    delay(2000);
    analogReadResolution(12);
    pinMode(CURRENT_PIN, INPUT);

    ledcAttach(SERVO_PIN, freq, resolution);
    ledcAttach(ESC_PIN, freq, resolution);

    steerMin = map(steerLimit, 0, 180, PWM_MIN, PWM_MAX);
    steerMax = map(180 - steerLimit, 0, 180, PWM_MIN, PWM_MAX);
    throttleMin = map(-100 + throttleLimit, -100, 100, PWM_MIN, PWM_MAX);
    throttleMax = map(100 - throttleLimit, -100, 100, PWM_MIN, PWM_MAX);

    ledcWrite(SERVO_PIN, map(90, 0, 180, steerMin, steerMax));
    ledcWrite(ESC_PIN, map(0, -100, 100, throttleMin, throttleMax));

    WiFi.softAP(ssid, password, 6);
    udp.begin(localPort);
    
    pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // GREEN
    pixels.show();
    Serial.println("System Ready.");
}

void loop()
{
    // Read IMU Data
    if (bno08x.getSensorEvent(&sensorValue)) {
        if (sensorValue.sensorId == SH2_LINEAR_ACCELERATION) {
            linAccX = sensorValue.un.linearAcceleration.x;
            linAccY = sensorValue.un.linearAcceleration.y;
            linAccZ = sensorValue.un.linearAcceleration.z;
        } else if (sensorValue.sensorId == SH2_GYROSCOPE_CALIBRATED) {
            gyroX = sensorValue.un.gyroscope.x;
            gyroY = sensorValue.un.gyroscope.y;
            gyroZ = sensorValue.un.gyroscope.z;
        }
    }

    // Read Load Cell
    float loadCellGrams = scale.is_ready() ? scale.get_units(1) : 0.0;

    int packetSize = udp.parsePacket();
    if (packetSize)
    {
        int len = udp.read(packetBuffer, 255);
        if (len > 0)
        {
            packetBuffer[len] = 0;
            if (sscanf(packetBuffer, "S%f T%f", &steerValue, &throttleValue) == 2)
            {
                // --- STEERING (Servo) ---
                int steerDuty = map((int)steerValue, 0, 180, steerMin, steerMax);
                ledcWrite(SERVO_PIN, steerDuty);

                // --- THROTTLE (ESC) ---
                int throttleDuty = map((int)throttleValue, -100, 100, throttleMin, throttleMax);
                ledcWrite(ESC_PIN, throttleDuty);
                
                // Send IMU + Load Cell data back to PC
                // Format: A[x,y,z]G[x,y,z]L[loadcell]
                String imuData = "A" + String(linAccX, 2) + "," + String(linAccY, 2) + "," + String(linAccZ, 2) + 
                                 "G" + String(gyroX, 2) + "," + String(gyroY, 2) + "," + String(gyroZ, 2) +
                                 "L" + String(loadCellGrams, 1);
                udp.beginPacket(udp.remoteIP(), udp.remotePort());
                udp.print(imuData);
                udp.endPacket();
            }
        }
    }
}
