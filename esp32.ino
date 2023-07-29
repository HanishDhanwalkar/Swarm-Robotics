
// Including the following libraries is a must to use the IoT functions and features of esp32
#include "WiFi.h"
#include "ESPAsyncWebSrv.h"

const char *ssid = "TechMinds_Bot1"; // This will show up when you turn on your mobile WIFI
const char *password = "12345687";   // change to more unique password

AsyncWebServer server(80); // These will start the webserver // If you don't know much, Ignore this line

// These pins are the Enable pins of the L293D motor driver which connects to esp32 gpio pins to implement the PWM function
int enable1_2 = 14;
int enable3_4 = 23;

// These pins are the input pins of l293d on the left side
int inp1 = 13;
int inp2 = 12;

// These pins are the input pins of l293d on the right side
int inp3 = 22; // Choose your GPIO pin of esp32 for the input 3
int inp4 = 21; // Choose your GPIO pin of esp32 for the input 4

int magnet = 27; // change it

int led = 2; // until now you must know what is the inbuilt led pin number of esp32.

int const id = 1; // change for each bot same as aruco marker id

void setup()
{

    // Fill in the blanks
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(enable1_2, OUTPUT);
    pinMode(enable3_4, OUTPUT);
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

    WiFi.softAP(ssid, password); // This sets your esp32's name as per above mentioned

    IPAddress IP = WiFi.softAPIP();

    // A bit of WEB DEV stuff
    server.on("/control", HTTP_GET, [](AsyncWebServerRequest *request)
              {
        if(request->hasArg("id") & (request->getParam("id")->value()).toInt()==id){    
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

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(1000);                     // wait for a second
    digitalWrite(LED_BUILTIN, LOW);  // turn the LED off by making the voltage LOW
    delay(1000);
}