import time
import random

# in time, we won't generate a random int, it'll be a function from the subsystem that we call

# Note: we should keep the battery voltage between 3.5 and 4.1 volts if possible to maximize the lifespan of our li-ions

while True:
    time.sleep(0.5) # Interval to run measurements on
    
    acc = random.randint(100, 200) # mV

    battery_percentage = 100 * (acc - 35000)/6000 # Not an ideal measurement as discharge curves are nonlinear, we should track current

    output = "[DATA_VX] [" + str(acc) + "]" # Battery percentage
    print(output, flush=True)
    
