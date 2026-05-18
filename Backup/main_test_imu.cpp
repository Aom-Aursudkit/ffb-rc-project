#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BNO08x.h>

// ESP32-C6 I2C Pins
#define SDA_PIN 6
#define SCL_PIN 7

// BNO08x I2C Address (0x4A)
#define BNO08X_ADDR 0x4A

Adafruit_BNO08x bno08x(-1);
sh2_SensorValue_t sensorValue;

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10); // Wait for Serial

    Serial.println("BNO08x Test Initializing with address 0x4A...");
    
    // Initialize I2C with defined pins
    Wire.begin(SDA_PIN, SCL_PIN);

    // Initialize BNO085 with specific I2C address
    if (!bno08x.begin_I2C(BNO08X_ADDR)) {
        Serial.println("Failed to find BNO08x chip at 0x4A");
        while (1) delay(10);
    }
    Serial.println("BNO08x Found at 0x4A!");

    // Enable Rotation Vector report
    if (!bno08x.enableReport(SH2_ROTATION_VECTOR)) {
        Serial.println("Could not enable rotation vector");
    }
}

void loop() {
    if (bno08x.getSensorEvent(&sensorValue)) {
        if (sensorValue.sensorId == SH2_ROTATION_VECTOR) {
            Serial.print("Rotation Vector: ");
            Serial.print(sensorValue.un.rotationVector.real);
            Serial.print(" ");
            Serial.print(sensorValue.un.rotationVector.i);
            Serial.print(" ");
            Serial.print(sensorValue.un.rotationVector.j);
            Serial.print(" ");
            Serial.println(sensorValue.un.rotationVector.k);
        }
    }
}
