#TO DOs:
#   -maybe need to set the whole msg to False every once in a while to make sure Trues don't carry over 
#       from previous code
#   -auto go into test mode if not import spidev
#   -even out RGBdisplay function, meaning for 50% right now it is on for 50% then off for 50%,
#       better to alternate on and off for the whole time. Need to add (2**(3+mode)) somewhere I think
#   -remove runs as a parameter for RGBdisplay, can just call it, no need as a parameter,
#       still need to interate it outside once per layer cycle
#   -brightness function, can just untilize RGBdisplay but focus on birghtness idk


test = False #don't need to modify this any more for the testing or non testing modes
test_speed = 1   #just a delay in seconds so that the terminal read out isn't too quick for testing mode

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
FOCUS_EFFECT = 7
ON_IDLE_EFFECT = 8

#----------------GLOBAL---VARIBLES----------------------------------
#don't add anything here, unless important to all states and function
try:
    statePointer = 7
    msg = [False for i in range(120)] #114 bits 108 for columns, 6 for rows
    runs = 0    #might need to loop if it gets too large
    level = 0
    setup = True
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
        spi.max_speed_hz = 10000000  #this class attribute defines the max speed the data will be transfered to the device in hz
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
    elif statePointer == FOCUS_EFFECT:
        focusEffect() 
    elif statePointer == ON_IDLE_EFFECT:
        on_idle() 
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
    
