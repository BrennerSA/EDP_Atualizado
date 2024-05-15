int IN1_desce = 2,IN2_desce = 3, IN3_desce = 4, IN4_desce = 5;
int IN1_sobe = 6,IN2_sobe = 7, IN3_sobe = 8, IN4_sobe = 9;
int leitura = 0;

void subir(){
  digitalWrite(IN1_desce, 0); 
  digitalWrite(IN2_desce, 0);
  digitalWrite(IN3_desce, 0);
  digitalWrite(IN4_desce, 0);
  digitalWrite(IN1_sobe, 1); 
  digitalWrite(IN2_sobe, 1);
  digitalWrite(IN3_sobe, 1);
  digitalWrite(IN4_sobe, 1); 
}

void descer(){
  digitalWrite(IN1_desce, 1); 
  digitalWrite(IN2_desce, 1);
  digitalWrite(IN3_desce, 1);
  digitalWrite(IN4_desce, 1);
  digitalWrite(IN1_sobe, 0); 
  digitalWrite(IN2_sobe, 0);
  digitalWrite(IN3_sobe, 0);
  digitalWrite(IN4_sobe, 0);  
}
void parar(){
  digitalWrite(IN1_desce, 1); 
  digitalWrite(IN2_desce, 1);
  digitalWrite(IN3_desce, 1);
  digitalWrite(IN4_desce, 1);
  digitalWrite(IN1_sobe, 1); 
  digitalWrite(IN2_sobe, 1);
  digitalWrite(IN3_sobe, 1);
  digitalWrite(IN4_sobe, 1);  
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(IN1_desce, OUTPUT);
  pinMode(IN2_desce, OUTPUT);
  pinMode(IN3_desce, OUTPUT);
  pinMode(IN4_desce, OUTPUT);
  pinMode(IN1_sobe, OUTPUT);
  pinMode(IN2_sobe, OUTPUT);
  pinMode(IN3_sobe, OUTPUT);
  pinMode(IN4_sobe, OUTPUT);
  parar();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 1){
    leitura = Serial.parseInt();
    Serial.println(leitura);
  }
  if(leitura == 0) parar();
  else if(leitura == 1) subir();
  else if(leitura == 2) descer();
}
