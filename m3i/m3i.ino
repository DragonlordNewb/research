using namespace std;

// Point of configuration: measurements per data point.

const int MEASUREMENT_COUNT = 1000;

// Pin numbers for the devices in question.

const char PWR_CONTROL_PHOTOSENSOR = 2;
const char PWR_TEST_PHOTOSENSOR = 3;
const char PWR_LASER = 4;
const char PWR_TEST_DEVICE = 5;

const char DATA_CONTROL_PHOTOSENSOR = 6;
const char DATA_TEST_PHOTOSENSOR = 7;

// Data analysis variables.

// On an Arduino microcontroller, an
// "unsigned long long int" is an 8-byte number,
// which was selected so that overflow is not
// a problem.

// Since these variables take up a very large data volume,
// they are stored in flash memory rather than in RAM
// which for the purposes of the interferometer experiment
// needs to be running as fast as possible.

unsigned long long data[MEASUREMENT_COUNT] = {};
unsigned long long stopwatch = 0;

unsigned long long computeResult() {

    unsigned long long sum = 0;

    for (int i = 0; i < MEASUREMENT_COUNT; i++) {
        sum += data[i];
    }

    return sum / static_cast<unsigned long long>(MEASUREMENT_COUNT);
}

// Data acquisition functions.

unsigned long long int acquireDataPoint(const char sensorPin) {

    // Power on the desired sensor and wait for a moment.
    digitalWrite(sensorPin, HIGH);
    delay(25);

    // For the desired number of repetitions in measurement:
    for (int i = 0; i < MEASUREMENT_COUNT; i++) {
        
        // Power on the laser ...
        digitalWrite(PWR_LASER, HIGH);

        // ... then, as fast as possible, increment "stopwatch" ...
        while (digitalRead(sensorPin) == 1) {
            stopwatch += 1;
        }

        // ... until the sensor goes off, at which point, the
        // value of stopwatch is placed in the data array for later
        // output.
        digitalWrite(PWR_LASER, LOW);
        data[i] = stopwatch;
    }

    return computeResult();

}

void setup() {}

void loop() {}