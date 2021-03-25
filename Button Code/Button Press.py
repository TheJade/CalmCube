import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

button_Pin = 20
GPIO.setup(button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print 'Button Is Pressed'
    sleep(2)