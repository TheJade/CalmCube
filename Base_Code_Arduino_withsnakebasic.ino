
//----------------LIBRARY------------------------------------------
#include <SPI.h>


//----------------CONSTANTS---AND---DEFINIES-------------------------
const int slaveSelectPin = 10;  // don't change unless necessary

#define P_FIRST_STATE_FUNCITON 1  // use a #define to make the program more readable, this one is a Pointer to the UserInput function
                        // use all caps when naming


//----------------GLOBAL---VARIBLES----------------------------------
//don't add anything here, unless important to all states and functions
boolean bits [24];
short state_pointer = 0;   //picks what state is currently run
short substate_p=0;

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
  snakeDisplay();
}


//-------------------COMMON---FUNCTIONS-------------------------------
// functions often used by the different state functions
void bitsDisplay(){
  //displays the entire bits array on the cube
  //
  
  int test=bits[0];
  snakeDisplay();
}

void snakeDisplay(){
  //displays snake pattern on slice
  //

  int i=0;
  int n=24;
  int j=0;
  static unsigned long start = millis();  //won't be reassigned each loop
  unsigned short on_length = 300; //value it holds for
if(substate_p==0)
{
    boolean startbits[]= {false,false,false,false,false,false,
    false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};//Turn everything off

for(j=0; j<n; j++)
    {
        bits[j] = startbits[j];
    }
if ((millis()-start) > on_length){
  substate_p = 1;
  start = millis();
}
    
}


else if(substate_p=1){
    boolean transferbits[]= {true,false,false,false,false,false,
    true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};//floor 1 LED 1 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 2;
    bitsDisplay();
  }
  
  
  else if(substate_p=2){
    boolean transferbits[]= {true,false,false,false,false,false,
    false,false,false,true,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};//floor 1 LED 2 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 3;
    bitsDisplay();
  }
  
  
  else if(substate_p=3){
    boolean transferbits[]= {true,false,false,false,false,false,
    false,false,false,false,false,false,true,false,false,false,false,false,false,false,false,false,false,false
};//floor 1 LED 3 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 4;
    bitsDisplay();
  }
  
  else if(substate_p=4){
    boolean transferbits[]= {true,false,false,false,false,false,
    false,false,false,false,false,false,false,false,false,true,false,false,false,false,false,false,false,false
};//floor 1 LED 4 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 5;
    bitsDisplay();
  }
  
  
else if(substate_p=5){
    boolean transferbits[]= {true,false,false,false,false,false,
    false,false,false,false,false,false,false,false,false,false,false,false,true,false,false,false,false,false
};//floor 1 LED 5 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 6;
    bitsDisplay();
  }
  
  
else if(substate_p=5){
    boolean transferbits[]= {true,false,false,false,false,false,
    false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,true,false,false
};//floor 1 LED 6 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 7;
    bitsDisplay();
  }

else if(substate_p=7){
    boolean transferbits[]= {false,true,false,false,false,false,
    true,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};//floor 2 LED 1 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 8;
    bitsDisplay();
  }
  
  
  else if(substate_p=8){
    boolean transferbits[]= {false,true,false,false,false,false,
    false,false,false,true,false,false,false,false,false,false,false,false,false,false,false,false,false,false
};//floor 2 LED 2 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 9;
    bitsDisplay();
  }
  
  
  else if(substate_p=9){
    boolean transferbits[]= {false,true,false,false,false,false,
    false,false,false,false,false,false,true,false,false,false,false,false,false,false,false,false,false,false
};//floor 2 LED 3 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 10;
    bitsDisplay();
  }
  
  else if(substate_p=10){
    boolean transferbits[]= {false,true,false,false,false,false,
    false,false,false,false,false,false,false,false,false,true,false,false,false,false,false,false,false,false
};//floor 2 LED 4 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 11;
    bitsDisplay();
  }
  
  
else if(substate_p=11){
    boolean transferbits[]= {false,true,false,false,false,false,
    false,false,false,false,false,false,false,false,false,false,false,false,true,false,false,false,false,false
};//floor 2 LED 5 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 12;
    bitsDisplay();
  }
  
  
else if(substate_p=12){
    boolean transferbits[]= {false,true,false,false,false,false,
    false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,true,false,false
};//floor 2 LED 6 red on

for(j=0; j<n; j++)
    {
        bits[j] = transferbits[j];
    }
    substate_p = 13;
    bitsDisplay();
  }
    
  
else
  {
    i++;
  }
  
  }
  
/*
[
  // 0     1     2     3     4     5   //"Floor"
 false,false,false,false,false,false
   //R1    G1    B1    R2    G2    B2    R3    G3    B3    R4    G4    B4    R5    G5    B5    R6    G6    B6 //light coulour and number
,false, false, false, false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,
]
*/