int sensor=A0, soil;
void setup() {
  Serial.begin(9600);
  Serial.println("Serial begin");
  delay(10000);
}

void loop() {
  soil = analogRead(sensor);
  soil = map(soil, 1023, 386, 0, 100);
  Serial.println(String("Soil Val: ") + soil);
  delay(10000);
}
