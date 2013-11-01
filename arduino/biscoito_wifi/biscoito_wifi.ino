/*
  Biscoitinho da Sorte
 
Esse Sketch conecta a impressora em um servidor utilizando
o Shield Ethernet e aciona a impressao atraves do apertar de
um botao.

O sistema esta configurado para operar com um IP Dinamico para
o cliente (a impressora) e um ip fixo para o servidor.

 Circuito:
* Impressora Termica conectada com SoftwareSerial nos pinos 2,3.
* Botao conectado no pino 5.
* Ethernet shield conectado nos pinos 10, 11, 12, 13
 
 Codigo Ethernet original:
 http://arduino.cc/en/Tutorial/WebClientRepeating

 Esse codigo esta distribuido em dominio publico.
 
 */

#include <SPI.h>
#include <SoftwareSerial.h>
#include <WiFly.h>
#include "Credentials.h"

//Thermal Vars
#define BUFFER_SIZE 800
SoftwareSerial Thermal(2, 3); //number of thermal printer pin
int header = 0;
int heatTime = 80;
int heatInterval = 255;
char printDensity = 15; 
char printBreakTime = 15;

//Button Vars
const int buttonPin = 5;     // pino do botao
int buttonState = 0;         // variable for reading the pushbutton status
int buttonPressed = 0;

char server[] = "apps.thacker.com.br";
Client client(server, 80);

unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 60*100;  // delay between updates, in milliseconds

void setup() {
  
  //General
  Serial.begin(9600); // start serial port
  delay(1000); //Wait for modules to load
  
  //Button Setup
  pinMode(buttonPin, INPUT);
  digitalWrite(buttonPin, HIGH);

  //Thermal Setup
  Thermal.begin(19200); // to write to our new printer
  initPrinter();
  Serial.println("Printer ready"); 
  
  //Ethernet Setup
  WiFly.begin();
  
  if (!WiFly.join(ssid)) {
    Serial.println("Association failed.");
    while (1) {
      // Hang on failure.
    }
  }  
  Serial.print("WAN ready: ");
  Serial.println(WiFly.ip());
}

void loop() {
  //Setting buttonpressed flag
  //Serial.println(digitalRead(buttonPin));
  if (digitalRead(buttonPin) != buttonState) {
    buttonState = digitalRead(buttonPin);
    if (buttonState==LOW) {
        // if you're not connected, and ten seconds have passed since
        // your last connection, then connect again and send data:
        if(!client.connected() && (millis() - lastConnectionTime > postingInterval)) {
          httpRequest();
        }
      }
    }
  
  //Checking for ethernet incoming bytes
  if (client.available()) {
    uint8_t header = 0;
    uint8_t buffer[BUFFER_SIZE];
    uint8_t pos = 0;
    while(client.available() > 0 && pos < BUFFER_SIZE) {
      if (header == 1) {
      buffer[pos++] = client.read(); //Take a character from serial port and check what it is   
      }
      else if (client.read() == '\x03') {
        header = 1;
        pos = 0;
      }
      
      if (pos > 0) {
        delay(10);
        Thermal.write(buffer, pos);
        Serial.write(buffer, pos);
        pos = 0;
      }
    }
  }
  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
  // store the state of the connection for next time through
  // the loop:
  lastConnected = client.connected();
}


void initPrinter()
{
 //Modify the print speed and heat
 Thermal.write(27);
 Thermal.write(55);
 Thermal.write(7); //Default 64 dots = 8*('7'+1)
 Thermal.write(heatTime); //Default 80 or 800us
 Thermal.write(heatInterval); //Default 2 or 20us
 //Modify the print density and timeout
 Thermal.write(18);
 Thermal.write(35);
 int printSetting = (printDensity<<4) | printBreakTime;
 Thermal.write(printSetting); //Combination of printDensity and printBreakTime
 //Latin
 Thermal.write(27);
 Thermal.write(82);
 Thermal.write(12); 
 }

// this method makes a HTTP connection to the server:
void httpRequest() {
  // if there's a successful connection:
  if (client.connect()) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println("GET /biscoitinho HTTP/1.1");
    client.println("Host: apps.thacker.com.br");
    client.println("User-Agent: arduino-ethernet");
    client.println("Connection: close");
    client.println();
  
    // note the time that the connection was made:
    lastConnectionTime = millis();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println("disconnecting.");
    client.stop();
  }
}




