/*
  SD card file dump

  This example shows how to read a file from the SD card using the
  SD library and send it over the serial port.

  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

  created  22 December 2010
  by Limor Fried
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

*/

#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 redDac;
Adafruit_MCP4725 blueDac;
Adafruit_MCP4725 greenDac;



//DAC
#define DAC_RESOLUTION    (9)
const int redDacAddr = 0x60;
const int blueDacAddr = 0x61;
const int greenDacAddr = 0x62;

//SD Card Reader
const int chipSelect = 4;
const int voltageModifier = 5000;

// going to have to account for difference in the size of intervals between voltage
const int dacOneVolt = (1 * voltageModifier) / 4;
const int dacTwoVolt = ((2 * voltageModifier) / 4)-300;
const int dacThreeVolt = (3 * voltageModifier) / 5;
const int dacFourVolt = (4 * voltageModifier) / 5;
const int maxVolt = 4000;
const int maxColorValue = 255;

int red, green, blue;
File dataFile;
char debug [255];

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");

  if (redDac.begin(redDacAddr) && blueDac.begin(blueDacAddr) && greenDac.begin(greenDacAddr) ){
    Serial.println("MCP4725 Initialized Successfully.");
  }
  else{
    Serial.println("Failed to Initialize MCP4725.");
    // don't do anything more:
    while (1);
  }
  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  dataFile = SD.open("test.csv");
}


void loop() {
  String line;
  while (dataFile.available()) {
    Serial.println("here 2");
    char unparsed[13];
    line = readLine(dataFile);            
    line.toCharArray(unparsed, sizeof(unparsed));
    sscanf(unparsed, "%d, %d, %d", &red, &green, &blue);
    //sprintf(debug, "R:%d G:%d B:%d ", red, green, blue);    
    Serial.println("got here");
    transmitColors();
    delay(2000);
    Serial.println(debug);    
  }

  dataFile.close();
}

void transmitColors(){  
  float redVoltage =  ((float) red / maxColorValue) * maxVolt;
  redDac.setVoltage((int)redVoltage, false);    
  Serial.print("Red Voltage: ");
  Serial.println(redVoltage);

  float greenVoltage = ((float) green / maxColorValue) * maxVolt; 
  greenDac.setVoltage((int)greenVoltage, false);    //Set voltage to 1V
  Serial.print("Green Voltage: ");
  Serial.println(greenVoltage);

  float blueVoltage = ((float) blue / maxColorValue) * maxVolt;
  blueDac.setVoltage((int) blueVoltage, false);    //Set voltage to 1V  
  Serial.print("Blue Voltage: ");
  Serial.println(blueVoltage);
}


String readLine(File dataFile) {
  String inputLine;
  char c;
  while (c = dataFile.read()) {
    if (c != '\n') {
      inputLine += c;      
    } else {
      break;
    }
  }
  return inputLine;
}
