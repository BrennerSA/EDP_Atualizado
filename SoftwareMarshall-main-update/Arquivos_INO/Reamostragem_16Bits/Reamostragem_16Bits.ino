#include <Wire.h>
#include <Oversampling.h>

#define   ADC_16BIT_MAX   65536
#define   ADC_10BIT_MAX   1024

Oversampling adc(10, 14, 2); //Adc Bytes 10 or 12, Oversampeling Bytes 11-18, 2 Is avaraging count.

float ads_bit_Voltage;
float ard_bit_Voltage;
float ads_code_bit_Voltage;

void setup(void) 
{
  Serial.begin(19200);
  Serial.println("Hello!");
  
  Serial.println("Getting single-ended readings from AIN0..3");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV/ADS1015, 0.1875mV/ADS1115)");

  float ads_InputRange = 4.096f;
  float ads_InputRange_code = 5.0f;// 3.3V É a tensão máxima que pode ser lida 
  ads_bit_Voltage = (ads_InputRange * 2) / (ADC_16BIT_MAX - 1);
  ard_bit_Voltage = (ads_InputRange * 2)/(ADC_10BIT_MAX - 1);
  ads_code_bit_Voltage = (ads_InputRange_code)/(ADC_16BIT_MAX - 1);
}

void loop(void) 
{
  int16_t adc0;
  float voltage_ads, voltage_ard, voltage_ads_code;
  
  voltage_ard = analogRead(0)*ard_bit_Voltage;
  voltage_ads_code = adc.read(0)*ads_code_bit_Voltage;
  
  Serial.print(analogRead(0)); Serial.print("  ");Serial.print(adc.read(0)); Serial.print("  "); Serial.println(voltage_ads_code); 
  delay(200);
}
