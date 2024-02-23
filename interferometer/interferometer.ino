// Code used to run the warp field interferometer used in the experiment.
//
// This code is placed in the public domain for anyone to use. Written 2024
// by Lux Bodell. May not work on all Arduino models; compiled for an Arduino
// Uno connected to appropriate components.

// --- Setup --- //

// Parameters specified by directive instead of variable to save very 
// valuable storage space - Arduino Uno has only 2048 B of RAM.
//
// These can be changed as needed.
#define READING_COUNT 100 // how many readings per measurement?
#define SERIAL_BAUD 9600   // baud rate of serial port?
#define USING_TEST true   // using the test sensor or just control sensor?
#define READING_DELAY 50   // delay between readings

// Pin numbers specified by directive too.
//
// These can be changed as needed.
#define LASER_PWR 2 // connected to laser voltage input - digital I/O pin
#define CTRL_PWR 3  // connected to control sensor voltage input - digital I/O pin
#define CTRL_DATA 4 // connected to control sensor data output
#define TEST_PWR 5  // connected to test sensor voltage input
#define TEST_DATA 6 // connected to test sensor data output

// Variables that are used over the course of data collection.
unsigned int readings[READING_COUNT];
unsigned int readingNumber = 0;
unsigned int reading = 0;
unsigned int sum = 0;

// --- Main body --- //

double computeDataPoint() {
	// Compute the average of all the readings to give a single data point.
	sum = 0;
	for (readingNumber = 0; readingNumber < READING_COUNT; readingNumber++) {
		sum += readings[readingNumber];
	}
	return (double)(sum) / READING_COUNT;
}

void setup() {
	// Set up input and output pins and initialize the serial port.

	Serial.begin(SERIAL_BAUD);

	pinMode(LASER_PWR, OUTPUT);
	pinMode(CTRL_PWR, OUTPUT);
	pinMode(TEST_PWR, OUTPUT);

	pinMode(CTRL_DATA, INPUT);
	pinMode(TEST_DATA, INPUT);

  digitalWrite(CTRL_PWR, HIGH);
  digitalWrite(TEST_PWR, HIGH);

  Serial.write("using test: ");
  Serial.print(USING_TEST);
  Serial.write("\n");
}

void loop() {

	// Collect interferometric data as well as local atmospheric conditions.

	if (USING_TEST) {

		// ... if using the test sensor,

		for (readingNumber = 0; readingNumber < READING_COUNT; readingNumber++) {
      reading = 0;

			// activate the laser,
			digitalWrite(LASER_PWR, HIGH);
			
			// wait for the control sensor to trip,
			while (digitalRead(CTRL_DATA) == 1);

			// then count ticks until the test sensor trips,
			while (digitalRead(TEST_DATA) == 1) { reading++; }

			// then disable the laser,
			digitalWrite(LASER_PWR, LOW);

			// record the tick count as a single reading (one of READING_COUNT),
			readings[readingNumber] = reading;

			// and wait READING_DELAY ms for the laser to cool down.
			delay(READING_DELAY);
		}

	} else {

		// if using just the control sensor for calibration, 

		for (readingNumber = 0; readingNumber < READING_COUNT; readingNumber++) {
      reading = 0;

			// activate the laser,
			digitalWrite(LASER_PWR, HIGH);

			// count ticks until the control sensor trips,
			while (digitalRead(CTRL_DATA) == 1) { reading++; }

			// then disable the laser,
			digitalWrite(LASER_PWR, LOW);

			// record the tick count as a single reading (one of READING_COUNT),
			readings[readingNumber] = reading;

			// and wait READING_DELAY ms for the laser to cool down.
			delay(READING_DELAY);
		}

	}

	// Report findings
	Serial.print(computeDataPoint());
	Serial.write("\n\r");

}