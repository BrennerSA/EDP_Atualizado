#include <Oversampling.h>

// VARIÁVEIS DE ACIONAMENTO DOS RELÉS
int IN1_desce = 2, IN2_desce = 3, IN3_desce = 4, IN4_desce = 5;
int IN1_sobe = 8, IN2_sobe = 9, IN3_sobe = 10, IN4_sobe = 11;

// FUNÇÕES DE ACIONAMENTO DO MOTOR
void subir();
void descer();
void parar();

// VARIÁVEIS DE FLUÊNCIA E ESTABILIDADE E CALIBRAÇÃO
double offset_fluencia = 0, offset_estabilidade = 0;
double lvdt_fluencia = 0, lvdt_estabilidade = 0, lvdt_estabilidade_anterior = 0, lvdt_estabilidade_variacao = 0;

// FUNÇÕES PARA CALIBRACAI E LEITURA DOS LVDTS
void calibrar_lvdts();
void ler_fluencia();
void ler_estabilidade();
void ler_velocidade();
bool criterioParada();
bool emergencia();

// VARIAVEL  DE COMUNICAÇÃO
char conexao;
bool Ensaio_em_andamento = false;
int status = 0;
unsigned long timeStop = 90000; 
double maximo = 0;
bool atendido = 0;
double x_fluencia = 0;
double limite_flu = 0;
double x_estabilidade = 0;
double velocidade = 0;

unsigned long lastmillis;

int contador = 0;
double valores_iniciais = 0;

Oversampling adc(12, 14, 2);

void setup() {
  // DEFININDO ADC PARA 12 BITS
  analogReadResolution(12); // SÓ PARA ARDUINO DUE
  // DEFININDO COMUNICAÇÃO
  Serial.begin(19200);
  // DEFININDO PINO DOS RELÉS COMO SAÍDA
  pinMode(IN1_desce, OUTPUT);
  pinMode(IN2_desce, OUTPUT);
  pinMode(IN3_desce, OUTPUT);
  pinMode(IN4_desce, OUTPUT);
  pinMode(IN1_sobe, OUTPUT);
  pinMode(IN2_sobe, OUTPUT);
  pinMode(IN3_sobe, OUTPUT);
  pinMode(IN4_sobe, OUTPUT);
  // GARANTIDO QUE O RELÉ INICIA NÃO ACIONADO
  parar();

}

void loop() {
  // LEITURA DE DADOS DO SOFTWARE MARSHALL
  conexao = Serial.read();
  if(conexao == 'C') calibrar_lvdts();
  else if(conexao == 'I'){
    lastmillis = millis(); 
    while((millis() - lastmillis) < timeStop){
      subir();
      ler_fluencia();
      ler_estabilidade();
      Serial.print(double(9.9999),4);Serial.print(lvdt_estabilidade,4);Serial.print(velocidade,4);Serial.println(lvdt_fluencia,3); //ENVIA DADOS PARA PROGRAMA EM PYTON 
      Serial.flush();  //LIMPA BUFFER
      delay(50); 
      if(criterioParada()) timeStop = (millis() - lastmillis) + 1000; // PARA EXECUÇÃO 1 SEGUNDOS APÓS ROMPIMENTO DO CP
      if(emergencia()) timeStop = (millis() - lastmillis); // PARA EXECUÇÃO INSTANTÂNEAMENTE
    }
    Serial.print(double(0.0000),4);Serial.print(lvdt_estabilidade,4);Serial.print(velocidade,4);Serial.println(lvdt_fluencia,3); //ENVIA DADOS PARA PROGRAMA EM PYTON 
    Serial.flush(); //LIMPA BUFFER 
    parar();
  }
  else if(conexao == 'F'){
    descer();
    delay(29000);
    parar();
  }
  else if(conexao == 'S'){
    subir();
    delay(29000);
    parar();
  }else if(conexao== 'U'){    //SUBIR
    subir();
  }else if(conexao== 'D'){    //DESCER
    descer();
  }else if(conexao== 'P'){    //PARAR
    parar();
  }


  
}

void subir(){
//  Serial.println("SUBINDO");  
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
//  Serial.println("DESCENDO");
  maximo = 0;
  atendido = 0;  
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
//  Serial.println("PARADO");
  digitalWrite(IN1_desce, 1); 
  digitalWrite(IN2_desce, 1);
  digitalWrite(IN3_desce, 1);
  digitalWrite(IN4_desce, 1);
  digitalWrite(IN1_sobe, 1); 
  digitalWrite(IN2_sobe, 1);
  digitalWrite(IN3_sobe, 1);
  digitalWrite(IN4_sobe, 1);  
}

void calibrar_lvdts(){
  //OFFSET LVDT FLUENCIA
//  analogReadResolution(12);
  double x_fluencia = analogRead(0);
  offset_fluencia = x_fluencia/1000.0; //DIVIDE LEITURA POR MIL PARA GARANTIR FORMATO DECIMAL COM UMA CASA ANTES DA VÍRGULA
  //OFFSET LVDT ESTABILIDADE
 // analogReadResolution(12);
  double x_estabilidade = adc.read(2);
  offset_estabilidade = x_estabilidade/10000.0; //DIVIDE LEITURA POR 10 MIL PARA GARANTIR FORMATO DECIMAL COM UMA CASA ANTES DA VÍRGULA
  ler_fluencia(); //ATUALIZA LEITURAS
  ler_estabilidade(); //ATUALIZA LEITURAS
  //if((lvdt_estabilidade) < 1.0 or (lvdt_estabilidade) > (1.001) or (lvdt_fluencia) < 1.0 or (lvdt_fluencia) > (1.001)) calibrar_lvdts(); // CHAMADA RECURSIVA PARA OFFSET DOS SENSORES
  Serial.print(double(9.9999),4);Serial.print(lvdt_estabilidade,4);Serial.print(velocidade,4);Serial.println(lvdt_fluencia,3); // ENVIO DE DADOS PARA PROGRAMA EM PYTHON
  // Serial.println(x_fluencia);
}

void ler_fluencia(){
 // analogReadResolution(12);
  x_fluencia = analogRead(0);
  lvdt_fluencia = 1.0 + (x_fluencia/1000.0 - offset_fluencia); 
}

void ler_estabilidade(){
 // analogReadResolution(12);
  x_estabilidade = adc.read(2);
  lvdt_estabilidade = 1.0 + (x_estabilidade/10000.0 - offset_estabilidade);
}

void ler_velocidade(){
  velocidade = double(random(48,52)/10);
}
limite_flu = x_fluencia - offset_estabilidade;
bool emergencia(){
  //bool caio = ((x_estabilidade - offset_estabilidade) >= 25) && ((x_fluencia - offset_fluencia) >= 2500);
  if(limite_flu >= 1000.0){ // ver uma forma para não ir até o final do curso depois do inicio da força ir até delta15mm (2460 counts) 16/03
    return true;
  }
  return false;
}

bool criterioParada(){
  if(lvdt_estabilidade > maximo){
    maximo = lvdt_estabilidade; 
    //Serial.println(maximo);
  }
  else if((lvdt_estabilidade < 0.98*maximo and atendido == 0)){
    atendido = 1;
    return true;
  }
  return false;
}