// Double-sensor direct interferometer driver code!

const char RAW_DATA_ARRAY_SIZE = 100;
int DIAGNOSTIC_REPETITION = 1000;
bool PASSED_DIAGNOSTIC = true;

char PWR_LASER = 2;
char PWR_S_CTRL = 3;
char PWR_S_TEST = 4;
char PWR_DRIVE = 5;
char DATA_CTRL = 6;
char DATA_TEST = 7;
char ALARM_BUZZ = 8;
char ALARM_LAMP = 9;

unsigned int RAW_DATA[RAW_DATA_ARRAY_SIZE] = {0};

unsigned int stopwatch = 0;

struct Result {
  unsigned int sum = 0;
  double avg = 0.0;
};

Result res;

Result processRawData() {
  Result result;
  for (int i = 0; i < RAW_DATA_ARRAY_SIZE; i++) {
    result.sum += RAW_DATA[i];
  }
  result.avg = static_cast<double>(result.sum) / RAW_DATA_ARRAY_SIZE;
  return result;
}

void waitForActivation() {
  while (!Serial.available());
  Serial.read();
}

bool ambientLightLevelTest(char pwr, char data) {
  digitalWrite(pwr, HIGH);
  delay(50);
  PASSED_DIAGNOSTIC = true;
  for (int i = 0; i < DIAGNOSTIC_REPETITION; i++) {
    if (digitalRead(data) == 0) {
      PASSED_DIAGNOSTIC = false;
      break;
    }
  }
  digitalWrite(pwr, LOW);
  return PASSED_DIAGNOSTIC;
}

void setup() {
  Serial.begin(9600);
  Serial.write("WFI double sensor driver code loaded.\nFor safety, [ENTER] must be pressed in between stages of activation.\nPress [ENTER] to begin pin configuration.");
  waitForActivation();
  Serial.write("  Configuring pins ...");

  pinMode(PWR_LASER, OUTPUT);
  pinMode(PWR_S_CTRL, OUTPUT);
  pinMode(PWR_S_TEST, OUTPUT);
  pinMode(PWR_DRIVE, OUTPUT);
  pinMode(DATA_CTRL, INPUT);
  pinMode(DATA_TEST, INPUT);
  pinMode(ALARM_BUZZ, OUTPUT);
  pinMode(ALARM_LAMP, OUTPUT);

  Serial.write("done.\n  All pins correctly configured.\nPress [ENTER] to begin system diagnostics and activate the laser.\n");
  waitForActivation();

  Serial.write("  WARNING, diagnostics will activate the laser and will begin in 5 seconds ...\n");
  for (char i = 0; i < 5; i++) {
    tone(ALARM_BUZZ, 440, 500);
    digitalWrite(ALARM_LAMP, HIGH);
    delay(500);
    digitalWrite(ALARM_LAMP, LOW);
    delay(500);
  }
  digitalWrite(ALARM_LAMP, HIGH);
  
  Serial.write("  Running diagnostics ...\n    Diagnostic 1: ambient control sensor light level ...");
  if (ambientLightLevelTest(PWR_S_CTRL, DATA_CTRL)) {
    Serial.write("control sensor responding incorrectly: failed.\n");
  } else {
    Serial.write("control sensor responding correctly: passed.\n");
  }

  Serial.write("    Diagnostic 2: ambient test sensor light level ...");
  if (ambientLightLevelTest(PWR_S_TEST, DATA_TEST)) {
    Serial.write("test sensor responding incorrectly: failed.\n");
  } else {
    Serial.write("test sensor responding correctly: passed.\n");
  }

  Serial.write("    Diagnostic 3: control beam alignment test ...");
  digitalWrite(PWR_LASER, HIGH);
  digitalWrite(PWR_S_CTRL, HIGH);
  digitalWrite(PWR_S_TEST, HIGH);
  delay(50);

  if (digitalRead(DATA_CTRL) > 0) {
    Serial.write("beam out of alignment with control sensor: failed.\n");
  } else {
    Serial.write("beam aligned with control sensor: passed.\n");
  }

  Serial.write("    Diagnostic 4: test beam alignment test ...");

  if (digitalRead(DATA_TEST) > 0) {
    Serial.write("beam out of alignment with test sensor: failed.\n");
  } else {
    Serial.write("beam aligned with test sensor: passed.\n");
  }

  digitalWrite(PWR_LASER, LOW);
  digitalWrite(PWR_S_CTRL, LOW);
  digitalWrite(PWR_S_TEST, LOW);
  digitalWrite(ALARM_LAMP, LOW);

  Serial.write("  Diagnostics complete.\nPlease review diagnostic information and press [ENTER] to proceed ONLY IF ALL DIAGNOSTICS PASSED.\n");
  waitForActivation();
  digitalWrite(PWR_S_CTRL, HIGH);
  digitalWrite(PWR_S_TEST, HIGH);

  for (char i = 0; i < 5; i++) {
    tone(ALARM_BUZZ, 440, 500);
    digitalWrite(ALARM_LAMP, HIGH);
    delay(500);
    digitalWrite(ALARM_LAMP, LOW);
    delay(500);
  }
}

void loop() {
  Serial.write("Collecting data point ...\n  Collecting raw data points ...");
  for (char i = 0; i < RAW_DATA_ARRAY_SIZE; i++) {
    stopwatch = 0;
    digitalWrite(PWR_LASER, HIGH);
    while (digitalRead(DATA_CTRL) == 1);
    while (digitalRead(DATA_TEST) == 1) { stopwatch++; }
    digitalWrite(PWR_LASER, LOW);
    RAW_DATA[i] = stopwatch;
    delay(50);
  }
  Serial.write("done.\n  Calculating results ...");
  res = processRawData();
  Serial.write("done, sum: ");
  Serial.print(res.sum);
  Serial.write(", avg: ");
  Serial.print(res.avg);
  Serial.write("\n\n");
}
