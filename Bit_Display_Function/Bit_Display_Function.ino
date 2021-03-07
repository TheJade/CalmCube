
//----------------LIBRARY------------------------------------------
#include <SPI.h>


//----------------CONSTANTS---AND---DEFINIES-------------------------
const int slaveSelectPin = 10;  // don't change unless necessary

#define P_FIRST_STATE_FUNCITON 1  // use a #define to make the program more readable, this one is a Pointer to the UserInput function
                        // use all caps when naming


//----------------GLOBAL---VARIBLES----------------------------------
//don't add anything here, unless important to all states and functions
boolean bits [24] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};   // array of the data to be displayed, in True and False values
short state_pointer = P_FIRST_STATE_FUNCITON;   //picks what state is currently run

//----------------SETUP----------------------------------------------
//will run once at the beginning of the program and never again
void setup() {
  Serial.begin(9600);       //needed for the Serial to communicate properly
  Serial.println("Start");  //prints the message to the Serial monitor 
  pinMode(slaveSelectPin, OUTPUT);  //sets up the SlaveSelect (Strobe) pin
  // initialize SPI:
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);  //sets the default order of how the info is read
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
  Serial.println("Running First State");
  bitsDisplay();
}


//-------------------COMMON---FUNCTIONS-------------------------------
// functions often used by the different state functions
void bitsDisplay()
{
  //displays the entire bits array on the cube
  bool bits1[8], bits2[8], bits3[8]; 
  array8section(bits1, 0);
  array8section(bits2, 8);
  array8section(bits3, 16);

  
  digitalWrite(slaveSelectPin, LOW);
  
  SPI.transfer(bool2Int(bits3,8));
  SPI.transfer(bool2Int(bits2,8));
  SPI.transfer(bool2Int(bits1,8));
 
  digitalWrite(slaveSelectPin, HIGH);
}
int bool2Int(bool boolArray[], int size)
{
  int result = 0;
  for(int i = 0; i < size; i++)
  {
   result |= boolArray[i] << i;
  }
  Serial.println(result);
  return result;
}
void array8section(bool boolArray[], int n)
{
  for(int i = 0; i < 8; i++)
  {
    boolArray[i] = bits[n];
    n++;
  }
  
}
