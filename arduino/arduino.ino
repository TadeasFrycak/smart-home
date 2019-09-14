

void setup() {
  Serial.begin(9600);
}

void loop() {

    if(Serial.available() > 0){
      
      //String myString = "<pin>g1</pin><val>12</val>";
      String myString = Serial.readStringUntil('$');
      Serial.flush();
      
      //String pin = myString.substring(myString.indexOf("<pin>"),myString.indexOf("</pin>"));
      String value = myString.substring(myString.indexOf("<value>"),myString.indexOf("</value>"));

      //pin = pin.substring(pin.indexOf(">")+1);
      value = value.substring(value.indexOf(">")+1);
      //Serial.println(myString);
      //Serial.println("helo");
      analogWrite(9, map(myString.toInt(),0,100,0,255));
      
    }

  
  
  
}
