import RPi.GPIO as GPIO
import time
from threading import Thread

class MotionMonitor(Thread):
    def __init__(self, stopper, alert_callback, gpio_pin: int = 17, sleep_time: float = 0.1):
        Thread.__init__(self)
        self.gpio_pin = gpio_pin
        self.sleep_time = sleep_time
        self.stopper = stopper
        self.alert_callback = alert_callback
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN)

    def run(self):
        image_send = 0
        while not self.stopper.is_set():
            res = GPIO.input(self.gpio_pin)
            if res != 0 and image_send == 0:
                self.alert_callback(None)
                image_send = 1
            if res == 0:
                image_send = 0
            time.sleep(self.sleep_time)
