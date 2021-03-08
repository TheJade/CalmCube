//----------------LIBRARY------------------------------------------
#include <SPI.h>


//----------------CONSTANTS---AND---DEFINIES-------------------------
const int slaveSelectPin = 10;  // don't change unless necessary

#define P_FIRST_STATE_FUNCITON 1  // use a #define to make the program more readable, this one is a Pointer to the UserInput function
                        // use all caps when naming

#define P_RAIN_EFFECT 6
#define P_SNAKE_EFFECT 2

//----------------GLOBAL---VARIBLES----------------------------------
//don't add anything here, unless important to all states and functions
boolean bits [24] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};   // array of the data to be displayed, in 1 and 0 values
short state_pointer = P_SNAKE_EFFECT;   //picks what state is currently run
short substate_p=0;


//----------------SETUP----------------------------------------------
//will run once at the beginning of the program and never again
void setup() {
  Serial.begin(9600);       //needed for the Serial to communicate properly
  //Serial.println("Start");  //prints the message to the Serial monitor 
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
  //snakeDisplay();
  stateSlowDemo();
  //rainEffect();
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
  //Serial.println("Running First State");
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

//Jade's slow demo code below-------------------------------------------------
void stateSlowDemo() {
  //turns on down right of top left led to purple, 
  //  but this is a demo so it is slow to start 
  //  then speeds up to demonstarate how we update the cube's display
  
  //bool testing_mode = false; //make true if you want to see the serial output for testing

  
  //adjustable values to get the timing right
  unsigned int time_per_layer_slow = 100;  //milliseconds
  unsigned int time_slow_mode = 5000;   //milliseconds
  static unsigned short colour_RGB[3] = {255, 0, 0}; //only has 8 levels of each colour, so not a huge change
  static unsigned short colour_RGB2[3] = {0, 0, 255};
  static unsigned short colour_RGB3[3] = {0, 255, 0}; //green//only has 8 levels of each colour, so not a huge change
  static unsigned short colour_RGB4[3] = {255, 255, 0}; //yellow//only has 8 levels of each colour, so not a huge change
  static unsigned short colour_RGB5[3] = {255, 0, 255}; //magenta//only has 8 levels of each colour, so not a huge change
  static unsigned short colour_RGB6[3] = {0, 255, 255}; //cyan//only has 8 levels of each colour, so not a huge change
  
  
  //state static varibles
  static unsigned short level = 0;  //layer the board will display
  static bool temp_bits[24];
  static unsigned long runs;  //number of times the RGBdisplay function has run
  
  temp_bits[8] = true;  //blue of first column will always be on to demonstarte the layers changeing, can just call this once but doesn't really matter
  
  for (int i = 0; i < 6; i++){    //makes the layer it's currently on high
    temp_bits[i] = (level == i);  //active high
  }
  if  (level == 0){
    RGBdisplay(&temp_bits[6], colour_RGB, runs);
    RGBdisplay(&temp_bits[9], colour_RGB, runs);
    RGBdisplay(&temp_bits[12], colour_RGB, runs);
    RGBdisplay(&temp_bits[18], colour_RGB, runs);
    RGBdisplay(&temp_bits[21], colour_RGB, runs);
    if (runs > 4000000000){ //prevents overflow even tho I think it would be fine
      runs = 0;
    }
    runs++;
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing
  }
  else if (level == 1){
    RGBdisplay(&temp_bits[6], colour_RGB2, runs);
    RGBdisplay(&temp_bits[9], colour_RGB2, runs);
    RGBdisplay(&temp_bits[12], colour_RGB2, runs);
    RGBdisplay(&temp_bits[18], colour_RGB2, runs);
    RGBdisplay(&temp_bits[21], colour_RGB2, runs);
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing
  }
 else if (level == 3){
    RGBdisplay(&temp_bits[6], colour_RGB4, runs);
    RGBdisplay(&temp_bits[9], colour_RGB4, runs);
    RGBdisplay(&temp_bits[12], colour_RGB4, runs);
    RGBdisplay(&temp_bits[18], colour_RGB4, runs);
    RGBdisplay(&temp_bits[21], colour_RGB4, runs);
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing
  }
  else if (level == 4){
    RGBdisplay(&temp_bits[6], colour_RGB5, runs);
    RGBdisplay(&temp_bits[9], colour_RGB5, runs);
    RGBdisplay(&temp_bits[12], colour_RGB5, runs);
    RGBdisplay(&temp_bits[18], colour_RGB5, runs);
    RGBdisplay(&temp_bits[21], colour_RGB5, runs);
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing
  }
  else if (level == 5){
    RGBdisplay(&temp_bits[6], colour_RGB6, runs);
    RGBdisplay(&temp_bits[9], colour_RGB6, runs);
    RGBdisplay(&temp_bits[12], colour_RGB6, runs);
    RGBdisplay(&temp_bits[18], colour_RGB6, runs);
    RGBdisplay(&temp_bits[21], colour_RGB6, runs);
    
    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing
  }
  else{

    tempCopyToBits(&temp_bits[0]);
    
    bitsDisplay(); //need to make sure this function is working
    
    //if(testing_mode){serialPrintBits(&bits[0]);}  // for testing

  }
  for (int i = 0; i < 24; i++){ //resets all the values to false so no values are retained from last update
    temp_bits[i] = false;
  }
  if  (millis() < time_slow_mode){
    delay(time_per_layer_slow);
  }
  level++;
  if (level > 5){
    level = 0;
  }
}

//modifications Jade made------below
void rainEffect() {
  //fade in on the top then once it reaches max birghtness it falls then fades on the bottom
  //unsigned short's max num is 65535
  //static varibles don't get destroyed when the function ends
  //will add some randomization later to make the drops drip more randomly
  
  bool testing_mode = 0; //make 1 if you want to see the serial output for testing
  
  unsigned int fade_length = 2000;  //milliseconds, 
  unsigned int fall_length = 100;   //milliseconds
  static bool temp_bits[24];
  unsigned short fade_rate = 2;     //increase to increase the speed the colour turns on or off
  static unsigned short drop[6] = {0, 250,500,750,1000,1250};    //contains the info for each drop, the drop[drop#][time_start_fade]
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

    if(millis() > 2500)
    {
      restartDripStartTime(&drop[0], fade_length, fall_length); //don't need to check this all the time so it just goes on level 0
    }
    
    if(testing_mode){serialPrintBits(&bits[0]);}  //this is just for testing
  }

}

