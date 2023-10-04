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

unsigned long long acquireDataPoint(const char sensorPin) {

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

void writeUDL(unsigned long long x) {
	// By default, Arduino microcontrollers can't actually write
	// "unsigned long long" data types to Serial. This function
	// breaks it up into eight chars and prints it one byte at a
	// time.
	//
	// Right shifts and one-byte masking are used to achieve this.
	//
	//	(char)((x >> (8 * n)) & 0xFF)
	//
	// returns the nth byte of x as a char by shifting the value
	// 8 * n bits to the right and then running a bitmask of just
	// the last 8 bits.

	Serial.print((char)((x >> 0 ) & 0xFF));
	Serial.print((char)((x >> 8 ) & 0xFF));
	Serial.print((char)((x >> 16) & 0xFF));
	Serial.print((char)((x >> 24) & 0xFF));
	Serial.print((char)((x >> 32) & 0xFF));
	Serial.print((char)((x >> 40) & 0xFF));
	Serial.print((char)((x >> 48) & 0xFF));
	Serial.print((char)((x >> 56) & 0xFF));
}

void setup() {}

void loop() {}