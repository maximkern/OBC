# IMPORTS
import time
import random


# SETUP CONNECTIONS
# ...


while True:
    time.sleep(1) # Interval to run measurements on


    # DATA: battery percentage
    # we should keep the battery voltage between 3.5 and 4.1 volts if possible to maximize the lifespan of our li-ions
    # units: mV
    # output: [DATA_BATTERY_BP]
    v_bat = random.randint(35000, 41000)
    battery_percentage = 100 * (v_bat - 35000)/6000 # Not an ideal measurement as discharge curves are nonlinear, we should track current
    output = "[DATA_BATTERY_BP] [" + str(v_bat) + "]" # Battery percentage
    print(output, flush=True)


    # DATA: ...
    # description/notes
    # units
    # output: [DATA_BATTERY_...]

    
    # DATA: ...
    # description/notes
    # units
    # output: [DATA_BATTERY_...]

    