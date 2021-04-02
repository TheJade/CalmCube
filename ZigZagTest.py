#TO DOs:
#   -maybe need to set the whole msg to False every once in a while to make sure Trues don't carry over 
#       from previous code
#   -auto go into test mode if not import spidev
#   -even out RGBdisplay function, meaning for 50% right now it is on for 50% then off for 50%,
#       better to alternate on and off for the whole time. Need to add (2**(3+mode)) somewhere I think
#   -remove runs as a parameter for RGBdisplay, can just call it, no need as a parameter,
#       still need to interate it outside once per layer cycle
#   -brightness function, can just untilize RGBdisplay but focus on birghtness idk


test = False #make True if wanting to print instead of run the code
test_speed = 0.1   #just a delay in seconds so that the terminal read out isn't too quick

#----------------LIBRARY------------------------------------------

try:
    import time # commonly used for timing (obviously)
    import RPi.GPIO as GPIO     #this is to control other pins besides the spi
    import spidev   #ignore the error on this line, make sure this import is last
                    #this is the module that will control the pins, below is the best documentation I found
                    #   https://www.sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf  
except:
    print("Error occurred importing a libary, don't worry if just testing")
finally:
    print("Start")
    if test:
        print("Testing mode is active")
    if not test:
        print("Raspberry Pi mode active")
        

#----------------GLOBAL---CONSTANTS--------------------------------
RAIN_EFFECT = 2
SNAKE_EFFECT = 3
SLOW_DEMO = 4
TEST_EFFECT = 5
SIMPLE_TEST_EFFECT = 6

#----------------GLOBAL---VARIBLES----------------------------------
#don't add anything here, unless important to all states and function
try:
    statePointer = 6
    msg = [False for i in range(120)] #114 bits 108 for columns, 6 for rows
    runs = 0    #might need to loop if it gets too large
    level = 0
    start_time = 0
    on_length = 0.1
    counter = 0

    start_time = time.time()

except:
    print("error in global varibles")

#testEffects global varibles (won't change for each function call) need to import it into the function with global VARBILE_NAME


#----------------SETUP----------------------------------------------
#will run once at the beginning of the program and never again
    #the setup code goes here
try:
    if not test:    #only runs if not in the testing mode
        spi = spidev.SpiDev(0, 0)   #this function creates an instance of the object spidev called spi (you can call it whatever you like). 
                                #   The first parameter is the spi pin group select.
                                #       Meaning, it will utilize all the pins (SPI0_MOSI, SPI0_MISO, SPI0_SCLK, SPI0_CE0_N) in the default spi group on the board
                                #       To have use the other set of pins I think we set the first parameter to 1
                                #       For the first version of the code we will only be utilizing the defualt spi pins on the GPIOs
                                #   The second parameter is the CE select (also known as slave select).
                                #       We use this for selecting what slave gets written to.
                                #       For our project we are just having a single line of slaves, so the default of CE0 works fine.
                                #       If wanted to add another slave we could simple declare another instance of the object (e.g. spi2 = spidev.SpiDev(0, 1))
        spi.max_speed_hz = 16384  #this class attribute defines the max speed the data will be transfered to the device in hz
                                #   For the raspberry pi don't set it any higher then 32 Mhz
                                #   There is a debate about permissible speed values, with some insisting
                                #   that the speed must be a power of 2, while others argue that it can be a
                                #   multiple of 2. Tests at least partially confirm that the latter is correct. It
                                #   was possible to set the speed at 3800 Hz, which appears to be a lower
                                #   limit, and at 4800 Hz. Neither of these values is a power of 2. 
except:
    print("error in setup")

#-------------------STATE----RELAY-----------------------------------
#uses the function pointer to
def stateRelay():
    if statePointer == SNAKE_EFFECT:
        snakeDisplay()
    elif statePointer == SLOW_DEMO:
        stateSlowDemo()
    elif statePointer == RAIN_EFFECT:
        rainEffect()
    elif statePointer == TEST_EFFECT:
        testEffect()
    elif statePointer == SIMPLE_TEST_EFFECT:
        simpleTestEffect()
    else:
        idle()
#-------------------STATE----FUNCTIONS-------------------------------
#will stay in each of these states an a pattern or main function is runnin
def idle():
    pass    #just needs something in it to not cause an error

def snakeDisplay():
    pass

def stateSlowDemo():
    pass

def rainEffect():
    pass

def simpleTestEffect(): #should just turn on the first light on level 2 to purple
    global runs
    global level
    global msg
    global counter
    global start_time
    level = 2

    for i in range(6):      #!!!need to assign first layers manually!!! could make a function but it is just 2 lines!!!
        msg[i] = (level == i)
    for i in range(36):
        RGBdisplay(i, [255 - (7*counter), (7*counter), 0], runs, 0)

    runs += 3

    if time.time() > start_time + 0.2:
        counter += 1
        start_time = time.time()
    if counter > 36:
        counter = 0
    bitsDisplay()



