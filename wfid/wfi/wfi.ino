// Arduino Uno driver code to run a modified Michelson-Morley dual-sensor interferometer.
//
// Constants can be adjusted as per any particular interferometer's construction but the
// program should work either way.

// Point of configuration: how many repetitions to run per data point emitted by the WFI.
// Defaults to 100, so that each data point is an aggregate average of 100 individual
// measurements.
const char NUM_REPETITIONS = 100;

// Several basic constants to handle serial responses, delimetry, etc.
const char COMMAND_ACCEPTED = 0;
const char COMMAND_INVALID = 1;

const char 

// Data array which stores measurements before data is outputted to the master computer.
int data[NUM_REPETITIONS];

void transferRawData

void setup() {
	Serial.begin(9600);
}

void loop() {
	if (Serial.available() > 0) {
		int command = Serial.parseInt();  // Read an integer from the serial port

		if (command >= 0 && command <= 255) {
		// Here, you can perform actions based on the received command
		// For example:
		switch (command) {
			case 0:
			// Do something for command 0
			break;
			case 1:
			// Do something for command 1
			break;
			// Add more cases for other commands as needed
		}
		} else {
		// Invalid command, handle it here
		Serial.write(INVALID_COMMAND);
		}
	}
}