import time
from RPi import GPIO
GPIO.setwarnings(False)

PIN = 2
#BUZZER_REPETITIONS = 2000
BUZZER_DELAY = 0.001
PAUSE_TIME = 0.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

while True:
    #for i in range(BUZZER_REPETITIONS):
    for value in [True, False]:
        GPIO.output(PIN, value)
        time.sleep(BUZZER_DELAY)
time.sleep(PAUSE_TIME)
