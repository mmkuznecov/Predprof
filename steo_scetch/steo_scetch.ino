#include <Stepper.h>


int incoming_state;
int a = 0;
int vr;

const int stepsPerRevolution = 200;   // Количество шагов 
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);
Stepper myStepper1(stepsPerRevolution, 12, 13, 14, 15);

//Пусть будут 6 поступающих байт: "R"-rectangle,"S"-square,"C"-circle, "H"-semicircle, "P"-pentagon, "D" - вращение верхнего диска

int cont1[3] = {82, 83, 67};
int cont2[2] = {72, 80};
int container;

void setup(){
  Serial.begin(9600);  //Started the serial communication at 9600 baudrate
}

void loop(){
  if (Serial.available() > 0){  //Looking for incoming data
    incoming_state = Serial.read();  //Reading the data
    //if (incoming_state == 'C' || incoming_state == 'H'){Serial.println('first cont')}
    //else  {Serial.println('second cont')}
  }
   if (incoming_state == 68){
    myStepper.step(2);}
   else if(incoming_state == 87){container = 1;}
   else if(incoming_state == 66){container = 2;}
   else{
    for (int i; i < 3; i++){
      if (incoming_state == cont1[i]){
        container = 1;
        break;
      }
    }
    }
    for (int i; i < 2; i++){
      if (incoming_state == cont2[i]){container = 2; break;}
      }
    Serial.println(container);
    if (container == 1){
      myStepper1.step(stepsPerRevolution);
      myStepper.step(stepsPerRevolution*2);
      myStepper1.step(stepsPerRevolution);
    }
    if (container == 2){
      myStepper1.step(stepsPerRevolution);
      myStepper.step(stepsPerRevolution*2);
      myStepper1.step(stepsPerRevolution);
      }
   }
