import time
import random

# in time, we won't generate a random int, it'll be a function from the subsystem that we call

# Note: we should keep the battery voltage between 3.5 and 4.1 volts if possible to maximize the lifespan of our li-ions

while True:
    time.sleep(1) # Interval to run measurements on
    
    v_bat = random.randint(35000, 41000) # mV

    battery_percentage = 100 * (v_bat - 35000)/6000 # Not an ideal measurement as discharge curves are nonlinear, we should track current

    output = "[DATA_BP] [" + str(random_int) + "]" # Battery percentage
    print(output, flush=True)
    
