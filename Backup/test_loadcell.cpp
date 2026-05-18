#include <Arduino.h>
#include "HX711.h"

// HX711 Pin Configuration - Adjust these to your wiring
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 18;

HX711 scale;

void setup() {
  Serial.begin(115200);
  Serial.println("HX711 Calibration Test");
  
  // Initialize the HX711
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  
  // Set scale to 1 to get raw readings initially
  scale.set_scale();
  
  // Tare: Reset to 0 (make sure nothing is on the load cell at startup)
  Serial.println("Ensure no weight on the load cell...");
  delay(2000);
  scale.tare(); 
  Serial.println("Tared. Now place a known weight (e.g., 500g) on the load cell.");
  delay(2000);
}

void loop() {
  if (scale.is_ready()) {
    // Get raw reading (average of 10 samples)
    long reading = scale.get_value(10); 
    Serial.print("Raw Reading: ");
    Serial.println(reading);
  } else {
    Serial.println("HX711 not found.");
  }
  delay(500);
}
