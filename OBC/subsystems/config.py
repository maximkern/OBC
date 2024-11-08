# ///////////////////////////////////////////////////////////////// #
# SUBSYSTEM: CONFIG
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
import Adafruit_BBIO.GPIO as GPIO


# SUBSYSTEM => PIN INPUT/OUTPUT
subsystem_imu_in                = GPIO.setup("P8_7", GPIO.IN)
subsystem_imu_out               = GPIO.setup("P8_8", GPIO.OUT)
subsystem_reaction_wheel_in     = GPIO.setup("P8_9", GPIO.IN)
subsystem_reaction_wheel_out    = GPIO.setup("P8_10", GPIO.OUT)
subsystem_magnetorquer_in       = GPIO.setup("P8_11", GPIO.IN)
subsystem_magnetorquer_out      = GPIO.setup("P8_12", GPIO.OUT)
subsystem_sun_sensor_in         = GPIO.setup("P8_14", GPIO.IN)
subsystem_star_tracker_in       = GPIO.setup("P8_15", GPIO.IN)
subsystem_battery_in            = GPIO.setup("P8_16", GPIO.IN)
subsystem_nithinol_in           = GPIO.setup("P8_17", GPIO.IN)
subsystem_nithinol_out          = GPIO.setup("P8_18", GPIO.OUT)
subsystem_camera_in             = GPIO.setup("P9_23", GPIO.IN)
subsystem_camera_out            = GPIO.setup("P9_24", GPIO.OUT)
subsystem_antenna_in            = GPIO.setup("P9_25", GPIO.IN)
subsystem_antenna_out           = GPIO.setup("P9_26", GPIO.OUT)