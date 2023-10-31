// Arduino Uno driver code to run a modified Michelson-Morley dual-sensor interferometer.
//
// Constants can be adjusted as per any particular interferometer's construction but the
// program should work either way.

// Point of configuration: how many repetitions to run per data point emitted by the WFI.
// Defaults to 100, so that each data point is an aggregate average of 100 individual
// measurements.
const unsigned char MEASUREMENT_COUNT = 100;

// Data array. Each int represents the time delay since the laser was activated.
unsigned int data[MEASUREMENT_COUNT];

// Pin configurations. Can be changed as necessary.
const char PWR_LASER = 2;    // Laser power output
const char PWR_CONTROL = 3;  // Control photosensor power output
const char PWR_TEST = 4;     // Test photosensor power output
const char DATA_CONTROL = 5; // Control photosensor data input
const char DATA_TEST = 6;    // Test photosensor data input

// Stuff for inside functions - so that memory usage is accurately calculated.
// Add a byte for "for" loops inside the takeMeasurement function.
char powerPin;
unsigned long long sum = 0;
unsigned int count = 0;

double takeMeasurement(const char dataPin) {
  if (dataPin == 5) {
    powerPin = 3;
  } else if (dataPin == 6) {
    powerPin = 4;
  } else {
    return 0;
  }

  digitalWrite(powerPin, HIGH);

  for (char i = 0; i < MEASUREMENT_COUNT; i++) {
    count = 0;
    digitalWrite(PWR_LASER, HIGH);
    while (digitalRead(dataPin) == 1) {
      count += 1;
    }
    digitalWrite(PWR_LASER, LOW);
    delay(25);

    data[i] = count;
  }

  digitalWrite(powerPin, LOW);

  sum = 0;
  for (char i = 0; i < MEASUREMENT_COUNT; i++) {
    sum += data[i];
  }

  return static_cast<double>(sum) / MEASUREMENT_COUNT;
}

void setup() {
  Serial.begin(9600);

  pinMode(PWR_LASER, OUTPUT);
  pinMode(PWR_CONTROL, OUTPUT);
  pinMode(PWR_TEST, OUTPUT);
  pinMode(DATA_CONTROL, INPUT);
  pinMode(DATA_TEST, INPUT);
}

void loop() {
  Serial.println(takeMeasurement(5));
}