void snakeDisplay()
{
  //displays snake pattern on slice
  int i=0;
  int n=24;
  int j=0;
  static unsigned long start = millis();  //won't be reassigned each loop
  unsigned short on_length = 300; //value it holds for
  
  if(substate_p == 0){
    boolean startbits[]= {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//Turn everything off
    for(j=0; j<n; j++){
      bits[j] = startbits[j];
    }
    if ((millis()-start) > on_length){
      substate_p = 1;
      start = millis();
      bitsDisplay();
    }  
  }
  
  else if(substate_p == 1)
  {
    boolean transferbits[]= {1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//floor 1 LED 1 red on
    for(j=0; j<n; j++)
    {
      bits[j] = transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 2;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 2)
  {
    boolean transferbits[]= {1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//floor 1 LED 2 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 3;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 3)
  {
    boolean transferbits[]= {1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0};//floor 1 LED 3 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 4;
      start = millis();
      bitsDisplay();
    }
  } 
  
  else if(substate_p == 4)
  {
    boolean transferbits[]= {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0};//floor 1 LED 4 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 5;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 5)
  {
    boolean transferbits[]= {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0};//floor 1 LED 5 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 6;
      start = millis();
      bitsDisplay();
    }
  }
    
  else if(substate_p == 6)
  {
    boolean transferbits[]= {1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0};//floor 1 LED 6 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 7;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 7)
  {
      boolean transferbits[]= {0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//floor 2 LED 1 red on
    for(j=0; j<n; j++)
    {
      bits[j] = transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 8;
      start = millis();
      bitsDisplay();
    }
  }
    
    
  else if(substate_p == 8)
  {
    boolean transferbits[]= {0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0};//floor 2 LED 2 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 9;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 9)
  {
    boolean transferbits[]= {0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0}; //floor 2 LED 3 red on
    for(j=0; j<n; j++)
      {
        bits[j] += transferbits[j];
      }
    if ((millis()-start) > on_length){
      substate_p = 10;
      start = millis();
      bitsDisplay();
    }
  } 
  
  else if(substate_p == 10)
  {
    boolean transferbits[]= {0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0}; //floor 2 LED 4 red on
    for(j=0; j<n; j++)
    {
      bits[j] += transferbits[j];
    }
    if ((millis()-start) > on_length)
    {
      substate_p = 11;
      start = millis();
      bitsDisplay();
    }
  }
  
  else if(substate_p == 11)
  {
    boolean transferbits[]= {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0}; //floor 2 LED 5 red on
    for(j=0; j<n; j++)
        {
            bits[j] += transferbits[j];
        }
    if ((millis()-start) > on_length){
      substate_p = 12;
      start = millis();
      bitsDisplay();
    }
  }  
  
  else if(substate_p == 12){
    boolean transferbits[]= {0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0}; //floor 2 LED 6 red on
    for(j=0; j<n; j++)
        {
            bits[j] += transferbits[j];
        }
    if ((millis()-start) > on_length){
      substate_p = 1;
      start = millis();
      bitsDisplay();
    }
  }  
  
  else
  {
    i++;
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
  //Serial.println(result);
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

//___Common____Functions___For___stateSlowDemo_____

void RGBdisplay (bool *temp_bits, unsigned short colour[3], unsigned long runs){  //this functions doesn't work perfectly
  //uses 8 different display values
  for (int i = 0; i < 3; i++){
    unsigned short RGB_amount = floor(colour[i]/29);  //floor just round down the value to the nearest whole number
    if(RGB_amount && (runs % (9 - RGB_amount) == 0)){  //doesn't quite work perfectly but it is close, issue with 50% on
      *(temp_bits + i) = true;
    }
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
      *(temp_bits + 2 + 3*i) = 1;   //writes 1 to blue
    }
    else{
      *(temp_bits + 3*i) = 0;       //writes 0 to red
      *(temp_bits + 1 + 3*i) = 0;   //writes 0 to green
      *(temp_bits + 2 + 3*i) = 0;   //writes 0 to blue
    }
  }
}

void dripFall(bool *temp_bits, unsigned short drop[6], unsigned int fade_length, unsigned int fall_length, unsigned int level){
  for (int i = 0; i < 6; i++){
    unsigned long time_since_start = millis() - drop[i]; //this would help with speed
    if (((fade_length + (4-level)*fall_length) < time_since_start) && (time_since_start < (fade_length + (5-level)*fall_length))){  //puts bounds on on region
      *(temp_bits + 2 + 3*i) = 1;
    }
    else{
      *(temp_bits + 3*i) = 0;       //writes 0 to red
      *(temp_bits + 1 + 3*i) = 0;   //writes 0 to green
      *(temp_bits + 2 + 3*i) = 0;   //writes 0 to blue
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
        //Serial.print(temp[i]);
      }
      //Serial.println("");
}
