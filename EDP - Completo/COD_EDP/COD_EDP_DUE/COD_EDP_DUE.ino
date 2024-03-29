/**********************************************************************************
*              Arduino DUE - código para software EDP - v. Beta                   *
* ------------------------------------------------------------------------------- *
* Criado por: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com                    *
* Data – 18/04/2022 - v 1.0                                                       *
***********************************************************************************/

/* Bibliotecas */
#include <Stepper.h>  //biblioteca para controlar motor de passos
#include <Oversampling.h>  //biblioteca de alteração da resolução
#include "Waveforms.h"  //biblioteca que gera a função (1-cos)/2

#define AR_12BIT_MAX   4096 //valor da resolucao do arduino DUE 12 bit
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling

Oversampling adc(12, 16, 2); //aumentar a resolução do adc de 12bit para 16bit (apenas arduino DUE)

/* Variavéis */
const int pinA = 7; //pino do aplicador de golpes DNIT134
const int pinB = 8; //pino do aplicador de golpes DNIT135
const int pinOnOff = 12; //pino On/Off da fonte
const int SensorIndutivo = 9;
int condConect = 0; //Condicao para conexao com o software
int condicao = 2; //Condicao para iniciar o motor de passos
int conditionEnsaio = 0; //Condicao de Ensaio (0 - DNIT134 | 1 - DNIT135)
int conditionMR = 1; //Condicao de Ensaio (0 - MR | 1 - COND)
int contadorG = 1; //Valor que conta os golpes dentro da função *Intervalo de tempo do aplicador*
int nGolpe = 0; //numpero de golpes
int nTime = 0; //parte inteira do tempo
int statuS = 0; //(0 ou 1)(ok ou n_ok) mado de avisar erro de pressao do aplicador
int margemSup = 63000; //margem superior
int margemInf = 10000; //margem inferior
int ntotalGolpes; //Numero total de golpes por estagio
int frequencia; //Valor condicao para intervalo da frequencia
int botoes; //Acoes do botoes pausar, parar e continuar o ensaio
int ad0; //valor analógico do LVDT1
int ad1; //valor analógico do LVDT2
int ad2; //valor analógico do LVDT3
int ad3; //valor analógico do LVDT4
int ad4; //valor analógico do sensor de pressão (Válvula do Motor)
int ad5; //valor analógico do sensor de pressão (Válvula Dinâmica)
int ad6; //valor analógico do sensor de temperatura (Estufa)
int i; //indicador temporal da funcao waveforms
int tipoWave; //indicador do tipo da funcao waveforms
int setpoint; //valor de entrada para o setpoint em porcentagem
int setpoint1; //Valor de entrada para o setpoint1 em milibar (0 - 10.000)mBar
int setpoint2; //Valor de entrada para o setpoint2 em milibar (0 - 10.000)mBar
int condFadiga=0;

//********************* VARIAVEIS PARA A CONDIÇÃO DE DISCREPÂNCIA  ************************//
int lmt;  //valor limite para os golpes com a condicao de discrepância
float adMin;  //valor do adMin
float admedio; //valor do admedio
float adMediaMovel; //valor do adMediaMovel
float defResiliente; //valor da deformação Resiliente
float defResilienteAnterior; //valor da deformação Resiliente anterior
float discrep; //valor da discrepancia entre as leituras


//*************************************(MOTOR) ********************************************//
float AM = 2.0677; //valor de A da calibração da válvula do motor de passos
float BM = 10.01; //valor de B da calibração da válvula do motor de passos

//**************** (DINAMICA1 - Pistão) OBS:VALORES UTILIZADOS NO SOFTWARE *****************//
float AE1 = 2.0384;  //valor de A da calibração da válvula dinâmica 1 AD2 para mBar (output)
float BE1 = -2.7918; //valor de B da calibração da válvula dinâmica 1 AD2 para mBar (output)
float AE2 = 0.6021;  //valor de A da calibração da válvula dinâmica 1 mBar para DAC1 (input)
float BE2 = 62.652; //valor de B da calibração da válvula dinâmica 1 mBar para DAC1 (input)

