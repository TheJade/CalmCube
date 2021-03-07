
//----------------LIBRARY------------------------------------------
#include <SPI.h>


//----------------CONSTANTS---AND---DEFINIES-------------------------
const int slaveSelectPin = 10;  // don't change unless necessary

#define P_FIRST_STATE_FUNCITON 1  // use a #define to make the program more readable, this one is a Pointer to the UserInput function
                        // use all caps when naming

#define P_RAIN_EFFECT 6

//----------------GLOBAL---VARIBLES----------------------------------
//don't add anything here, unless important to all states and functions
boolean bits [24] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};   // array of the data to be displayed, in True and False values
short state_pointer = P_RAIN_EFFECT;   //picks what state is currently run

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
  rainEffect();
}
/*  if (state_pointer == P_FIRST_STATE_FUNCITON)
  {
    //go to the first state function
    firstStateFunction();
  }
  else if (state_pointer == P_RAIN_EFFECT)
  {
    rainEffect();
  }
  else
    idle();
}*/


//-------------------STATE----FUNCTIONS-------------------------------
//will stay in each of these states an a pattern or main function is running

void firstStateFunction(){  // just an example, please pick more descriptive sames like: "colourFade"
  Serial.println("Running First State");
  bitsDisplay();
}

void idle() {
  //sits idle waiting until a certain time or user input
  //then changes the function_pointer to the state value wanted to run
  /*
    when user hits button
    state_pointer = 1
  */
}

//modifications Jade made------below
void rainEffect() {
  //fade in on the top then once it reaches max birghtness it falls then fades on the bottom
  //unsigned short's max num is 65535
  //static varibles don't get destroyed when the function ends
  //will add some randomization later to make the drops drip more randomly
  
  bool testing_mode = false; //make true if you want to see the serial output for testing
  
  unsigned int fade_length = 3000;  //milliseconds, 
  unsigned int fall_length = 250;   //milliseconds
  static bool temp_bits[24];
  unsigned short fade_rate = 2;     //increase to increase the speed the colour turns on or off
  static unsigned short drop[6] = {0, 500,1000,1500,2000,2500};    //contains the info for each drop, the drop[drop#][time_start_fade]
  static unsigned short level = 0; //layer the board will display
  
  for (int i = 0; i < 6; i++){    //makes the layer it's currently on high
    temp_bits[i] = (level == i);  //active high
  }
  if (level == 5){  // if top layer is to be displayed lights will grow
  
    LEDGrow(&temp_bits[6], drop, fade_length); //use temp_bits[6] cuz thats when the rgb starts
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    level = 0;
    
    if(testing_mode){serialPrintBits(&bits[0]);}  //this is just for testing
  }
  else if (level > 0 && level < 5){  // activates all but top and bottom levels
  
    dripFall(&temp_bits[6], drop, fade_length, fall_length, level); //use temp_bits[6] cuz thats when the rgb starts, could use pointers to save memory
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    level = level + 1;
    
    if(testing_mode){serialPrintBits(&bits[0]);}  //this is just for testing
  }
  else if (level == 0)  //for now this does the same thing as levels 1-4, will want to make it fade eventually
  {
    //the drops should stop and fade and have the time they should wait for now it just continues the dripping
    dripFall(&temp_bits[6], drop, fade_length, fall_length, level); //use temp_bits[6] cuz thats when the rgb starts
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    level = 1;
    
    restartDripStartTime(&drop[0], fade_length, fall_length); //don't need to check this all the time so it just goes on level 0
    
    if(testing_mode){serialPrintBits(&bits[0]);}  //this is just for testing
  }

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

void LEDGrow(bool *temp_bits, unsigned short drop[6], unsigned int fade_length){
  //is used for the top layer of the cube, will grow the lights
  //only considers using the blue light
  unsigned short brightness = 8;    //need to think of a better varible name
  for (int i = 0; i < 6; i++){
    unsigned long time_since_start = millis() - drop[i];
    if (time_since_start < (fade_length/5)) //probably a more efficient way of doing this
      brightness = 8;
    else if (time_since_start < (fade_length/5)*2)
      brightness = 5;
    else if (time_since_start < (fade_length/5)*3)
      brightness = 3;
    else if (time_since_start < (fade_length/5)*4)
      brightness = 2;
    else if (time_since_start < (fade_length-10)) //minus 10 so that it hits brightness = 0
      brightness = 1;
    else
      brightness = 0;
    if (time_since_start % brightness == 0){
      *(temp_bits + 2 + 3*i) = true;   //writes true to blue
    }
    else{
      *(temp_bits + 3*i) = false;       //writes false to red
      *(temp_bits + 1 + 3*i) = false;   //writes false to green
      *(temp_bits + 2 + 3*i) = false;   //writes false to blue
    }
  }
}

void dripFall(bool *temp_bits, unsigned short drop[6], unsigned int fade_length, unsigned int fall_length, unsigned int level){
  for (int i = 0; i < 6; i++){
    unsigned long time_since_start = millis() - drop[i]; //this would help with speed
    if (((fade_length + (4-level)*fall_length) < time_since_start) && (time_since_start < (fade_length + (5-level)*fall_length))){  //puts bounds on on region
      *(temp_bits + 2 + 3*i) = true;
    }
    else{
      *(temp_bits + 3*i) = false;       //writes false to red
      *(temp_bits + 1 + 3*i) = false;   //writes false to green
      *(temp_bits + 2 + 3*i) = false;   //writes false to blue
    }
  }
}

void tempCopyToBits(bool *temp){
  for (int i = 0; i < 24; i++){
    bits[i] = *(temp + i);
  }
}

void restartDripStartTime(unsigned short *drop, unsigned int fade_length, unsigned int fall_length){
  //this function loop the drips so they will drip again after they fall
  for (int i = 0; i < 6; i++){
    if (millis() - *(drop+i) > fade_length*2 + fall_length*4){
      *(drop + i) = millis();
    }
  }
}

void serialPrintBits(bool *temp){ //this is for testing 
    //testing
    //LSB first
      for(int i=0; i<24; i++){
        Serial.print(temp[i]);
      }
      Serial.println("");
}
