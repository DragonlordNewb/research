#define MEASUREMENT_COUNT 500

bool debug = true;

unsigned char PWR_LASER = 2;
unsigned char PWR_SENSOR = 3;
unsigned char DATA = 4;

unsigned int sensorLevel;

bool activated = true;

unsigned char data[MEASUREMENT_COUNT] = {0};
unsigned char measurement = 0;

struct Result {
  double avg;
  int sum;
};

Result dataPoint;

char usr;

Result computeDataPoint() {
  Result result;
  
  int s = 0;
  for (short i = 0; i < 1000; i++) {
    s += static_cast<double>(data[i]);
    data[i] = 0;
  }
  
  result.sum = s;
  result.avg = static_cast<double>(s) / MEASUREMENT_COUNT;

  return result;
}

void setup() {
  Serial.begin(250000);

  Serial.write("Single-sensor interferometer initializing ...\n");
  Serial.write("WARNING: LASER WILL ACTIVATE DURING INITIALIZATION!\nINITIALIZATION WILL BEGIN IN 3 SECONDS.");
  delay(3000);
  Serial.write("  Setting pinouts ...\n");
  Serial.write("    Laser power supply to OUTPUT ...");
  pinMode(PWR_LASER, OUTPUT);
  Serial.write("done.\n    Sensor power supply to OUTPUT ..."); 
  pinMode(PWR_SENSOR, OUTPUT);
  Serial.write("done.\n    Sensor data input to INPUT ...");
  pinMode(DATA, INPUT);
  Serial.write("done\n  Running diagnostics ...\n");
  
  Serial.write("    Diagnostic 1: ambient light level check.\n");    
  digitalWrite(PWR_SENSOR, HIGH);
  delay(25);
  sensorLevel = digitalRead(DATA);
  if (sensorLevel == 1) {
    Serial.write("      Diagnostic 1 PASSED.\n");
  } else {
    Serial.write("      Diagnostic 1 FAILED.\n");
    activated = false;
  }

  Serial.write("    Diagnostic 2: laser alignment check.\n");
  digitalWrite(PWR_LASER, HIGH);
  delay(25);
  sensorLevel = digitalRead(DATA);
  digitalWrite(PWR_LASER, LOW);
  digitalWrite(PWR_SENSOR, LOW);
  if (sensorLevel == 1) {
    Serial.write("      Diagnostic 2 PASSED.\n");
  } else {
    Serial.write("      Diagnostic 2 FAILED.\n");
    activated = false;
  }

  Serial.write("  Diagnostics complete.\n");
  if (activated) {
    Serial.write("Ready to collect data.");
  } else {
    Serial.write("Check all diagnostics and ensure all tests passed.\n");
  }

  if (!activated) {
    activated = debug;
  }

  if (activated) {
    Serial.write("INTERFEROMETER ACTIVE.\n");
  } else {
    Serial.write("INTERFEROMETER INACTIVE: FAILED DIAGNOSTICS.\n");
  }

  Serial.write("Press [Enter] to begin data collection.\n\n");
  while (!Serial.available()) {
    delay(1);
  }

  digitalWrite(PWR_SENSOR, HIGH);
}

void loop() {
  if ((!activated) || (debug)) {
    measurement = 0;
    for (int i = 0; i < MEASUREMENT_COUNT; i++) {
      digitalWrite(PWR_LASER, HIGH);
      while (digitalRead(DATA) == 0) {
        measurement++;
      }
      digitalWrite(PWR_LASER, LOW);
      data[i] = measurement;
      delay(25);
    }

    dataPoint = computeDataPoint();

    Serial.print("Sum: ");
    Serial.print(dataPoint.sum);
    Serial.print("\nAverage: ");
    Serial.print(dataPoint.avg);
    Serial.write("\n");
  } else {
    delay(1000);
  }
}