def on_idle():
    global runs     #!!! if you are going to modify a global value you must "  global VARIABLE_NAME   "!!!
    global level            #
    global msg
    global start_time
    global substate
    global colour_focus
    global setup

    on_length = 0.1 #on for .5 second per phase
    
    if setup:   #runs once to set up the varibles correctly
        substate = 0
        start_time = time.time()
        colour_focus = 0
        setup = False
    
    if colour_focus == 66:
        colour_focus =0
    if colour_focus == 0:
        x=0         #Blue
        y=0         #
        z=255       #
    elif colour_focus == 1:
        x=0        #blue
        y=60          #
        z=255        #
    elif colour_focus == 2:
        x=0         #blue
        y=94           #
        z=255         #
    elif colour_focus == 3:
        x=0       #blue
        y=123         #
        z=255       #
    elif colour_focus == 4:
        x=0       #blue
        y=153         #
        z=255         #
    elif colour_focus == 5:
        x=0       #blue
        y=170       #
        z=255         #
    elif colour_focus == 6:
        x=0       #blue
        y=183       #
        z=255         #
    elif colour_focus == 7:
        x=0       #blue
        y=200       #
        z=255        #
    elif colour_focus == 8:
        x=0       # blue
        y=213     #
        z=255       #
    elif colour_focus == 9:
        x=0        # Turquoise
        y=229      #
        z=255      #
    elif colour_focus == 10:
        x=0        # Turquoise
        y=242      #
        z=255      #
    elif colour_focus == 11:
        x=0        # Turquoise
        y=255      #
        z=255      #
    elif colour_focus == 12:
        x=0        # Turquoise
        y=255      #
        z=234      #
    elif colour_focus == 13:
        x=0        # Turquoise
        y=255      #
        z=213      #
    elif colour_focus == 14:
        x=0        # Turquoise
        y=255      #
        z=204      #
    elif colour_focus == 15:
        x=0        # Turquoise
        y=255      #
        z=195      #
    elif colour_focus == 16:
        x=0        # Turquoise
        y=255      #
        z=174      #
    elif colour_focus == 17:
        x=0        # green
        y=255      #
        z=153      #
    elif colour_focus == 18:
        x=0        # green
        y=255      #
        z=140      #
    elif colour_focus == 19:
        x=0        # green
        y=255      #
        z=128      #
    elif colour_focus == 20:
        x=0        # green
        y=255      #
        z=106      #
    elif colour_focus == 21:
        x=0        # green
        y=255      #
        z=85      #
    elif colour_focus == 22:
        x=0        # green
        y=255      #
        z=64      #
    elif colour_focus == 23:
        x=0        # green
        y=255      #
        z=30      #
    elif colour_focus == 24:
        x=0        # green
        y=255      #
        z=13      #
    elif colour_focus == 25:
        x=0        # green
        y=255      #
        z=0      #
    elif colour_focus == 26:
        x=26        # green
        y=255      #
        z=0      #
    elif colour_focus == 27:
        x=60        # green
        y=255      #
        z=0      #
    elif colour_focus == 28:
        x=89        # green
        y=255      #
        z=0      #
    elif colour_focus == 29:
        x=123        # yellow green
        y=255      #
        z=0      #
    elif colour_focus == 30:
        x=149        # yellow green
        y=255      #
        z=0      #
    elif colour_focus == 31:
        x=174        # yellow green
        y=255      #
        z=0      #
    elif colour_focus == 32:
        x=208        # yellow green
        y=255      #
        z=0      #
    elif colour_focus == 33:
        x=238        # yellow
        y=255      #
        z=0      #
    elif colour_focus == 34:
        x=255        # yellow
        y=255      #
        z=0      #
    elif colour_focus == 35:
        x=255        # yellow
        y=230      #
        z=0      #
    elif colour_focus == 36:
        x=255        # yellow
        y=200      #
        z=0      #
    elif colour_focus == 37:
        x=255        # yellow
        y=174      #
        z=0      #
    elif colour_focus == 38:
        x=255        # orange
        y=153      #
        z=0      #
    elif colour_focus == 39:
        x=255        # orange
        y=140      #
        z=0      #
    elif colour_focus == 40:
        x=255        # orange
        y=123      #
        z=0      #
    elif colour_focus == 41:
        x=255        # orange
        y=106      #
        z=0      #
    elif colour_focus == 42:
        x=255        # orange
        y=85      #
        z=0      #
    elif colour_focus == 43:
        x=255        # orange
        y=64      #
        z=0      #
    elif colour_focus == 44:
        x=255        # red
        y=42      #
        z=0      #
    elif colour_focus == 45:
        x=255        # red
        y=0      #
        z=0      #
    elif colour_focus == 46:
        x=255        # red
        y=0      #
        z=43      #
    elif colour_focus == 47:
        x=255        # red
        y=0      #
        z=64      #
    elif colour_focus == 48:
        x=255        # red
        y=0      #
        z=85      #
    elif colour_focus == 49:
        x=255        # pink
        y=0      #
        z=106      #
    elif colour_focus == 50:
        x=255        # pink
        y=0      #
        z=128      #
    elif colour_focus == 51:
        x=255        # pink
        y=0      #
        z=153      #
    elif colour_focus == 52:
        x=255        # pink
        y=0      #
        z=179      #
    elif colour_focus == 53:
        x=255        # pink
        y=0      #
        z=195      #
    elif colour_focus == 54:
        x=255        # pink
        y=0      #
        z=221      #
    elif colour_focus == 55:
        x=255        # pink
        y=0      #
        z=247      #
    elif colour_focus == 56:
        x=255        # pink
        y=0      #
        z=255      #
    elif colour_focus == 57:
        x=221        # purple
        y=0      #
        z=255      #
    elif colour_focus == 58:
        x=208        # purple
        y=0      #
        z=255      #
    elif colour_focus == 59:
        x=187        # purple
        y=0      #
        z=255      #
    elif colour_focus == 60:
        x=166        # purple
        y=0      #
        z=255      #
    elif colour_focus == 61:
        x=144        # purple
        y=0      #
        z=255      #
    elif colour_focus == 62:
        x=128        # purple
        y=0      #
        z=255      #
    elif colour_focus == 63:
        x=106        # purple blue
        y=0      #
        z=255      #
    elif colour_focus == 64:
        x=81        # purple blue
        y=0      #
        z=255      #
    elif colour_focus == 65:
        x=51        # purple blue
        y=0      #
        z=255      #
    
    if substate == 0:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 4:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 3:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 2:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 1:    
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 0:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 0 #Probaly don't need this statement
            start_time = time.time() #increment time
            colour_focus += 1        #increment to get next colour
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!

