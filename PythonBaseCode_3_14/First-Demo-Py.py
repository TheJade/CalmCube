
test = True #make true if wanting to print instead of run the code

#----------------LIBRARY------------------------------------------

try:
    import time # commonly used for timing (obviously)
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

#----------------GLOBAL---VARIBLES----------------------------------
#don't add anything here, unless important to all states and function
statePointer = 0
msg = [False for i in range(120)] #114 bits 108 for columns, 6 for rows

#----------------SETUP----------------------------------------------
#will run once at the beginning of the program and never again
    #the setup code goes here
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
    spi.max_speed_hz = 2000000  #this class attribute defines the max speed the data will be transfered to the device in hz
                            #   For the raspberry pi don't set it any higher then 32 Mhz
                            #   There is a debate about permissible speed values, with some insisting
                            #   that the speed must be a power of 2, while others argue that it can be a
                            #   multiple of 2. Tests at least partially confirm that the latter is correct. It
                            #   was possible to set the speed at 3800 Hz, which appears to be a lower
                            #   limit, and at 4800 Hz. Neither of these values is a power of 2. 

#-------------------STATE----RELAY-----------------------------------
#uses the function pointer to
def stateRelay():
    if statePointer == SNAKE_EFFECT:
        snakeDisplay()
    elif statePointer == SLOW_DEMO:
        stateSlowDemo()
    elif statePointer == RAIN_EFFECT:
        rainEffect()
    else:
        idle()
#-------------------STATE----FUNCTIONS-------------------------------
#will stay in each of these states an a pattern or main function is runnin
def idle():
    #maybe somehow enter low power mode or something
    bitsDisplay()
    time.sleep(3)

def snakeDisplay():
    pass

def stateSlowDemo():
    pass

def rainEffect():
    pass


#-------------------COMMON---FUNCTIONS-------------------------------
# functions often used by the different state functions

def bitsDisplay():  #NEEDS TO BE TESTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #less then one layer testing
    more_than_one_level = 0
    for i in range(6):
        more_than_one_level += msg[i]
    if more_than_one_level > 1:
        print("Multiple layers active, ignoring for testing mode")
        if not test:
            raise Exception("More then one layer is on at a time")
    #spi.writebytes
    if not test:    #seems like there should be a more efficient way of doing this
        for i in range(15):
            byte = 0
            for j in range(8):
                if msg[8*(14-i) + j]:   #(14-i) might have to become just i
                    byte += 2**(7-j)    #for MSB
            spi.writebytes(byte)
    #testing output print           
    else:   #modify the below for test formatting
        print("Level:", list(map(int, msg[0:6])))
        for i in range(36):
            print(list(map(int, msg[(6 + i*3):(9 + 3*i)])), end = '  ')
            if i % 6 == 5:
                print("\n")
    

#------------------MAIN------LOOP-----------------------------------
#don't modify, will loop continuously. This needs to be at the end of the program
#   we could make a file containing all the state funciton and common functions to make it a little more elegant

try:       #if an error occurs in the try then it will execute finally
    while True: #will loop forever
        stateRelay()

finally:
    if not test:    #we might want to remove this conditional statement
        spi.close()     #properly shuts down the activated pins
        GPIO.cleanup()  #just incase any other pins were activated, might cause an error not sure just remove GPIO.cleanup() if it does