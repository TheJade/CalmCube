
//----------------NOTES--------------------------------------------
/*
 0___1___2___3___4___5 
rgb_rgb_rgb_rgb_rgb_rgb
-->
rgb_rgb_rgb_rgb_rgb_rgb
-->                  
rgb_rgb_rgb_rgb_rgb_rgb
-->
rgb_rgb_rgb_rgb_rgb_rgb
-->
rgb_rgb_rgb_rgb_rgb_rgb
-->
rgb_rgb_rgb_rgb_rgb_rgb
*/

//----------------LIBRARY------------------------------------------
#include <SPI.h>


//----------------CONSTANTS---AND---DEFINIES-------------------------
const int slaveSelectPin = 10;  // don't change unless necessary

#define P_FIRST_STATE_FUNCITON 1  // use a #define to make the program more readable, this one is a Pointer to the UserInput function
                        // use all caps when naming


//----------------GLOBAL---VARIBLES----------------------------------
//don't add anything here, unless important to all states and functions
boolean bits [114];   // array of the data to be displayed, in True and False values
short state_pointer = 0;   //picks what state is currently run


//----------------SETUP----------------------------------------------
//will run once at the beginning of the program and never again
void setup() {
  Serial.begin(9600);       //needed for the Serial to communicate properly
  Serial.println("Start");  //prints the message to the Serial monitor 
  pinMode(slaveSelectPin, OUTPUT);  //sets up the SlaveSelect (Strobe) pin
  // initialize SPI:
  SPI.begin();
  SPI.setBitOrder(LSBFIRST);  //sets the default order of how the info is read
}


//------------------MAIN------LOOP-----------------------------------
//don't modify, will loop continuously 
void loop() {
  stateRelay();
}


//-------------------STATE----RELAY-----------------------------------
//uses the function pointer to 
void stateRelay() {
  if (state_pointer == P_FIRST_STATE_FUNCITON){
    //go to the first state function
    firstStateFunction();
  }
  else
    idle();
}


//-------------------STATE----FUNCTIONS-------------------------------
//will stay in each of these states an a pattern or main function is running
void idle(){
  //sits idle waiting until a certain time or user input
  //then changes the function_pointer to the state value wanted to run
  /*
  when user hits button
  state_pointer = 1
  */
}
void firstStateFunction(){  // just an example, please pick more descriptive sames like: "colourFade"
  //does something like
}


//-------------------COMMON---FUNCTIONS-------------------------------
// functions often used by the different state functions
void bitsDisplay(){
  //displays the entire bits array on the cube
  //
}



