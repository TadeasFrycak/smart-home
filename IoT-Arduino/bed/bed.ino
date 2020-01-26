#include <dht.h>

dht DHT;

#define DHT11_PIN 14

// Constants
const String ID = "i";
const String VALUE = "v";

const int LEFT_PIN = 5;
const int RIGHT_PIN = 9;
const int UP_PIN = 6;
const int DOWN_PIN = 10;

const int PIEZO_PIN = 16;
const int PIR1_PIN = 3;

const int MAX = 255;
const int MIN = 0;
const float CONSTANT = MAX/100;

const int DELAY = 10;
const int DELAY2 = 300;

const int MEASURE_TIME = 3000;

// Variables
int left = 0;
int right = 0;
int up = 0;
int down = 0;

int timer = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PIEZO_PIN, OUTPUT);
  pinMode(PIR1_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIR1_PIN), pir1_detection, RISING);
  piezo_pulse(50, 500, 1);
}

void loop() {
  if(Serial.available() > 0){
    String communication = Serial.readStringUntil('$');
    
    String id = strip(communication.substring(communication.indexOf("<" + ID + ">"), communication.indexOf("</" + ID + ">")));
    int value = strip(communication.substring(communication.indexOf("<" + VALUE + ">"), communication.indexOf("</" + VALUE + ">"))).toInt();

    if (id == "bed-toggle"){      
      if (value == 1) {
        fade(true);
      }
        
      else if (value == 0) {
        fade(false);
      }
    }

    else if (id == "bed-left") {
      left = value*MAX/100;
      analogWrite(LEFT_PIN, left);
    }
      
    else if (id == "bed-right") {
      right = value*MAX/100;
      analogWrite(RIGHT_PIN, right);
    }
      
    else if (id == "bed-up") {
      up = value*MAX/100;
      analogWrite(UP_PIN, up);
    }
      
    else if (id == "bed-down") {
      down = value*MAX/100;
      analogWrite(DOWN_PIN, down);
    }

    else if (id == "raspberry-halt") {
      piezo_pulse(50, 500, 1);
      fade(false);
    }
  }

  if (timer == MEASURE_TIME) {
    timer = 0;
    int chk = DHT.read11(DHT11_PIN);
    Serial.println("<temp>" + String(DHT.temperature) + "</temp><hum>" + String(DHT.humidity) + "</hum>");
  }

  timer += timer;
  delay(1);
}

String strip(String data) {
  return data.substring(data.indexOf(">")+1);
}

void pir1_detection() {
  Serial.println("<alarm>bed</alarm>");
}
void piezo_pulse(int pulse_pause, int pulse_end, int repeat) {
  for (int i=0; i<repeat; i++) {
    digitalWrite(PIEZO_PIN, HIGH);
    delay(pulse_pause);
    digitalWrite(PIEZO_PIN, LOW);
    delay(pulse_end);
  }
}

void write_led() {
  analogWrite(LEFT_PIN, left);
  analogWrite(RIGHT_PIN, right);
  analogWrite(UP_PIN, up);
  analogWrite(DOWN_PIN, down);
}

void fade(bool fade_in) {
  for (int i=MIN; i<(MAX+1); i++)
  {
    if (fade_in == true) {
      if (left < MAX) {
        left++;
      }
      if (right < MAX) {
        right++;
      }
      if (up < MAX) {
        up++;
      }
      if (down < MAX) {
        down++;
      }
    }

    else {
      if (left > MIN) {
        left--;
      }
      if (right > MIN) {
        right--;
      }
      if (up > MIN) {
        up--;
      }
      if (down > MIN) {
        down--;
      }
    }

  write_led();
  delay(DELAY);
  }
}
