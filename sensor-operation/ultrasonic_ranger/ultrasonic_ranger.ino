#include <Wire.h>
#include "Ultrasonic.h"

#define RANGE_SENSORS 4

struct RangeSensor{
  int id;
  int port;
};

struct RangeSensor range_sensors[RANGE_SENSORS];

void initialize_range_sensor(int idx, int id, int port) {
  range_sensors[idx].id = id;
  range_sensors[idx].port = port;
}

void setup() {
  initialize_range_sensor(0, 1, 5);
  initialize_range_sensor(1, 2, 6);
  initialize_range_sensor(2, 3, 7);
  initialize_range_sensor(3, 4, 8);
  Serial.begin(9600);
}

void loop() {
  for(int i=0; i<RANGE_SENSORS; i++) {
    Ultrasonic ultrasonic(range_sensors[i].port);
    int centimeters = ultrasonic.MeasureInCentimeters();
    Serial.print(range_sensors[i].id);
    Serial.print(" ");
    Serial.println(centimeters);
  }
  delay(500);
}
