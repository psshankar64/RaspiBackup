import  RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#prev_input = 0
while True:

    input_state = GPIO.input(17)
    if input_state == False:
        print('oye')
        time.sleep(0.2)
