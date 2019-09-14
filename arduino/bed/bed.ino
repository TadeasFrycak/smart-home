// Constants
const String ID = "id";
const String TOGGLE = "value";

const String LEFT = "l";
const String RIGHT = "r";
const String UP = "u";
const String DOWN = "d";

const int LEFT_PIN = 5;
const int RIGHT_PIN = 9;
const int UP_PIN = 6;
const int DOWN_PIN = 10;

const int PIEZO_PIN = 16;

const int MAX = 255;
const int MIN = 0;
const float CONSTANT = MAX/100;

const int DELAY = 10;
const int DELAY2 = 300;

// Variables
int left = 0;
int right = 0;
int up = 0;
int down = 0;

bool can = NULL;

void setup() {
  Serial.begin(9600);
  pinMode(PIEZO_PIN, OUTPUT);
  piezo_pulse(50, 500, 3);
  piezo_pulse(500, 500, 1);
}

void loop() {
  if(Serial.available() > 0){
    String communication = Serial.readStringUntil('$');
    
    String id = strip(communication.substring(communication.indexOf("<" + ID + ">"), communication.indexOf("</" + ID + ">")));
    int toggle = strip(communication.substring(communication.indexOf("<" + TOGGLE + ">"), communication.indexOf("</" + TOGGLE + ">"))).toInt();

    if (id == "bed"){
      if (toggle == 50) {
        for (int i=0; i<10; i++) {
          analogWrite(LEFT_PIN, MAX);
          delay(DELAY2);
          analogWrite(LEFT_PIN, MIN);
          analogWrite(UP_PIN, MAX);
          delay(DELAY2);
          analogWrite(UP_PIN, MIN);
          analogWrite(RIGHT_PIN, MAX);
          delay(DELAY2);
          analogWrite(RIGHT_PIN, MIN);
          analogWrite(DOWN_PIN, MAX);
          delay(DELAY2);
          analogWrite(DOWN_PIN, MIN);
        }
      }
      
      else if (toggle == 100 && can == true) {
        can = false;
        fade(true);
      }
        
      else if (toggle == 0 && can == false) {
        can = true;
        fade(false);
      }

      else {
        left = strip(communication.substring(communication.indexOf("<" + LEFT + ">"), communication.indexOf("</" + LEFT + ">"))).toInt()*CONSTANT;
        right = strip(communication.substring(communication.indexOf("<" + RIGHT + ">"), communication.indexOf("</" + RIGHT + ">"))).toInt()*CONSTANT;
        up = strip(communication.substring(communication.indexOf("<" + UP + ">"), communication.indexOf("</" + UP + ">"))).toInt()*CONSTANT;
        down = strip(communication.substring(communication.indexOf("<" + DOWN + ">"), communication.indexOf("</" + DOWN + ">"))).toInt()*CONSTANT;

        write_led();
      }
    }
  }
}

String strip(String data) {
  return data.substring(data.indexOf(">")+1);
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
