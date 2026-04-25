#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

// --- AP Configuration ---
const char *ssid = "ESP32-RC-CAR";
const char *password = "12345678";
unsigned int localPort = 4210;

WiFiUDP udp;
char packetBuffer[255];

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
    // Convert ADC (0-4095) to Voltage (0-3.3V)
    float voltage = (rawADC / 4095.0) * 3.3;

    // For an ACS712 (5A version) centered at 1.65V (offset)
    // Sensitivity is roughly 0.185 V/A (Check your sensor's datasheet!)
    float offsetVoltage = 1.65;
    float sensitivity = 0.185;
    float Amps = (voltage - offsetVoltage) / sensitivity;

    return Amps;
}

void setup()
{
    pixels.begin();
    pixels.setBrightness(30);
    pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // RED
    pixels.show();

    Serial.begin(115200);
    delay(2000);

    // Configure ADC
    analogReadResolution(12); // 0-4095
    pinMode(CURRENT_PIN, INPUT);

    ledcAttach(SERVO_PIN, freq, resolution);
    ledcAttach(ESC_PIN, freq, resolution);
    Serial.println("PWM Initialized on Pin 15 (Servo) and Pin 23 (ESC)");

    steerMin = map(steerLimit, 0, 180, PWM_MIN, PWM_MAX);
    steerMax = map(180 - steerLimit, 0, 180, PWM_MIN, PWM_MAX);

    throttleMin = map(-100 + throttleLimit, -100, 100, PWM_MIN, PWM_MAX);
    throttleMax = map(100 - throttleLimit, -100, 100, PWM_MIN, PWM_MAX);

    // Move servo to neutral on start
    int initialDuty = map(90, 0, 180, steerMin, steerMax);
    ledcWrite(SERVO_PIN, initialDuty);

    // ARMING ESC
    int neutralDuty = map(0, -100, 100, throttleMin, throttleMax);
    ledcWrite(ESC_PIN, neutralDuty);

    Serial.println("Configuring Access Point...");
    // Set the ESP32 to be an Access Point
    WiFi.softAP(ssid, password);

    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP); // 192.168.4.1

    udp.begin(localPort);
    Serial.println("UDP server started. Ready for controller input!");

    pixels.setPixelColor(0, pixels.Color(0, 255, 0)); // GREEN
    pixels.show();
}

void loop()
{
    
    int packetSize = udp.parsePacket();
    if (packetSize)
    {
        int len = udp.read(packetBuffer, 255);
        if (len > 0)
        {
            packetBuffer[len] = 0;

            int items = sscanf(packetBuffer, "S%f T%f", &steerValue, &throttleValue);

            if (items == 2)
            {
                // --- STEERING (Servo) ---
                int steerDuty = map((int)steerValue, 0, 180, steerMin, steerMax);
                ledcWrite(SERVO_PIN, steerDuty);

                // --- THROTTLE (ESC) ---
                int throttleDuty = map((int)throttleValue, -100, 100, throttleMin, throttleMax);
                ledcWrite(ESC_PIN, throttleDuty);

                Serial.print("Steer: ");
                Serial.print(steerValue);
                Serial.print(" | Throttle: ");
                Serial.print(throttleValue);
                Serial.print(" | ");
            }
            else
            {
                Serial.print("Raw Packet Error: ");
                Serial.print(packetBuffer);
                Serial.print(" | ");
            }
        }
    }
    currentAmps = readCurrent();
    Serial.print("Current: ");
    Serial.print(currentAmps);
    Serial.println(" A");
}