//**************** (DINAMICA2 - Câmara) OBS:VALORES UTILIZADOS NO SOFTWARE *****************//
float AF1 = 1.0476;  //valor de A da calibração da válvula dinâmica 2 AD2 para mBar (output)
float BF1 = -1296; //valor de B da calibração da válvula dinâmica 2 AD2 para mBar (output)
float AF2 = 2.7668;  //valor de A da calibração da válvula dinâmica 2 mBar para DAC1 (input)
float BF2 = 84.886; //valor de B da calibração da válvula dinâmica 2 mBar para DAC1 (input)

float setpointA; //Valor do setpointA
float setpointB; //Valor do setpointB
float setpointC; //Valor do setpointB
float setpointE; //Valor do setpointE
float setpointF; //Valor do setpointF
float setpointM; //Valor do setpointM
float lmtVoltSenDesl = 3.0;
float bit12_Voltage; //Usado para a conversao de bits ~ volts
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
float ValMilivolt; //Valor do sensor de pressao em mBar
float vd0; //valor em voltagem do LVDT1
float vd1; //valor em voltagem do LVDT2
float vd2; //valor em voltagem do LVDT3
float vd3; //valor em voltagem do LVDT4
float vd4; //valor do sensor de pressão em mBar (válvula do motor)
float vd5; //valor do sensor de pressão em mBar (válvula dinâmica)
float vd6; //valor do sensor de temperatura em graus celsius (Estufa)
long intervalo00 = 90; // 90 miliseg
long intervalo01 = 35; //100 miliseg
long intervalo09 = 1000; //1Hz 01-09
long intervalo05 = 500; //2Hz 01-04-01-04
long intervalo04 = 333; //3Hz 01-0233-01-0233-01-0233
long intervalo03 = 250; //4Hz 01-015-01-015-01-015-01-015
long intervalo02 = 200; //5Hz 01-01-01-01-01-01-01-01-01-01
long resultTempo[1];
unsigned long currentMillis; //variacao do tempo em milisegundos
unsigned long initialMillis; //tempo incial dinamico
unsigned char conexao;  //tipos de conexoes
unsigned char leitura;  //ler dado na porta serial

/* Estrutura da função S */
struct S{
  long t;
  int n;
};

Stepper mp(200, 8, 9, 10, 11); //Funcao definicao do motor de passos

/* Inicializacao da serial */
void setup(void) {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
  analogReference(AR_DEFAULT); //Define a tensao de 3.3Volts como sendo a padrao (apenas no arduino DUE)
  analogWrite(DAC0, 0); //pino responsavel em alterar a pressao no (regulador de pressão proporcional 1) (valvula dinâmica 1)
  analogWrite(DAC1, 0); //pino responsavel em alterar a pressao no (regulador de pressão proporcional 2) (valvula dinâmica 2)
  //analogWrite(DAC1, 0); //pino apenas para ver a função waveforms no osciloscopio (para testes)
  pinMode(A4, INPUT); //pino LVDT1
  pinMode(A6, INPUT); //pino LVDT2
  pinMode(A8, INPUT); //pino LVDT_Asfalto
  // pinMode(A9, INPUT); //pino LVDT4
  pinMode(A0, INPUT); //pino Sensor de pressão (válvula do motor) (valvula dinâmica 1) (camara)
  pinMode(A2, INPUT); //pino Sensor de pressão (válvula dinâmica 2) (pistao)
  pinMode(A10, INPUT); //pino Sendor de Temperatura (Estufa)
  pinMode(pinA, OUTPUT);  //configura o pinA
  pinMode(SensorIndutivo,INPUT);
  pinMode(pinB, OUTPUT);  //configura o pinB
  pinMode(pinOnOff, OUTPUT);  //configura o pinOnOff
  digitalWrite(pinA, LOW); //inicia desativado o pinA
  digitalWrite(pinB, LOW); //inicia desativado o pinB
  digitalWrite(pinOnOff, LOW); //inicia desativado o pinOnOff
  mp.setSpeed(40); //velocidade de rotacao do motor de passos em rpm
  mp.step(0);  //inicia o motor de passos com zero passos
  bit12_Voltage = (InputRange_code)/(AR_12BIT_MAX - 1); //fator de conversão bit~voltagem
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de conversão bit~voltagem
  setpointM = 340/InputRange_code;   //setpointM inicia sendo o menor valor admissível (referente a v. do motor)
  setpointE = int(12); //setpoint inicia sendo o menor valor admissível (referente a v. dinâmica1)
  setpointF = int(12);  //setpoint inicia sendo o menor valor admissível (referente a v. dinâmica2)
  lmt = 200;  //200 é considerado o valor padrão do limite de golpes para a discrepância
  discrep = 1.05;  //inicia sendo o valor de 5%
}

