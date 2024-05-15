#include <Oversampling.h>

int ad0;
int acc;
char dados;

Oversampling adc(12, 14, 2); // faz a reamostragem de 12bits para 14bits com média de 2 pontos

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogReadResolution(12);
}

void loop() {
  dados = Serial.read();
  if(dados == 'C'){
    int acc = 0;
    for(int i=0; i<10; i++){
      ad0 = adc.read(A0); // ler o sensor do anel de força;
      acc = acc + ad0;
      delay(100);
    }
    Serial.println(acc/10);
    Serial.println("----");  
  }
  
}
