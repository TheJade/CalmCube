//the serial must be in Newline mode with 9600 baud

#include <SPI.h>

const int slaveSelectPin = 10;

const byte numChars = 32; //max length
char receivedChars[numChars]; // an array to store the received data

boolean newData = false;
unsigned int bits = 0b0000;
unsigned int bits2 = 0b11100000;
//0000000011100000
//RGBRGBRGBRGBRGB
void setup() {
  Serial.begin(9600);
  Serial.println("Start");
  Serial.println("Input the bits to be put in LSB first, in sets of 8 bits");
  pinMode(slaveSelectPin, OUTPUT);
  // initialize SPI:
  SPI.begin();
  SPI.setBitOrder(LSBFIRST);
  digitalWrite(slaveSelectPin, LOW);
  SPI.transfer(bits2); // using SPI.transfer(bits, 16); might allow 16 bits to be transfered
  SPI.transfer(bits);
  digitalWrite(slaveSelectPin, HIGH);
}

void loop() {
  takeInputBits();
  writeBits();
  //the display bits function from the other sketch
}

void takeInputBits(){
  recvWithEndMarker();
  convertToUnsignedInt();
}

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  // if (Serial.available() > 0) {
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
  
    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        ndx = 0;
        newData = true;
    }
  }
}

void convertToUnsignedInt() {
  if (newData == true) {
    bits= strtol(receivedChars, NULL, 2);
    newData = false;
  }
}

void writeBits()
{
   // digitalWrite(slaveSelectPin, LOW);
   // SPI.transfer(bits2); // using SPI.transfer(bits, 16); might allow 16 bits to be transfered
   // SPI.transfer(bits);
   // digitalWrite(slaveSelectPin, HIGH);
}
