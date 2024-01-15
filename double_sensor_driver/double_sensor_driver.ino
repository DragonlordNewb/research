// Parameters
#define RAW_DATA_COUNT 100

// Pin numbers
const char PWR_LASER = 2;
const char PWR_CTRL = 3;
const char DATA_CTRL = 5; 

int rawData[RAW_DATA_COUNT];
int ctr = 0;

double computeDataPoint() {
  double result = 0;
  for (int i = 0; i < RAW_DATA_COUNT; i++) {
    result += (double)(rawData[i]);
  }
  return result / (double)(RAW_DATA_COUNT);
}

void setup() {
  pinMode(PWR_LASER, OUTPUT);
  pinMode(PWR_CTRL, OUTPUT);
  digitalWrite(PWR_CTRL, HIGH);

  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < RAW_DATA_COUNT; i++) {
    ctr = 0;
    digitalWrite(PWR_LASER, HIGH);
    while (digitalRead(DATA_CTRL) == 1) {ctr++;}
    digitalWrite(PWR_LASER, LOW);
    rawData[i] = ctr;
    delay(75);
  }
  Serial.write("DATA: ");
  Serial.print(computeDataPoint());
  Serial.write("\n");
}