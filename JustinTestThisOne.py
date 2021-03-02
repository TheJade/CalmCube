import spidev
import time

spi = spidev.SpiDev(0, 0) # create spi object connecting to /dev/spidev0.1
spi.max_speed_hz = 10000 # set speed to 10 Khz
timestart = time.time()
print("Program Start")

try:
    while True: # endless loop, press Ctrl+C to exit
        if ((1 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b10_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 1 worked, red1")
        if ((2 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b01_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 2 worked, green1")
        if ((3 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b00_10000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 3 worked, blue1")
        if ((4 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b00_01110000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 4 worked, white2")
        if ((5 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b00_00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 5 worked, red2")
        if ((6 - (time.time() - timestart)) == 0 ):
            spi.writebytes([0b00_10010010_01001001_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000]) # write one byte
            print("if 6 worked, all on blue")
        if ((10 - (time.time() - timestart)) == 0 ):
            timestart = time.time()
            print("restart")

        
finally:
    spi.close() # always close the port before exit