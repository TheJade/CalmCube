import spidev
import time

spi = spidev.SpiDev(0, 0) # create spi object connecting to /dev/spidev0.1
spi.max_speed_hz = 10000 # set speed to 10 Khz
timestart = time.time()
print("Program Start")
x = 0

try:
    while True: # endless loop, press Ctrl+C to exit
        if ((1.1 - (time.time() - timestart)) <= 0.1 ):
            x += 1
            timestart = time.time()
            if (x == 1):
                spi.writebytes([0b10000000]) # write one byte
                print("if 1 worked, red1")
            elif (x == 2):
                spi.writebytes([0b01000000]) # write one byte
                print("if 2 worked, green1")
            elif (x == 3):
                spi.writebytes([0b00100000]) # write one byte
                print("if 3 worked, blue1")
            elif (x == 4):
                spi.writebytes([0b00_01110]) # write one byte
                print("if 4 worked, white2")
            elif (x == 5):
                spi.writebytes([0b00_00001]) # write one byte
                print("if 5 worked, red2")
            elif (x == 6):

                spi.writebytes([0b01001001])
                spi.writebytes([0b10010010]) # write one byte
                spi.writebytes([0b00])
                print("if 6 worked, all on blue")
            elif (x == 7):
                x = 0
                print("restart")

        
finally:
    spi.close() # always close the port before exit