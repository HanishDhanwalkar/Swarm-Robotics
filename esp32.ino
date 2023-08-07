#include <WiFi.h>
#include <HTTPClient.h>
#include "ESPAsyncWebSrv.h"
  
const char* ssid = "VN";
const char* password =  "halloween123";

AsyncWebServer server(80); 

int enable1_2 = 14;
int enable3_4 = 23;
int enable_magnet=26;

int inp1 = 13;
int inp2 = 12;

int inp3 = 22;
int inp4 = 21;

int magnet = 27; 

int led = 2; 

const String id="4";

void connectWiFi(){
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");  
}

void setup() {
  Serial.begin(115200);
  delay(4000);   //Delay needed before calling the WiFi.begin
  connectWiFi();
  HTTPClient http; 
  http.begin("http://192.168.122.118:8080/");  //Specify destination for HTTP request
   http.addHeader("Content-Type", "text/plain");             //Specify content-type header
   http.addHeader("id", id);
   http.addHeader("ip", WiFi.localIP().toString().c_str());    
   int httpResponseCode = http.POST("POSTING from ESP32");   //Send the actual POST request
   if(httpResponseCode>0){
    String response = http.getString(); //Get the response to the request
    Serial.println(httpResponseCode);   //Print return code
    Serial.println(response);           //Print request answer
   }else{
    Serial.println(httpResponseCode);
    }

      // Fill in the blanks
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(enable1_2, OUTPUT);
    pinMode(enable3_4, OUTPUT);
    pinMode(enable_magnet,OUTPUT);
    Serial.begin(115200);

    // The inputs
    // pinMode(int pinNum, MODE) is the function which sets the functional mode of the corresponding pin
    // where first argument is the pin number and the second argument is the mode eg. OUTPUT, INPUT.
    pinMode(inp1, OUTPUT);
    pinMode(inp2, OUTPUT);
    pinMode(inp3, OUTPUT);
    pinMode(inp4, OUTPUT);

    pinMode(led, OUTPUT);

    pinMode(magnet, OUTPUT);

    // We use the following function to run the bot at variable speed.
    analogWrite(enable1_2, 255); // analog write "255" corresponds to digital write "1"
    analogWrite(enable3_4, 255);
    digitalWrite(enable_magnet,HIGH);
    
  server.on("/control", HTTP_GET, [](AsyncWebServerRequest *request)
        {
        if(request->hasArg("id") & (request->getParam("id")->value()).toInt()==id.toInt()){    
            if(request->hasArg("vright")){ 
                String vright = request->getParam("vright")->value();
            // if '255' is the equivalent to digital '1', and '0' is eqvivalent to digial '0', We vary the pwm values to vary the speed of the motor
                if(vright.toInt()>=0){    
                    digitalWrite(inp1, HIGH);
                    digitalWrite(inp2, LOW);
                }else{
                    digitalWrite(inp1, LOW);
                    digitalWrite(inp2, HIGH);
                }  
                analogWrite(enable1_2, abs(vright.toInt()));   
                }
            if(request->hasArg("vleft")){ 
                String vleft = request->getParam("vleft")->value();
            // if '255' is the equivalent to digital '1', and '0' is eqvivalent to digial '0', We vary the pwm values to vary the speed of the motor
                if(vleft.toInt()>=0){    
                    digitalWrite(inp3, HIGH);
                    digitalWrite(inp4, LOW);
                }else{
                    digitalWrite(inp3, LOW);
                    digitalWrite(inp4, HIGH);
                }  
                analogWrite(enable3_4, abs(vleft.toInt()));   
                }
            if(request->hasArg("magnet")){  
               String val = request->getParam("magnet")->value(); 
               if(val.toInt()){
                digitalWrite(magnet,HIGH);
               }else{
                digitalWrite(magnet,LOW);
               }
                }           
            }
        request->send_P(200, "text/plain", ""); });
    server.begin();
}
  
void loop() {
  // Serial.println("Connected");
}