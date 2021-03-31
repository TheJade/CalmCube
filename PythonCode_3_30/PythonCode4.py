
#----------------LIBRARY------------------------------------------

import time # commonly used for timing (obviously)
import spidev   #ignore the error on this line, make sure this import is last
                    #this is the module that will control the pins, below is the best documentation I found
                    #   https://www.sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf  
                    
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

try:       #if an error occurs in the try then it will execute finally
    while True: #will loop forever
        spi.writebytes([0b00000000]) #
        spi.writebytes([0b11111110]) #
        spi.writebytes([0b01000011]) # first 3 columns should have white and Row 2 is the only one on

finally:

    spi.close()     #properly shuts down the activated pins