def focusEffect():   #
    global runs     #!!! if you are going to modify a global value you must "  global VARIABLE_NAME   "!!!
    global level            #
    global msg
    global start_time
    global substate
    global colour_focus
    global setup

    on_length = 0.3 #on for 1 second per phase
    
    if setup:   #runs once to set up the varibles correctly
        substate = 0
        start_time = time.time()
        colour_focus = 0
        setup = False
    
    if colour_focus == 20:
        colour_focus =0
    if colour_focus == 0:
        x=152         #purple
        y=3           #
        z=252         #
    elif colour_focus == 1:
        x=136         #purple
        y=3       #
        z=252       #
    elif colour_focus == 2:
        x=111         #purple blue
        y=3       #
        z=252         #
    elif colour_focus == 3:
        x=73       #blue
        y=3       #
        z=252       #
    elif colour_focus == 4:
        x=3       #blue
        y=19       #
        z=252       #
    elif colour_focus == 5:
        x=3       # blue
        y=86       #
        z=252       #
    elif colour_focus == 6:
        x=3       #Light blue
        y=152       #
        z=252       #
    elif colour_focus == 7:
        x=3       #Light blue
        y=194       #
        z=252       #
    elif colour_focus == 8:
        x=3       # turquoise
        y=227      #
        z=252       #
    elif colour_focus == 9:
        x=3        # turquoise
        y=252        #
        z=231       #
    elif colour_focus == 10:
        x=3        # turquoise green
        y=252        #
        z=194       #
    elif colour_focus == 11:
        x=3        # light green
        y=252        #
        z=161       #
    elif colour_focus == 12:
        x=3        # green
        y=252        #
        z=98       #
    elif colour_focus == 13:
        x=0        #  green
        y=186        #
        z=71       #
    elif colour_focus == 14:
        x=14        # dark green
        y=130        #
        z=43       #
    elif colour_focus == 15:
        x=9        # turquoise dark green
        y=77        #
        z=54       #
    elif colour_focus == 16:
        x=9        # dark turquoise 
        y=77        #
        z=72       #
    elif colour_focus == 17:
        x=9        # dark turqoise blue
        y=64        #
        z=77       #
    elif colour_focus == 18:
        x=9        # dark blue
        y=34        #
        z=77       #
    elif colour_focus == 19:
        x=38       # dark purple
        y=9        #
        z=77       #
    
    if substate == 0:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 4:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 3:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 2:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 1:    
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 0:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 1    
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 1:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 2    
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 2:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!                                                 ###
        if ((time.time() - start_time)>on_length):
            substate = 3
            start_time = time.time() #increment time
            colour_focus += 1        #increment to get next colour
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 3:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)          #
            RGBdisplay(1, [0, 0, 0], runs)          #
            RGBdisplay(2, [0, 0, 0], runs)          #
            RGBdisplay(3, [0, 0, 0], runs)          #
            RGBdisplay(4, [0, 0, 0], runs)          #
            RGBdisplay(5, [0, 0, 0], runs)          #
            RGBdisplay(6, [0, 0, 0], runs)          #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)         #
            RGBdisplay(12, [0, 0, 0], runs)         #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)         #
            RGBdisplay(18, [0, 0, 0], runs)         #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)         #
            RGBdisplay(24, [0, 0, 0], runs)         #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)         #
            RGBdisplay(30, [0, 0, 0], runs)         #
            RGBdisplay(31, [0, 0, 0], runs)         #
            RGBdisplay(32, [0, 0, 0], runs)         #
            RGBdisplay(33, [0, 0, 0], runs)         #
            RGBdisplay(34, [0, 0, 0], runs)         #
            RGBdisplay(35, [0, 0, 0], runs)         #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 4    
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 4:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 4:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)          #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)          #
        elif level == 3:
            RGBdisplay(0, [x, y, z], runs, 1)           #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)           #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 2:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 1:    
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 0:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 5
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 5:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 6
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 6:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!                                                 ###
        if ((time.time() - start_time)>on_length):
            substate = 7
            start_time = time.time() #increment time
            colour_focus += 1        #increment to get next colour
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 7:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)              #blue
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 8
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 8:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 4:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 3:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 2:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 1:    
            RGBdisplay(0, [0, 0, 0], runs)              #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        elif level == 0:
            RGBdisplay(0, [0, 0, 0], runs)              #entire off
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [0, 0, 0], runs)              #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [0, 0, 0], runs)             #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [0, 0, 0], runs)             #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 9
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 9:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 4:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 3:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 2:
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 1:    
            RGBdisplay(0, [x, y, z], runs, 1)       #
            RGBdisplay(1, [0, 0, 0], runs)              #
            RGBdisplay(2, [0, 0, 0], runs)              #
            RGBdisplay(3, [0, 0, 0], runs)              #
            RGBdisplay(4, [0, 0, 0], runs)              #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [0, 0, 0], runs)              #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [0, 0, 0], runs)             #
            RGBdisplay(12, [0, 0, 0], runs)             #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [0, 0, 0], runs)             #
            RGBdisplay(18, [0, 0, 0], runs)             #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [0, 0, 0], runs)             #
            RGBdisplay(24, [0, 0, 0], runs)             #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [0, 0, 0], runs)             #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [0, 0, 0], runs)             #
            RGBdisplay(32, [0, 0, 0], runs)             #
            RGBdisplay(33, [0, 0, 0], runs)             #
            RGBdisplay(34, [0, 0, 0], runs)             #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 0:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [0, 0, 0], runs)              #
            RGBdisplay(8, [0, 0, 0], runs)              #
            RGBdisplay(9, [0, 0, 0], runs)              #
            RGBdisplay(10, [0, 0, 0], runs)             #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [0, 0, 0], runs)             #
            RGBdisplay(14, [0, 0, 0], runs)             #
            RGBdisplay(15, [0, 0, 0], runs)             #
            RGBdisplay(16, [0, 0, 0], runs)             #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [0, 0, 0], runs)             #
            RGBdisplay(20, [0, 0, 0], runs)             #
            RGBdisplay(21, [0, 0, 0], runs)             #
            RGBdisplay(22, [0, 0, 0], runs)             #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [0, 0, 0], runs)             #
            RGBdisplay(26, [0, 0, 0], runs)             #
            RGBdisplay(27, [0, 0, 0], runs)             #
            RGBdisplay(28, [0, 0, 0], runs)             #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 10
            start_time = time.time() #increment time
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!
    elif substate == 10:   
        for i in range(6):      #
            msg[i] = (level == i)
        if level == 5:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 4:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 3:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 2:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 1:    
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        elif level == 0:
            RGBdisplay(0, [x, y, z], runs, 1)       #Blue entire level
            RGBdisplay(1, [x, y, z], runs, 1)       #
            RGBdisplay(2, [x, y, z], runs, 1)       #
            RGBdisplay(3, [x, y, z], runs, 1)       #
            RGBdisplay(4, [x, y, z], runs, 1)       #
            RGBdisplay(5, [x, y, z], runs, 1)       #
            RGBdisplay(6, [x, y, z], runs, 1)       #
            RGBdisplay(7, [x, y, z], runs, 1)       #
            RGBdisplay(8, [x, y, z], runs, 1)       #
            RGBdisplay(9, [x, y, z], runs, 1)       #
            RGBdisplay(10, [x, y, z], runs, 1)      #
            RGBdisplay(11, [x, y, z], runs, 1)      #
            RGBdisplay(12, [x, y, z], runs, 1)      #
            RGBdisplay(13, [x, y, z], runs, 1)      #
            RGBdisplay(14, [x, y, z], runs, 1)      #
            RGBdisplay(15, [x, y, z], runs, 1)      #
            RGBdisplay(16, [x, y, z], runs, 1)      #
            RGBdisplay(17, [x, y, z], runs, 1)      #
            RGBdisplay(18, [x, y, z], runs, 1)      #
            RGBdisplay(19, [x, y, z], runs, 1)      #
            RGBdisplay(20, [x, y, z], runs, 1)      #
            RGBdisplay(21, [x, y, z], runs, 1)      #
            RGBdisplay(22, [x, y, z], runs, 1)      #
            RGBdisplay(23, [x, y, z], runs, 1)      #
            RGBdisplay(24, [x, y, z], runs, 1)      #
            RGBdisplay(25, [x, y, z], runs, 1)      #
            RGBdisplay(26, [x, y, z], runs, 1)      #
            RGBdisplay(27, [x, y, z], runs, 1)      #
            RGBdisplay(28, [x, y, z], runs, 1)      #
            RGBdisplay(29, [x, y, z], runs, 1)      #
            RGBdisplay(30, [x, y, z], runs, 1)      #
            RGBdisplay(31, [x, y, z], runs, 1)      #
            RGBdisplay(32, [x, y, z], runs, 1)      #
            RGBdisplay(33, [x, y, z], runs, 1)      #
            RGBdisplay(34, [x, y, z], runs, 1)      #
            RGBdisplay(35, [x, y, z], runs, 1)      #
        else:
            raise Exception("An error occured with the testEffect Level, level is not a value from 0-5")
        level += 1
        if level > 5:       #!!!need to make it loop the layers!!!
            level = 0
        runs += 1           #!!!increment runs only once per layer cycle!!!
        if ((time.time() - start_time)>on_length):
            substate = 0    #goes to start on focus 
            start_time = time.time() #increment time
            colour_focus += 1        #increment to get next colour
        bitsDisplay()       #!!!need to bitsDisplay() once per layer update!!!

        
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
