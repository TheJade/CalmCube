import RPi.GPIO as GPIO
import signal
import sys

button = 20

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Sets button pin to input and sets input to always true

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def state_Relay():
    GPIO.add_event_detect(button, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100) #bouncetime is in miliseconds

    #button_state = GPIO.input(button) # determines if button is pressed (False) or not (True)
    #if button_state == False: # if button is pressed the statements is true
    #    print('Button Pressed')
    #    sleep(0.2)

def button_pressed_callback(channel):
    print("Button Pressed!")

if __name__ == '__main__':
    setup()
    state_Relay()
    signal.signal(signal.SIGINT,signal_handler)
    signal.pause()