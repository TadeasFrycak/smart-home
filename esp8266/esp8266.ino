#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Tadeasek2";                   // wifi ssid
const char* password =  "123456789";         // wifi password
const char* mqttServer = "192.168.0.100";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "username";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "12345678";  // if you don't have MQTT Password, no need input

int prewState = 0;
int prewState2 = 0;
int statState2 = 0;
int slider = 0;
int prewSlider = 0;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  
  pinMode(2, OUTPUT);     // Initialize GPIO2 pin as an output
  pinMode(16, INPUT);     // Initialize GPIO2 pin as an output
   pinMode(5, INPUT);     // Initialize GPIO2 pin as an output
   pinMode(A0, INPUT);     // Initialize GPIO2 pin as an output
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
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

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  String message = "";
  for (int i = 0; i < length; i++) {
    message += String((char)payload[i]);
  }
  
  if (String(topic) == "toggle-1>modal-toggle-1"){
    if (message == "1") { digitalWrite(2, LOW); Serial.println("ON");}
    if (message == "0") { digitalWrite(2, HIGH); Serial.println("OFF");}
  }

  Serial.print("Message:");
  Serial.print(message);

  Serial.println();
  Serial.println("-----------------------");

}

void loop() { 
    //client.publish("esp8266", "Hello Raspberry Pi");
    //client.subscribe("bed-toggle>bed-toggle");
    client.subscribe("home/toggle-1/modal-toggle-1");
    
    client.loop();
    client.subscribe("home/toggle-1/modal-toggle-2");
    client.loop();


   if (digitalRead(16) == 1 && prewState == 0){
      prewState = 1;
      client.publish("home/toggle-1/modal-toggle-1", "1");
   }
   else if (digitalRead(16) == 0 && prewState == 1){
      prewState = 0;
      client.publish("home/toggle-1/modal-toggle-1", "0");
   }

   if (digitalRead(5) == 1 && prewState2 == 0){
      prewState2 = 1;
      statState2 ^= 1;
      if (statState2 == 1) client.publish("home/toggle-1", "1");
      if (statState2 == 0) client.publish("home/toggle-1", "0");
      
   }
   else if (digitalRead(5) == 0){
      prewState2 = 0; 
   }

  int Aread = analogRead(A0);
  
  if (Aread + 5 < prewSlider || Aread - 5 > prewSlider) {
    prewSlider = Aread;
    String incoming = String(prewSlider);

    char charBuf[incoming.length() + 1];
    incoming.toCharArray(charBuf,incoming.length() + 1);
    client.publish("home/percentage-1", charBuf);
  }
   
 
}
