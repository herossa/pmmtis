import RPi.GPIO as GPIO
import time
from threading import Thread

class MotionMonitor():
    def __init__(self, stopper, alert_callback, gpio_pin: int = 11, sleep_time: float = 0.1):
        Thread.__init__(self)
        self.sleep_time = sleep_time
        self.gpio_pin = gpio_pin
        self.stopper = stopper
        self.alert_callback = alert_callback
    
    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.IN)

    def run(self):
        while not self.stopper.is_set():
            res = GPIO.input(self.gpio_pin) 
            if res != 0 :
                self.alert_callback()
            time.sleep(self.sleep_time)
