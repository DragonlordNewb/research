using namespace std;

// Point of configuration: measurements per data point.

const int MEASUREMENT_COUNT = 1000;

// For if everything needs to stop.

bool ABORTED = false;

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

void setup() {
	// Set up the serial port to write data.
	Serial.begin(9600); // assume baud of 9,600
	Serial.write("Initializing interferometer ...\n");
	Serial.write("  Configuring IO pins ...\n");
	Serial.write("    Setting up control photosensor power output ...");
	pinMode(PWR_CONTROL_PHOTOSENSOR, OUTPUT);
	Serial.write("done.\n");
	Serial.write("    Setting up test photosensor power output ...");
	pinMode(PWR_TEST_PHOTOSENSOR, OUTPUT);
	Serial.write("done.\n");
	Serial.write("    Setting up test device power output ...");
	pinMode(PWR_TEST_DEVICE, OUTPUT);
	Serial.write("done.\n");
	Serial.write("    Setting up laser power output ...");
	pinMode(PWR_LASER, OUTPUT);
	Serial.write("done.\n");
	Serial.write("    Setting up control photosensor data input ...");
	pinMode(DATA_CONTROL_PHOTOSENSOR, INPUT);
	Serial.write("done\n.");
	Serial.write("    Setting up test photosensor data input ...");
	pinMode(DATA_TEST_PHOTOSENSOR, INPUT);
	Serial.write("done.\n");
	Serial.write("  IO pins configured.\n");
	Serial.write("  Running basic calibration tests ...");
	Serial.write("    Checking ambient light levels on control photosensor ...");
	if (digitalRead(DATA_CONTROL_PHOTOSENSOR) == 0) {
		Serial.write("SYSTEM FAILURE.\n    Ambient light level too high, cannot activate interferometer.");
		ABORTED = true;
		return 1;
	}
	Serial.write("system nominal.\n");
	Serial.write("    Checking ambient light levels on test photosensor ...");
	if (digitalRead(DATA_TEST_PHOTOSENSOR) == 0) {
		Serial.write("SYSTEM FAILURE.\n    Ambient light level too high, cannot activate interferometer.");
		ABORTED = true;
		return 2;
	}
	Serial.write("system nominal.\n");
	Serial.write("    Checking laser alignment (warning: laser will power on momentarily) ...");
	delay(3000);
	digitalWrite(PWR_LASER, HIGH);
	delay(100);
	if (digitalRead(DATA_CONTROL_PHOTOSENSOR) + digitalRead(DATA_TEST_PHOTOSENSOR) > 0) {
		Serial.write("SYSTEM FAILURE.\n    Laser not properly aligned to target, ensure laser is aligned and restart.");
		ABORTED = true;
		return 3;
	}
	digitalWrite(PWR_LASER, LOW);
	Serial.write("system nominal.\n");
	Serial.write("  All systems go.");
	Serial.write("Ready to activate interferometer. Measurements will begin momentarily.\n");
	Serial.write("Warning: laser hazard. Do not look directly into the laser beam.\n\n");
	delay(5000);
}

void loop() {}