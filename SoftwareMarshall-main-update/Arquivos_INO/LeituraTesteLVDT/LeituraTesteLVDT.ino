int lvdt = 0;
int leitura_lvdt = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  analogReadResolution(14);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogReadResolution(12);
  Serial.print(analogRead(0));
  Serial.print("  ");
  analogReadResolution(14);
  Serial.println(analogRead(2));
}
