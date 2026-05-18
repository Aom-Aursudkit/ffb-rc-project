#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const char *ssid = "ESP32-RC-CAR";
const char *password = "12345678";
unsigned int localPort = 4210;

WiFiUDP udp;
char packetBuffer[255];

void setup()
{
    Serial.begin(115200);
    WiFi.softAP(ssid, password, 6);
    udp.begin(localPort);
    Serial.println("Echo server ready...");
}

void loop()
{
    int packetSize = udp.parsePacket();
    if (packetSize)
    {
        int len = udp.read(packetBuffer, 255);
        if (len > 0)
        {
            // Echo back to sender immediately
            udp.beginPacket(udp.remoteIP(), udp.remotePort());
            udp.write((uint8_t*)packetBuffer, len);
            udp.endPacket();
        }
    }
}