/* Principal */
void loop(void) {
  conexao:
  conexao = Serial.read();

  switch(conexao){
    //**********************************************************************************//
    case 'C':
      //caso receba C (verifica se há conexao com a porta serial)
      Serial.println("conectado");
      Serial.flush();
      condConect = 1;
      digitalWrite(pinOnOff, HIGH); //ativa o pinOnOff após ativar a conexao
      break;

    //**********************************************************************************//
    case 'D':
      //caso receba D (implica na desconexao com a porta serial)
      Serial.println("desconectado");
      digitalWrite(pinOnOff, LOW); //desativa o pinOnOff após desconectar
      Serial.flush();
      Serial.end();
      Serial.begin(115200);
      condConect = 0;
      break;

    case 'I':
      //caso receba I (acessa o ensaio da norma DNIT134)

      //**********************************************************************************//
      //**********************************************************************************//
      //********************************* norma DNIT134 **********************************//
      //**********************************************************************************//
      //**********************************************************************************//

      if(condConect == 1){
        sensorLVDTDNIT134:
        Serial.println("DNIT134");
        conditionEnsaio = 0;
        serialFlush();
        while(true){
          if(Serial.available()>0){
            leitura = Serial.read();
            if(leitura == 'B'){
              Serial.println("BREAK");
              serialFlush();
              goto conexao;
            }
            if(leitura == 'E'){
              Serial.println("DINAMICA1");
              serialFlush();
              goto dinamica2DNIT134;
            }
            if(leitura == 'F'){
              Serial.println("DINAMICA2");
              serialFlush();
              goto dinamica1DNIT134;
            }
            if(leitura == 'M'){
              Serial.println("MOTOR");
              serialFlush();
              goto motorDNIT134;
            }
            if(leitura == 'G'){
              Serial.println("GOLPES");
              serialFlush();
              goto golpesDNIT134;
            }
            if(leitura == 'J'){
              imprimir();
              serialFlush();
            }
            if(leitura == 'K'){
              Serial.println("DISCREPANCIA");
              serialFlush();
              goto discrepancia;
            }
            if(leitura == 'L'){
              Serial.println("LIMITE");
              serialFlush();
              goto limite;
            }
            if(leitura == 'I'){
              Serial.println("IMPRIMIR");
              serialFlush();
              while(true){
                if(Serial.available()>0){
                  leitura = Serial.read();
                  if(leitura == 'S'){
                    goto sensorLVDTDNIT134;
                  }
                }
                else{
                  imprimir();
                }
              }
            }
          }
        }
        break;

        //**********************************************************************************//
        //********************************* DISCREPANCIA ***********************************//
        discrepancia:
        while(true){
          if (Serial.available()>1){
            setpoint = Serial.parseInt();    //valor em %
            if(setpoint > 5){
              discrep = 1 + float(setpoint)/100;
              Serial.print("DISCREP=");
              Serial.println(discrep);
              serialFlush();
            }
            if(setpoint == 3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        break;

        //**********************************************************************************//
        //*************************** LIMITE DOS GOLPES NO MR ******************************//
        limite:
        while(true){
          if (Serial.available()>1){
            setpoint = Serial.parseInt();    //numero limite dos glp no MR
            if(setpoint > 5){
              lmt = setpoint;
              Serial.print("LIMITE=");
              Serial.println(lmt);
              serialFlush();
            }
            if(setpoint == 3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        break;

        //**********************************************************************************//
        //************************* VÁLVULA DINÂMICA 2 (camara) ****************************//
        dinamica1DNIT134:
        while(true){
          if (Serial.available()>1){
            setpoint1 = Serial.parseInt();  //setpoint1 é um valor em mbar
            if(setpoint1 >= 0){
              setpointF = int(setpoint1);   //valor em contagem
              analogWrite(DAC0, setpointF);
              Serial.print("CHEGOU=");
              Serial.print(setpoint1);
              Serial.print("/SENSOR=");
              ad4 = analogRead(A0);
              Serial.println(ad4);
              serialFlush();
            }
            if(setpoint1 == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        break;

        //**********************************************************************************//
        //************************** VÁLVULA DINÂMICA 1 (pistão) ***************************//
        dinamica2DNIT134:
        while(true){
          if (Serial.available()>1){
            setpoint2 = Serial.parseInt();  //setpoint2 é um valor em mbar
            if(setpoint2 >= 0){
              setpointE = int(setpoint2);   //valor em contagem
              analogWrite(DAC1, setpointE);
              Serial.print("CHEGOU=");
              Serial.print(setpoint2);
              Serial.print("/SENSOR=");
              ad5 = analogRead(A2);
              Serial.println(ad5);
              serialFlush();
            }
            if(setpoint2 == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        break;

        //**********************************************************************************//
        //******************************* MOTOR DE PASSOS **********************************//
        motorDNIT134:
        while(true){
          ad4 = analogRead(A0);
          vd4 = ad4*AM+BM; //mbar
          if(Serial.available()>0){
            setpoint1 = Serial.parseInt();
            if(setpoint1 > 5){
              Serial.print("CHEGOU=");
              Serial.print(setpoint1);
              Serial.print("/SENSOR=");
              ad4 = analogRead(A0);
              vd4 = ad4*AM+BM; //mbar
              Serial.println(vd4);
              serialFlush();
              condicao = 1;
            }
            if(setpoint1 == 3){
              digitalWrite(8, LOW);
              digitalWrite(9, LOW);
              digitalWrite(10, LOW);
              digitalWrite(11, LOW);
              mp.setSpeed(40); //retorna a velocidade original do motor
              condicao = 2;
              goto sensorLVDTDNIT134;
            }
            if(setpoint1 == 2){
              digitalWrite(pinA, HIGH);  //ativa o pinA
              delay(100);
              digitalWrite(pinA, LOW);  //desativa o pinA
              delay(900);
              digitalWrite(pinA, HIGH);  //ativa o pinA
              delay(100);
              digitalWrite(pinA, LOW);  //desativa o pinA
              delay(900);
              digitalWrite(pinA, HIGH);  //ativa o pinA
              delay(100);
              digitalWrite(pinA, LOW);  //desativa o pinA
              setpoint1 = 120;
            }
            else{
              setpointM = setpoint1;     //valor do setpoint em milibar (0 - 10.000)mBar
            }
          }
          if((vd4 > 1.1*setpointM || vd4 < 0.97*setpointM) && condicao == 1){ //INTERVALO DE PRESSAO NAO OK//
            condicao = 0;
          }
          if(vd4 < 1.1*setpointM && vd4 > 0.98*setpointM){ //INTERVALO DE PRESSAO OK//
            Serial.println("o");
            mp.step(0);
            condicao = 1;
          }
          if(condicao == 0){
            Serial.println("n");
            if(abs((setpointM - vd4)) > 500){
              mp.setSpeed(40); //deixa a rotacao do motor em 40 rpm
            }
            if(abs((setpointM - vd4)) < 400){
              mp.setSpeed(25); //deixa a rotacao do motor em 25 rpm
            }
            if(abs((setpointM - vd4)) < 200){
              mp.setSpeed(10); //deixa a rotacao do motor em 10 rpm
            }
            if(abs((setpointM - vd4)) < 50){
              mp.setSpeed(5); //deixa a rotacao do motor em 5 rpm
            }
            mp.step(floor((setpointM - vd4)/2));
          }
        }
        break;

        //**********************************************************************************//
        //************************************ GOLPES **************************************//
        golpesDNIT134:
        while(true){ //RESPONSAVEL EM COLETAR A QUANTIDADE TOTAL DE GOLPES/
          if(Serial.available()> 0){
            ntotalGolpes = Serial.parseInt();
            if(ntotalGolpes > 0){
              if(ntotalGolpes<=10){
                conditionMR = 0;   //entende-se que tá se executando o MR (conditionMR = 0)
              }else{
                conditionMR = 1;
              }
              Serial.print("NGOLPES=");
              Serial.println(ntotalGolpes);
              serialFlush();
              break;
            }
            if(ntotalGolpes == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        while(true){ //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
          if(Serial.available()>0){
            frequencia = Serial.parseInt();
            if(frequencia > 0){
              Serial.print("FREQ=");
              Serial.println(frequencia);
              digitalWrite(pinB, LOW);  //ativa o pinAplicador
              serialFlush();
              break;
            }
            if(frequencia == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }

        currentMillis = millis(); //Tempo atual em ms
        initialMillis = currentMillis;  //Tempo inicial

        while(true){
          S resultTempo = tempo(nTime, frequencia, initialMillis);
          initialMillis = resultTempo.t;
          nTime = resultTempo.n;

          if(nGolpe >= ntotalGolpes){
            while(currentMillis - initialMillis <= 990){
              currentMillis = millis(); //Tempo atual em ms
              while(true){
                if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
                  imprimir();
                  break;
                }
                else{
                  delayMicroseconds(1);
                  currentMillis = millis(); //Tempo atual em ms
                }
              }
            }
            initialMillis = currentMillis;
            nGolpe = 0;
            nTime = 0;
            contadorG = 1;
            goto sensorLVDTDNIT134;
          }

          if (Serial.available()> 0){ //aguarda o valor na serial e se for 3 "para" o ensaio//
            botoes = Serial.parseInt();
            if(botoes == 3){
              pararEnsaio:
              nGolpe = 0;
              nTime = 0;
              statuS = 0;
              currentMillis = millis();
              initialMillis = currentMillis;
              goto sensorLVDTDNIT134;
            }
            if(botoes == 4){ //aguarda o valor na serial. e se for 4 pausa o ensaio//
              float guardavalor;
              guardavalor = float(currentMillis - initialMillis);
              while(true){
                imprimir();
                if (Serial.available()> 0){
                  botoes = Serial.parseInt();
                  if(botoes == 2){ //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                    currentMillis = millis();
                    initialMillis = currentMillis-guardavalor;
                    break;
                  }
                  if(botoes == 3){ //aguarda o valor na serial. e se for 3 "para" o ensaio//
                    goto pararEnsaio;
                  }
                }
              }
            }
          }
          if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
            imprimir();
            calculoDiscrepancia();
          }
          else{
            delayMicroseconds(1);
            currentMillis = millis(); //Tempo atual em ms
          }
        }/*while*/
        break;
      }/*if(condConect == 1)*/

    case 'J':
    //caso receba J (acessa o ensaio da norma DNIT135)

    //**********************************************************************************//
    //**********************************************************************************//
    //********************************* norma DNIT135 **********************************//
    //**********************************************************************************//
    //**********************************************************************************//

      if(condConect == 1){
        sensorLVDTDNIT135:
        Serial.println("DNIT135");
        conditionEnsaio = 1;
        serialFlush();
        while(true){
          if(Serial.available()>0){
            leitura = Serial.read();
            if(leitura == 'B'){
              Serial.println("BREAK");
              serialFlush();
              goto conexao;
            }
            if(leitura == 'G'){
              Serial.println("GOLPES");
              serialFlush();
              goto golpesDNIT135;
            }
            if(leitura == 'J'){
              imprimir2();
              serialFlush();
            }
            if (leitura == 'E'){
              Serial.println("PRESSÃO DO APLICADOR");
              serialFlush();
              SetarPressGlp();
              goto sensorLVDTDNIT135;
            }
            if(leitura == 'I'){
              Serial.println("IMPRIMIR");
              serialFlush();
              while(true){
                if(Serial.available()>0){
                  leitura = Serial.read();
                  if(leitura == 'S'){
                    goto sensorLVDTDNIT135;
                  }
                }
                else{
                  imprimir2();
                }
              }
            }
          }
        }
        break;

        //**********************************************************************************//
        //************************************ GOLPES **************************************//
        golpesDNIT135:
        while(true){ //RESPONSAVEL EM COLETAR A QUANTIDADE TOTAL DE GOLPES//
          if(Serial.available()> 0){
            ntotalGolpes = Serial.parseInt();
            if(ntotalGolpes > 0){
              Serial.print("NGOLPES=");
              Serial.println(ntotalGolpes);
              serialFlush();
              break;
            }
            if(ntotalGolpes == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }
        while(true){ //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
          if(Serial.available()> 0){
            frequencia = Serial.parseInt();
            if(frequencia > 0){
              Serial.print("FREQ=");
              Serial.println(frequencia);
              serialFlush();
              break;
            }
            if(frequencia == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }

        while(true){ //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
          if(Serial.available()> 0){
            condFadiga = Serial.parseInt();
            if(condFadiga >= 0){
              Serial.print("FREQ=");
              Serial.println(condFadiga);
              serialFlush();
              break;
            }
            if(condFadiga == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }
        
        

        currentMillis = millis(); //Tempo atual em ms
        initialMillis = currentMillis;  //Tempo inicial

        while(true){
          S resultTempo = tempo(nTime, frequencia, initialMillis);
          initialMillis = resultTempo.t;
          nTime = resultTempo.n;

          if(nGolpe == ntotalGolpes){ //CONDIÇAO DE PARAR O ENSAIO E IMPRIMIR 1S DE DADOS FINAIS
            while(currentMillis - initialMillis <= 995){
              currentMillis = millis(); //Tempo atual em ms
              while(true){
                if((currentMillis - initialMillis)% 5 == 0 && (currentMillis - initialMillis)!= 0){
                  imprimir2();
                  break;
                }
                else{
                  delayMicroseconds(1);
                  currentMillis = millis(); //Tempo atual em ms
                }
              }
            }
            initialMillis = currentMillis;
            nGolpe = 0;
            nTime = 0;
            contadorG = 1;
            digitalWrite(pinB, LOW);  //desativa o pinAplicador
            // analogWrite(DAC1, 0);  //SETA UM VALOR ZERO NO DAC1
            goto sensorLVDTDNIT135;
          }
          if (Serial.available()> 0){ //CONDICAO DE FUNCIONALIDADES AO DECORRER DO ENSAIO
            botoes = Serial.parseInt();
            if(botoes == 3){ //aguarda o valor na serial e se for 3 "para" o ensaio//
              pararEnsaioDNIT135:
              nGolpe = 0;
              nTime = 0;
              statuS = 0;
              currentMillis = millis();
              initialMillis = currentMillis;
              digitalWrite(pinB, LOW);  //desativa o pinAplicador
              // analogWrite(DAC1, 0);  //SETA UM VALOR ZERO NO DAC1
              goto sensorLVDTDNIT135;
            }
            else if(botoes == 4){ //aguarda o valor na serial. e se for 4 pausa o ensaio//
              float guardavalor;
              guardavalor = float(currentMillis - initialMillis);
              while(true){
                imprimir2();
                if (Serial.available()> 0){
                  botoes = Serial.parseInt();
                  if(botoes == 2){ //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                    currentMillis = millis();
                    initialMillis = currentMillis-guardavalor;
                    break;
                  }
                  if(botoes == 3){ //aguarda o valor na serial. e se for 3 "para" o ensaio//
                    goto pararEnsaioDNIT135;
                  }
                }
              }
            }else if(botoes==5){
              ntotalGolpes++;
            }
          }
          if(digitalRead(SensorIndutivo)==1){
            Serial.println(digitalRead(SensorIndutivo));
            statuS=2;
            if((currentMillis - initialMillis)% 5 == 0 && (currentMillis - initialMillis)!= 0){
              goto pararEnsaioDNIT135;
            }
          }
          if((currentMillis - initialMillis)% 5 == 0 && (currentMillis - initialMillis)!= 0){
            imprimir2();
            if (digitalRead(SensorIndutivo)==0 && condFadiga==1 && (ntotalGolpes-nGolpe)<=5){
              ntotalGolpes++;
            }
          }
          else{
            delayMicroseconds(1);
            currentMillis = millis(); //Tempo atual em ms
          }
        }/*while*/
        break;
      }/*if(condConect == 1)*/

    case 'K':
    //caso receba K (acessa o ensaio da norma DNIT...)

    //**********************************************************************************//
    //**********************************************************************************//
    //********************************* norma DNIT... **********************************//
    //**********************************************************************************//
    //**********************************************************************************//
      if(condConect == 1){
        Serial.println("Ainda falta complementar");
      }/*if(condConect == 1)*/

   }/*switch*/

}/*void*/


void SetarPressGlp(){
  while(true){
    if (Serial.available()>1){
      setpoint2 = Serial.parseInt();  //setpoint2 é um valor em mbar
      if(setpoint2 >= 0){
        setpointE = int(setpoint2);   //valor em contagem
        analogWrite(DAC1, setpointE); 
        Serial.print("CHEGOU=");
        Serial.print(setpoint2);
        Serial.print("/SENSOR=");
        ad5 = analogRead(A2);
        Serial.println(ad5);
        serialFlush();
      }
      if(setpoint2 == -3){
        break;
      }
    }
  }
}

//**********************************************************************************//
//*************************** Imprimir dados na 134 ********************************//
//**********************************************************************************//

/* Imprimir dados na 134 */
void imprimir(){
  ad0 = adc.read(A4);
  ad1 = adc.read(A6);
  ad4 = analogRead(A0);
  ad5 = analogRead(A2);
  vd0 = ad0*bit16_Voltage;
  vd1 = ad1*bit16_Voltage;
  vd4 = ad4; //mbar (camara)
  vd5 = ad5; //mbar (pistão)
  admedio = (ad0+ad1)/2; //admedio
  //CONDICAO DE DE MARGEM DE SEGURANÇA PARA OS SENSORES//
  if(ad0 > margemSup or ad1 > margemSup or ad0 < margemInf or ad1 < margemInf){
    nGolpe = ntotalGolpes; //critério de parada
    statuS = 2; //status passa a valer 2
  }
  Serial.print(float(nTime)+float(currentMillis - initialMillis)/1000, 3); //temp
  Serial.print(",");
  Serial.print(ad0);         //y1
  Serial.print(",");
  Serial.print(ad1);         //y2
  Serial.print(",");
  Serial.print(vd0,4);       //y1v
  Serial.print(",");
  Serial.print(vd1,4);       //y2v
  Serial.print(",");
  Serial.print(vd4,4);       //camara
  Serial.print(",");
  Serial.print(vd5,4);       //pistao
  Serial.print(",");
  Serial.print(statuS);      //sts
  Serial.print(",");
  Serial.print(nGolpe);      //glp
  Serial.print(",");
  Serial.println(ntotalGolpes); //ntglp
}/* Imprimir dados DA 134*/

void calculoDiscrepancia(){
  //CONDICAO DE DISCREPÂNCIA// (OBS: O GRÁFICO AQUI É INVERTIDO)
  if(conditionMR == 0){
    if(nTime == 4){
      if((currentMillis - initialMillis) == 10){
        adMediaMovel = admedio;
        adMin = admedio;
      }
      if((currentMillis - initialMillis) > 10 && (currentMillis - initialMillis) < 200){
        if(admedio < adMin){
          adMin = admedio;
        }
      }
      if((currentMillis - initialMillis) > 200 && (currentMillis - initialMillis) < 1000){
        adMediaMovel = (adMediaMovel + admedio)/2;
        defResilienteAnterior = adMediaMovel - adMin;
      }
    }
    if(nTime >= 5){
      if((currentMillis - initialMillis) == 10){
        adMin = admedio;
      }
      if((currentMillis - initialMillis) > 10 && (currentMillis - initialMillis) < 200){
        if(admedio < adMin){
          adMin = admedio;
        }
      }
      if((currentMillis - initialMillis) > 200 && (currentMillis - initialMillis) < 1000){
        adMediaMovel = (adMediaMovel + admedio)/2;
        defResiliente = adMediaMovel - adMin;
      }
      if((currentMillis - initialMillis) == 990){
        if(defResiliente > defResilienteAnterior){
          if(defResiliente/defResilienteAnterior > discrep){
            ntotalGolpes++;
            defResilienteAnterior = defResiliente;
          }
          if(ntotalGolpes >= lmt){
            statuS = 1;
          }
        }
        if(defResiliente < defResilienteAnterior){
          if(defResilienteAnterior/defResiliente > discrep){
            ntotalGolpes++;
            defResilienteAnterior = defResiliente;
          }
          if(ntotalGolpes >= lmt){
            statuS = 1;
          }
        }
      }
    }
  }
}

//**********************************************************************************//
//************************** Imprimir dados na 135 *********************************//
//**********************************************************************************//
/* Imprimir dados na 135 */
void imprimir2(){
  ad2 = adc.read(A8);
  ad5 = analogRead(A2);
  // ad3 = adc.read(A9);
  // ad6 = analogRead(A10); //SENSOR DE TEMPERATURA
  vd2 = ad2*bit16_Voltage; //não deve ser maior q 3v
  // vd3 = ad3*bit16_Voltage;
  vd5=ad5;
  vd6 = ad6*bit12_Voltage*1000;

  if (vd2>lmtVoltSenDesl){
    statuS=2;
    nGolpe=ntotalGolpes;
  }

  Serial.print(float(nTime)+float(currentMillis - initialMillis)/1000, 3); //temp
  Serial.print(",");
  Serial.print(ad2);            //sensor deslocamento
  Serial.print(",");
  Serial.print(vd2,4);          //tensão sensor deslocamento
  Serial.print(",");
  Serial.print(0,4);       //sensor indutivo
  Serial.print(",");
  Serial.print(vd5,4);       //pistao
  Serial.print(",");
  Serial.print(statuS);      //sts
  Serial.print(",");
  Serial.print(nGolpe);      //glp
  Serial.print(",");
  Serial.println(ntotalGolpes); //ntglp

}/* Imprimir dados da 135 */

//**********************************************************************************//
//**************************Limpa o buffer serial***********************************//
//**********************************************************************************//
/* Limpa o buffer serial */
void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}/* Limpa o buffer serial */

//**********************************************************************************//
//**********************************************************************************//
//********************* Intervalo de tempo do aplicador ****************************//
//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
/* Intervalo de tempo do aplicador */
S tempo(int nTime, int frequencia, long initialMillis){
  currentMillis = millis(); //Tempo atual em ms
  switch(frequencia){
    case 1:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //ativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, HIGH);  //ativa o pinB
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo09){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, LOW);  //ativa o pinB
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;

    case 2:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //ativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, HIGH);  //ativa o pinA
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo05){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, LOW);  //ativa o pinA
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo05 && (currentMillis - initialMillis) <= intervalo05 + intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //ativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, HIGH);  //ativa o pinB
        }
      }
      if((currentMillis - initialMillis) > intervalo05 + intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          digitalWrite(pinB, LOW);  //desativa o pinB
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;

    case 3:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo01){
            digitalWrite(pinA, HIGH);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, LOW);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo04){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo04 && (currentMillis - initialMillis) <= intervalo04 + intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //ativa o pinA
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo04);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo04 + intervalo01 && (currentMillis - initialMillis) <= 2*intervalo04){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo04 && (currentMillis - initialMillis) <= 2*intervalo04+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //ativa o pinA
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo04);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo04+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, LOW);  //desativa o pinA;
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;

    case 4:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo03 && (currentMillis - initialMillis) <= intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo03);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo03+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo03 && (currentMillis - initialMillis) <= 2*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo03);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo03+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo03 && (currentMillis - initialMillis) <= 3*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 3*intervalo03);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 4){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;

    case 5:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo02 && (currentMillis - initialMillis) <= intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo02);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > intervalo02+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo02 && (currentMillis - initialMillis) <= 2*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo02);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo02 && (currentMillis - initialMillis) <= 3*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 3*intervalo02);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 4*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 4){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 4*intervalo02 && (currentMillis - initialMillis) <= 4*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinA, LOW);  //ativa o pinA
          }
          else{
            digitalWrite(pinA, HIGH);  //desativa o pinA
          }
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 4*intervalo02);
          setpointC = (waveformsTable[tipoWave-1][i]*setpointA+setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
      }
      if((currentMillis - initialMillis) > 4*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinA, HIGH);  //desativa o pinA
        }
        if(conditionEnsaio == 1){
          setpointC = (setpointB)*4095/3300;
          //analogWrite(DAC0, setpointC);
        }
        if(contadorG == 5){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
  }/*switch*/
  return {initialMillis, nTime};
}/* Intervalo de tempo do aplicador */

//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
