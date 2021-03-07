// inslude the SPI library:
#include <SPI.h>

// set pin 10 as the slave select for the digital pot:

const int slaveSelectPin = 10;
int bits = 0b1000000; // Determines which LED is on
int bits_layer = 0b11111100; // Determines which layers are on
int bits_shift8 = 0b00000000; // Used to right-shift 8 bits of information
bool swi = false; // Determines if we want bits to be on LED_Reg1 or LED Reg2

void setup() {
  
  Serial.begin(9600);

  // set the slaveSelectPin as an output:

  pinMode(slaveSelectPin, OUTPUT);

  // initialize SPI:

  SPI.begin();
  Serial.println("Start:");
  SPI.setBitOrder(LSBFIRST);
}

/* Protocal that we will be using:
 * ||Layer_Reg ||LED_Reg1  ||LED_Reg2  ||
 * ||123|456|RG||BRG|BRG|BR||GBR|GBR|GB||
 * Currently this code doesnt account for the first LED's Red and Green.
 * 
 * This code shows how to shift 1-bit of information from LSB to MSB (doesn't work perfectly, however, it is a good start).
*/
void loop() {
    Serial.println(bits); // Prints the value of bits in base 10 to console.
    
    // Switching to LED_Reg1
    if(bits == 0b00000000 && swi)
    {
      swi = false;
      bits = 0b10000000;
    }
    
    // Switching to LED_Reg2
    if(bits == 0b00000000 && !swi)
    {
      swi = true;
      bits = 0b10000000;
    }
    
    // Writing to LED_Reg2
    if(swi)
    {
      digitalWrite(slaveSelectPin, LOW);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits_off);
      SPI.transfer(bits);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits_layer);
      digitalWrite(slaveSelectPin, HIGH);
      bits = bits >> 1;
    }
    
    // Writing to LED_Reg1
    if(!swi)
    {
      digitalWrite(slaveSelectPin, LOW);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits_shift8);
      SPI.transfer(bits);
      SPI.transfer(bits_layer);
      digitalWrite(slaveSelectPin, HIGH);
      bits = bits >> 1;
    }
    delay(50);
}

// Each line below shows how the transfer works basically everytime we use transfer it inputs the next 8bits of information that "bits" is set to.
// We get this effect where our previous 8bits is shifted 8bits, the below information shows the exact bits from lease significant to most significant.
//||RGB|RGB|RG||BRG|BRG|B||RGB|XXX|XX|
//||111|000|00||000|000|0||
//||000|111|00||111|000|0||
//||000|000|11||000|111|0||
//||111|000|00||000|000|1||
