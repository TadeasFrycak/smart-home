#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Tadeasek2";                   // wifi ssid
const char* password =  "123456789";         // wifi password
const char* mqttServer = "192.168.0.100";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "username";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "12345678";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(espClient);


void MQTTOutput(String topic, String message);
char* StrToChar(String input);
void myLoop();
String subscribed[2] = {"home/toggle-1/modal-toggle-1","home/toggle-1/modal-toggle-2"};

void setup() {

  Serial.begin(115200);           // Begin serial communication 
  WiFi.begin(ssid, password);     // Begin WiFI connection

  // Wait until teh device is connected to the WiFi
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort); // Setting MQTT server
  client.setCallback(callback);

  while (!client.connected()) {           // Wait until client is connected to MQTT Broker
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }

//  client.publish("esp8266", "Hello Raspberry Pi");
//  client.subscribe("esp8266");

}

void callback(char* topic, byte* payload, unsigned int length) {

  String message = "";
  for (int i = 0; i < length; i++) { message += String((char)payload[i]); }
  
  MQTTOutput(String(topic),message);

}

void loop() { 

    for (int x = 0; x > sizeof(subscribed); x++)
    {
      client.subscribe(StrToChar(subscribed[0]));  
      client.loop();
    }
   myLoop();
}

char* StrToChar(String input){
  char charBuf[input.length() + 1];
  input.toCharArray(charBuf,input.length() + 1);
  return charBuf;
}



/*******************************************/
//                MY SCRIPT
/*******************************************/


void MQTTOutput(String topic, String message){
    
  if (topic == "toggle-1/modal-toggle-1"){
    if (message == "1") { digitalWrite(2, LOW); Serial.println("ON");}
    if (message == "0") { digitalWrite(2, HIGH); Serial.println("OFF");}
  }
  
}

void myLoop(){
  

  
//    if (digitalRead(16) == 1 && prewState == 0){
//      prewState = 1;
//      client.publish("home/toggle-1/modal-toggle-1", "1");
//   }
//   else if (digitalRead(16) == 0 && prewState == 1){
//      prewState = 0;
//      client.publish("home/toggle-1/modal-toggle-1", "0");
//   }
//
//   if (digitalRead(5) == 1 && prewState2 == 0){
//      prewState2 = 1;
//      statState2 ^= 1;
//      if (statState2 == 1) client.publish("home/toggle-1", "1");
//      if (statState2 == 0) client.publish("home/toggle-1", "0");
//      
//   }
//   else if (digitalRead(5) == 0){
//      prewState2 = 0; 
//   }
//
//     int Aread = analogRead(A0);
//  
//  if (Aread != prewSlider) {
//    prewSlider = Aread;
//    String incoming = String(prewSlider);
//
//    
//    client.publish("home/percentage-1", charBuf);
//  }

   
}
