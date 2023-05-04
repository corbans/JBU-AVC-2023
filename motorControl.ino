#include <Servo.h>      //Motor driver    
#include <stdlib.h>     //standard
//#include "SonarEZ0pw.h" //ultrasonic sensor

Servo ST1, ST2;         //initialize motor objects

float inch_dis=1000;    //inch variable
String msg;             //message to be read from Pi
int counter = 0;
//const int ledPin=13;    //led for debugging
const int speed = 160;  //start speed (affects the straightAdjust function)
int range = 72;

// defines pins numbers
const int trigPin = 12;
const int echoPin = 13;
// defines variables
long duration;
int distance;

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

void setup() 
{
 pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
 pinMode(echoPin, INPUT); // Sets the echoPin as an Input
 ST1.attach( 9, 1000, 2000); //setup motor1 to pin 9  -- 0 is full reverse, 180 is full forward
 ST2.attach(10, 1000, 2000); //setup motor2 to pin 10 -- 90 is stopped
 Serial.begin(9600);
}

void loop()
{
 straightAdjust();
 //driveIndef();
 float dist_inch = measure_distance(); //check distance

  if (dist_inch < range)
  {
    switch(counter){
      case 0:
        firstTurn();
        break;
      case 1:
        secondTurn();
        break;
      case 2:
        thirdTurn();
        break;
      case 3:
        //fourthTurn();
        driveRamp();
        break;
      case 4:
        fourthTurn();
        break;
      case 5:
        fifthTurn();
        break;
      default:
        straightAdjust();
        counter = 0;
        break;
    }
  }
}

void firstTurn()
{
  drive(130, 180, 1200);
  drive(180, 110, 3300);
  counter = 1;
}

void secondTurn()
{
  drive(180, 130, 1300);
  drive(120, 180, 2800);
  counter = 2;
}

void thirdTurn() 
{
   drive(130, 180, 1200);
   drive(180, 110, 3550);
   
   drive(160, 160, 3000);
   adjustLeft(800);
   drive(135, 135, 5000);
   adjustLeft(300);
  counter = 4;
}

void fourthTurn() //90 degree
{
  drive(130, 180, 1000);
  drive(180, 110, 3400);
  drive(130, 180, 1400); //straigten TEST
  counter = 5;
}

//arch

void fifthTurn() //90 degree (same as fourth)
{
  drive(130, 180, 1000);
  drive(180, 110, 3300);
  drive(130, 180, 1200);//straigten TEST  
  drive(180, 180, 3000); //full speed till finish
  drive(90,  90,  5000); //stop
  counter = 0;
}


void readSerialPort() {
  msg = "";
  if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
          msg += (char)Serial.read();
      }
      Serial.flush();
  }
}

void driveIndef()
{
  ST1.write(speed-2);
  ST2.write(speed+2);
}

void drive(int speed1, int speed2, int delaytime)
{
  ST1.write(speed1);
  ST2.write(speed2);
  delay(delaytime);
}

void adjustRight(int delaytime)
{
 drive(speed, speed-30, delaytime);
}

void adjustLeft(int delaytime)
{
 drive(speed-30, speed, delaytime);
}
 
void straightAdjust()
{
 driveIndef();
 readSerialPort();

 if (msg=="C")
 {
  driveIndef();
 }
 else if (msg=="L")
 {
  adjustLeft(300);
 }
 else if (msg=="R")
 {
    adjustRight(300);
 }
}

float measure_distance()
{
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  inch_dis = duration * 0.034 / (2*2.54);
  return inch_dis;
}