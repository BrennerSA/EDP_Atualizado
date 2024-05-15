#include <Oversampling.h>

Oversampling adc(12, 14, 2); //Adc Bytes 10 or 12, Oversampeling Bytes 11-18, 2 Is avaraging count.

void setup(void) 
{
  Serial.begin(19200);
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino due)
}

void loop(void) 
{
  float leitura = Serial.println(adc.read(2));
  delay(100);
}
