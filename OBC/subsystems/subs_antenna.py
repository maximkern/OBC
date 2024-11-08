# ///////////////////////////////////////////////////////////////// #
# SUBSYSTEM: ANTENNA
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
from subsystems import config
import Adafruit_BBIO.GPIO as GPIO


# CLASS AND METHODS
class subsystem_antenna:
    def __init__(self):
        GPIO.setup("P8_15", GPIO.OUT)
        pass

    # DATA FUNCTIONS

    # ACTION FUNCTIONS
    pass