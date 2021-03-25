import RPi.GPIO as GPIO
from time import sleep

button = 20

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    while True:
        button_state = GPIO.input(button)
        if button_state == False:
            print('Button Pressed')
            sleep(0.2)

if __name__ == '__main__':
    setup()
    loop()