test = False #don't need to modify this any more for the testing or non testing modes
test_speed = 0.5   #just a delay in seconds so that the terminal read out isn't too quick for testing mode

#----------------LIBRARY------------------------------------------

try:
    import time # commonly used for timing (obviously)
    import RPi.GPIO as GPIO     #this is to control other pins besides the spi, for buttons and stuff
    import spidev   #ignore the error on this line, make sure this import is last
                    #this is the module that will control the pins, below is the best documentation I found
                    #   https://www.sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf  
                    
except:
    test = True
    print("Error occurred importing a libary, running testing mode instead...")

finally:
    print("Start")
    if not test:
        print("Raspberry Pi mode is active")
        

#----------------GLOBAL---CONSTANTS--------------------------------
RAIN_EFFECT = 2
SNAKE_EFFECT = 3
SLOW_DEMO = 4
TEST_EFFECT = 5
SIMPLE_TEST_EFFECT = 6
WAVE_EFFECT = 7

#----------------GLOBAL---VARIBLES----------------------------------
#don't add anything here, unless important to all states and function
try:
    statePointer = 7
    msg = [False for i in range(120)] #114 bits 108 for columns, 6 for rows
    runs = 0    #might need to loop if it gets too large
    level = 0
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
        spi.max_speed_hz = 20000  #this class attribute defines the max speed the data will be transfered to the device in hz
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
    elif statePointer == WAVE_EFFECT:
        waveEffect() 
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

def simpleTestEffect(): #should just turn on the first light on level 2 to LED 0 green LED 1 green
    global runs
    global level
    global msg
    level = 2
    msg[2] = True
    msg[7] = True
    msg[10] = True
    bitsDisplay()

def waveEffect():
    global runs     #!!! if you are going to modify a global value you must "  global VARIABLE_NAME   "!!!
    global level            #
    global msg
    global start_time
    global substate
    global colour_focus
    
    substate = 0
    start_time = time.time()
    on_length = 2 #on for 2 second per phase
    colour_focus = 4
    
    #-----Colours-------
    off = [0, 0, 0]
    if colour_focus == 4:
        colour_focus = 0
    if colour_focus == 0:       #blue
        colour = [0, 128, 255]         
    elif colour_focus == 1:     #dark blue
        colour = [51, 51, 255]
    elif colour_focus == 2:
        colour = [102, 0, 204]  #purple
     
    #Slice 1 - columns 1-5 - blue
    if substate == 0:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, colour, runs, 1)       #
            RGBdisplay(1, colour, runs, 1)       #
            RGBdisplay(2, colour, runs, 1)       #
            RGBdisplay(3, colour, runs, 1)       #
            RGBdisplay(4, colour, runs, 1)       #
            RGBdisplay(5, colour, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 1
            colour_focus += 1
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    
    #Slice 2 - columns 6-11 - dark blue
    elif substate == 1:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, colour, runs, 1)          #
            RGBdisplay(7, colour, runs, 1)          #
            RGBdisplay(8, colour, runs, 1)          #
            RGBdisplay(9, colour, runs, 1)          #
            RGBdisplay(10, colour, runs, 1)         #
            RGBdisplay(11, colour, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 2
            colour_focus += 1
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!

    #Slice 3 - columns 12-17 - purple
    elif substate == 2:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, colour, runs, 1)         #
            RGBdisplay(13, colour, runs, 1)         #
            RGBdisplay(14, colour, runs, 1)         #
            RGBdisplay(15, colour, runs, 1)         #
            RGBdisplay(16, colour, runs, 1)         #
            RGBdisplay(17, colour, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 3
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    
    #Slice 4 - columns 18-23 - purple
    elif substate == 3:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, colour, runs, 1)         #
            RGBdisplay(19, colour, runs, 1)         #
            RGBdisplay(20, colour, runs, 1)         #
            RGBdisplay(21, colour, runs, 1)         #
            RGBdisplay(22, colour, runs, 1)         #
            RGBdisplay(23, colour, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 4
            colour_focus -= 1
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
         
         
    #Slice 5 - columns 24-29 - dark blue
    elif substate == 4:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, colour, runs, 1)         #
            RGBdisplay(25, colour, runs, 1)         #
            RGBdisplay(26, colour, runs, 1)         #
            RGBdisplay(27, colour, runs, 1)         #
            RGBdisplay(28, colour, runs, 1)         #
            RGBdisplay(29, colour, runs, 1)         #
            RGBdisplay(30, off, runs, 1)         #
            RGBdisplay(31, off, runs, 1)         #
            RGBdisplay(32, off, runs, 1)         #
            RGBdisplay(33, off, runs, 1)         #
            RGBdisplay(34, off, runs, 1)         #
            RGBdisplay(35, off, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 5
            colour_focus -= 1
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
        
        
    #Slice 6 - columns 30-35 - dark blue
    elif substate == 4:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        elif level == 4:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        elif level == 3:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        elif level == 2:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        elif level == 1:    
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        elif level == 0:
            RGBdisplay(0, off, runs, 1)       #
            RGBdisplay(1, off, runs, 1)       #
            RGBdisplay(2, off, runs, 1)       #
            RGBdisplay(3, off, runs, 1)       #
            RGBdisplay(4, off, runs, 1)       #
            RGBdisplay(5, off, runs, 1)       #
            RGBdisplay(6, off, runs, 1)          #
            RGBdisplay(7, off, runs, 1)          #
            RGBdisplay(8, off, runs, 1)          #
            RGBdisplay(9, off, runs, 1)          #
            RGBdisplay(10, off, runs, 1)         #
            RGBdisplay(11, off, runs, 1)         #
            RGBdisplay(12, off, runs, 1)         #
            RGBdisplay(13, off, runs, 1)         #
            RGBdisplay(14, off, runs, 1)         #
            RGBdisplay(15, off, runs, 1)         #
            RGBdisplay(16, off, runs, 1)         #
            RGBdisplay(17, off, runs, 1)         #
            RGBdisplay(18, off, runs, 1)         #
            RGBdisplay(19, off, runs, 1)         #
            RGBdisplay(20, off, runs, 1)         #
            RGBdisplay(21, off, runs, 1)         #
            RGBdisplay(22, off, runs, 1)         #
            RGBdisplay(23, off, runs, 1)         #
            RGBdisplay(24, off, runs, 1)         #
            RGBdisplay(25, off, runs, 1)         #
            RGBdisplay(26, off, runs, 1)         #
            RGBdisplay(27, off, runs, 1)         #
            RGBdisplay(28, off, runs, 1)         #
            RGBdisplay(29, off, runs, 1)         #
            RGBdisplay(30, colour, runs, 1)         #
            RGBdisplay(31, colour, runs, 1)         #
            RGBdisplay(32, colour, runs, 1)         #
            RGBdisplay(33, colour, runs, 1)         #
            RGBdisplay(34, colour, runs, 1)         #
            RGBdisplay(35, colour, runs, 1)         #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 0
            colour_focus = 0
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!


#-------------------COMMON---FUNCTIONS-------------------------------
# functions often used by the different state functions

def bitsDisplay():
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
        for i in range(6):
            for j in range(6):      #the below formatting is likely more complicated then it needs to be
                print("{:<2}".format(35-i*6-(5-j))+ ":" + str(list(map(int, msg[(6 + (35-i*6-(5-j))*3):(9 + 3*(35-i*6-(5-j)))]))), end = '  ') #could probably do it in a nicer way
            print("\n")
    
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
    elif (runs > 2100000000):   #might cause an error
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