def testEffect():   #!!! i recommend you create sub fuctions of the state to keep it organzied !!! I did not in this example !!!
    global runs     #!!! if you are going to modify a global value you must "  global VARIABLE_NAME   "!!!
    global level            #don't need to do if you are just using/reading the value 
    global msg
    
    for i in range(6):      #!!!need to assign first layers manually!!! could make a function but it is just 2 lines!!!
        msg[i] = (level == i)
    if level == 5:
        RGBdisplay(0, [0, 0, 0], runs)          #should be off
        RGBdisplay(1, [8, 8, 8], runs, 0)    # white but brighter then then led 2
        RGBdisplay(2, [8, 8, 8], runs, 2)    # this one should be slightly dimmer
    elif level == 4:
        RGBdisplay(0, [3, 252, 252], runs)  #just a colour
        RGBdisplay(1, [3, 252, 252], runs)
        RGBdisplay(2, [3, 252, 252], runs)
    elif level == 3:
        RGBdisplay(0, [73, 68, 212], runs)     #purple
        RGBdisplay(1, [118, 115, 217], runs)   #lighter purple
        RGBdisplay(2, [166, 165, 212], runs)   #even lighter purple
    elif level == 2:
        RGBdisplay(0, [73, 68, 212], runs, 1)     #purple  with 16 bit colour 
        RGBdisplay(1, [118, 115, 217], runs, 1)   #lighter purple
        RGBdisplay(2, [166, 165, 212], runs, 1)   #even lighter purple 
    elif level == 1:    
        RGBdisplay(0, [73, 68, 212], runs, 2)     #purple  with 32 bit colour 
        RGBdisplay(1, [118, 115, 217], runs, 2)   #lighter purple
        RGBdisplay(2, [166, 165, 212], runs, 2)   #even lighter purple 
    elif level == 0:
        RGBdisplay(0, [255, 125, 244], runs, 2) #just nice colours
        RGBdisplay(1, [212, 255, 0], runs, 2)
        RGBdisplay(2, [255, 176, 107], runs, 2)
    else:
        raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
    level += 1
    if level > 5:       #!!!need to make it loop the layers!!!
        level = 0
    runs += 1           #!!!increment runs only once per layer cycle!!!
    bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!


#-------------------COMMON---FUNCTIONS-------------------------------
# functions often used by the different state functions

def bitsDisplay():
    global msg
    errorProtection()
    #spi.writebytes
    if not test:    #seems like there should be a more efficient way of doing this, we might be able to use spi.writebytes2(msg)
        byte = [0 for i in range(15)]
        for i in range(15):                 #cuz it can do it more efficently with numpy bool type arrays, look into it maybe
            for j in range(8):
                if msg[8*(14-i) + j]:
                    byte[i] += 2**(j)    #for MSB
        spi.writebytes(byte) 

    #testing output print           
    else:   #modify the below for test formatting
        print("Level:", list(map(int, msg[0:6])), "                                             Runs:", runs, ) #just some formatting don't worry
        for i in range(36):
            print("{:<2}".format(i)+ ":" + str(list(map(int, msg[(6 + i*3):(9 + 3*i)]))), end = '  ') #could probably do it in a nicer way
            if i % 6 == 5:
                print("\n")
    msg = [False for i in range(120)]   #resets the values of msg to zero so it can be updated to new values
    
def RGBdisplay(position, colour, runs, mode = 0):   #run to turn on or dim a perticular led
    #position is column of LED, 
    #colour is an array of size 3 defining the colour parameters, 
    #runs is a constant that must be passed, 
    #mode is the number of colour bits (0 is for 8 bit colour, 1 is for 16, 2 is for 32, etc.) the higher the mode the more accurate colours but longer it takes to update the led
    #   use mode 2 as max, it get flickery if it is at mode 3 or above
    global msg    #I'm not sure if this is needed but just in case I have it in
    for i in range(3):
        msg[6+position*3 + i] = (runs % (2**(3+mode)) < colour[i]/(2**(5-mode)))

def errorProtection():
    global msg  #i am pretty sure this can be removed but just in case I don't want to break the program so you, I left it
    global runs
    #error for multiple layers on
    more_than_one_level = 0
    for i in range(6):
        more_than_one_level += msg[i]
    if more_than_one_level > 1:
        print("Multiple levels active at once, ignoring for testing mode")
        if not test:
            raise Exception("More then one layer is on at a time") #causes an error to occur with the terminal print message
    #runs in too large or negaitive
    if (runs < 0):
        runs = 0
    elif (runs > 2100000000):
        runs = 0
    

#------------------MAIN------LOOP-----------------------------------
#don't modify, will loop continuously. This needs to be at the end of the program
#   we could make a file containing all the state funciton and common functions to make it a little more elegant

try:       #if an error occurs in the try then it will execute finally
    while True: #will loop forever
        stateRelay()  
        if test:
            time.sleep(test_speed)

finally:
    if not test:    #we might want to remove this conditional statement
        spi.close()     #properly shuts down the activated pins
        GPIO.cleanup()  #just incase any other pins were activated, might cause an error not sure just remove GPIO.cleanup() if it does
