import time     # commonly used for timing (obviously)
import spidev   #this is the module that will control the pins, below is the best documentation I found
                #   https://www.sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf  
#import functions   #could help organzie the program

# Enable SPI
spi = spidev.SpiDev(0, 0)   #this function creates an instance of the object spidev called spi (you can call it whatever you like). 
                            #   The first parameter is the spi pin group select.
                            #       Meaning, it will utilize all the pins (SPI0_MOSI, SPI0_MISO, SPI0_SCLK, SPI0_CE0_N) in the default spi group on the board
                            #       To have use the other set of pins I think we set the first parameter to 1
                            #       For the first version of the code we will only be utilizing the defualt spi pins on the GPIOs
                            #   The second parameter is the CE select (also known as slave select).
                            #       We use this for selecting what slave gets written to.
                            #       For our project we are just having a single line of slaves, so the default of CE0 works fine.
                            #       If wanted to add another slave we could simple declare another instance of the object (e.g. spi2 = spidev.SpiDev(0, 1))

spi.max_speed_hz = 20000  #this class attribute defines the max speed the data will be transfered to the device in hz.
                            #   For the raspberry pi don't set it any higher then 32 Mhz
                            #   There is a debate about permissible speed values, with some insisting
                            #   that the speed must be a power of 2, while others argue that it can be a
                            #   multiple of 2. Tests at least partially confirm that the latter is correct. It
                            #   was possible to set the speed at 3800 Hz, which appears to be a lower
                            #   limit, and at 4800 Hz. Neither of these values is a power of 2. 
"""
Notes:

Don't use time.sleep(), it causes the whole program to pause for that amount of time
    Instead for timing use if statements to not pause the program
Don't use long while/for statements, cuz they can slow down the main While True: loop, if thats slow then things get updated slower
    Instead, use interative if statments: 
    i.e. 
    if(i < 1000):
        #some code
        if ((1000 - i)) % 10 == 0:
            make 1
        else:
            make 0
        i++

"""
#global constants
start_time = time.time()    #gets the time in seconds since Jan 1st 1970.
function_pointer = 0
msg = [0b00_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000001] #114 bits 108 for columns, 6 for rows
                #all the shift registers' outputs will be controlled by these values.
                #the underscore doesn't make a differnece to the values, all it does it make the 114 bits more readable by human.
                #could seperate it so that it is per led (i.e. 0b000_000_000_000), might work better idk whatever you like


#Function declarations
def function_relay():
    #this function gets run every loop, it's purpose is to use the function_pointer value to run a certain function
    if (function_pointer == 1):
        display_msg()
    else:
        idle()
    
def idle():         #checks for user input, could run every 0.1 seconds or something to imporve checking efficientcy
    #checks if button is pressed
    pass #does nothing just need something for the function

def display_msg():  #when function_pointer == 1
    spi.writebytes(msg)
    function_pointer = 0




try:       #if an error occurs in the try then it will execute finally
    while True: #will loop forever
        function_relay()

finally:
    spi.close()     #properly shuts down the activated pins
    GPIO.cleanup()  #just incase any other pins were activated, might cause an error not sure just remove GPIO.cleanup() if it does