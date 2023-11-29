// Double-sensor direct interferometer driver code!

const char RAW_DATA_ARRAY_SIZE = 100;
int DIAGNOSTIC_REPETITION = 1000;
bool PASSED_DIAGNOSTIC = true;

char PWR_LASER = 2;
char PWR_S_CTRL = 3;
char PWR_S_TEST = 4;
char PWR_D_CORE = 5;
char PWR_D_SHELL = 6;
char DATA_CTRL = 7;
char DATA_TEST = 8;
char DATA_D_CORE = 9;
char DATA_D_SHELL = 10;
char ALARM_BUZZ = 11;
char ALARM_LAMP = 12;

char RAW_DATA[RAW_DATA_ARRAY_SIZE] = {0};

struct Result {
  int sum = 0;
  double avg = 0.0d;
};

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
  pinMode(PWR_D_CORE, OUTPUT);
  pinMode(PWR_D_SHELL, OUTPUT);
  pinMode(DATA_CTRL, INPUT);
  pinMode(DATA_TEST, INPUT);
  pinMode(DATA_D_CORE, INPUT);
  pinMode(DATA_D_SHELL, INPUT);
  pinMode(ALARM_BUZZ, OUTPUT);
  pinMode(ALARM_LAMP, OUTPUT);

  Serial.write("done.\n  All pins correctly configured.\nPress [ENTER] to begin system diagnostics and activate the laser.\n");
  waitForActivation();

  Serial.write("WARNING, diagnostics will activate the laser and will begin in 3 seconds ...");
  delay(3000);
  
  Serial.write("  Running diagnostics ...\n    Diagnostic 1: ambient control sensor light level ...");
  if (ambientLightLevelTest(PWR_S_CTRL, DATA_CTRL)) {
    Serial.write("control sensor responding correctly: passed.\n");
  } else {
    Serial.write("control sensor responding incorrectly: failed.\n");
  }

  Serial.write("    Diagnostic 2: ambient test sensor light level ...");
  if (ambientLightLevelTest(PWR_S_TEST, DATA_TEST)) {
    Serial.write("test sensor responding correctly: passed.\n");
  } else {
    Serial.write("failed.\n");
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

  Serial.write("    Diagnostic 5: warp core ...");
  digitalWrite(PWR_D_CORE, HIGH);
  delay(100);
  if (digitalRead(DATA_D_CORE) == 1) {
    Serial.write("drive core online and stable: passed.\n");
  } else {
    Serial.write("drive core could not be brought online or is unstable: failed.\n");
  }

  Serial.write("    Diagnostic 6: warp shell ...");
  digitalWrite(PWR_D_SHELL, HIGH);
  delay(100);
  if (digitalRead(DATA_D_SHELL) == 1) {
    Serial.write("drive shell online and stable: passed.\n");
  } else {
    Serial.write("drive shell could not be brought online or is unstable: failed.\n");
  }

  Serial.write("  Diagnostics complete.\nPlease review diagnostic information and press [ENTER] to proceed ONLY IF ALL DIAGNOSTICS PASSED.\n");
  waitForActivation();
}

void loop() {
  // put your main code here, to run repeatedly:

}
