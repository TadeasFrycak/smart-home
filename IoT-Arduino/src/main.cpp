#include <Arduino.h>

#define BAUD 9600

const String BEG_ID = "<i>";
const String END_ID = "</i>";
const String BEG_VALUE = "<v>";
const String END_VALUE = "</v>";
const String END_CHAR = "$";


/*------------------------------|ENCODER|------------------------------*/
class Encoder
{
private:
  bool locked = false;
  int n = LOW;
  int encoder0PinALast = LOW;
  int encoder0PinA = 3;
  int encoder0PinB = 4;
  int Button;
  int OldValue = 0;
public:
  int value = 0;
  int button = 0;
  Encoder(char pinA, char pinB);
  void lock();
  void unlock();
  void blink();
  bool changed();
};

Encoder::Encoder(char pinA, char pinB)
{
  encoder0PinA = pinA;
  encoder0PinB = pinB;
  pinMode(pinA,INPUT_PULLUP);
  pinMode(pinB,INPUT_PULLUP);
}

bool Encoder::changed()
{
  if (OldValue != value)
  {
    OldValue = value;
    return true;
  }
  return false;
}

void Encoder::lock()
{
  locked = true;
}

void Encoder::unlock()
{
  locked = false;
}

void Encoder::blink()
{
  n = digitalRead(encoder0PinA);
  if ((encoder0PinALast == LOW) && (n == HIGH) and locked == false) {
    delay(1);
    if (digitalRead(encoder0PinB) == LOW) {
      value--;
    } else {
      value++;
    }
  }
  encoder0PinALast = n;
}

Encoder encoder(4,5);








void PWMLedStrip(String value);
void MyFirstDevice(String value);


/*--------------------|Prostor pro deklarování promněných|--------------------*/
int predchozi_pot = 0;


/*--------------------|Prostor pro deklarování funkcí|--------------------*/
void select(String id, String value){

  if (id == "toggle-1") MyFirstDevice(value);
  if (id == "modal-slider-1") PWMLedStrip(value);

}

void checkForInput(){

  encoder.blink();
  if (encoder.changed()){
    Serial.println(BEG_ID + "percentage-1" + END_ID + BEG_VALUE + encoder.value + END_VALUE + END_CHAR);
  }

}

/*--------------------|nastavování pinModů|--------------------*/
void setUpIO(){

  pinMode(13,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(A0,INPUT);

}

/*--------------------|Funkce|--------------------*/
void MyFirstDevice(String value){

  int val = value.toInt();
  digitalWrite(13,val);

}

void PWMLedStrip(String value){

  int val = value.toInt();
  val = map(val,0,100,0,255);

  analogWrite(6,val);

}










/*--------------------|Setup|--------------------*/
void setup() {
  Serial.begin(BAUD);
  
  setUpIO();
}

void loop() {

    if(Serial.available() > 0){
      String received_string = Serial.readStringUntil('$');
      Serial.flush();
      
      String id    = received_string.substring(received_string.indexOf("<i>"),received_string.indexOf("</i>"));
      String value = received_string.substring(received_string.indexOf("<v>"),received_string.indexOf("</v>"));

      value = value.substring(value.indexOf(">")+1);
      id    = id.substring(id.indexOf(">")+1);

      select(id,value);
      
    }
    checkForInput();
  
}


