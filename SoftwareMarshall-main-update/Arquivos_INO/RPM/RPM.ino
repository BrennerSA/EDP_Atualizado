volatile int rev;
float rpm;
unsigned long lastmillis;

void contar () {//método que ira variar as rpm;
  rev++;
}

void media_movel(int leitura);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  attachInterrupt (digitalPinToInterrupt (7), contar, FALLING); 
  rev = 0;
  rpm = 0;
  lastmillis = 0;
  analogWrite(2,100);
}
void loop() {
  if (millis () - lastmillis == 250) {
    detachInterrupt(digitalPinToInterrupt (7));
    rpm=rev*240/3;
    Serial.println(((0.104719755120*rpm)*6.5/60)/1.85);
    //media_movel(rpm);
    rev = 0;
    lastmillis = millis ();
    attachInterrupt (digitalPinToInterrupt (7), contar, FALLING);
  }
}

void media_movel(int leitura){
  int N = 3;
  float vals[] = {0, 0, 0};
  for(int i = N - 1; i > 0; i--){
    vals[i] = vals[i-1];
  }
  vals[0] = leitura;
  
  float filtered = 0;
  for(int i = 0; i < N; i++){
    filtered = filtered + (vals[i]/N);
  }
  
  Serial.println(filtered);
}
