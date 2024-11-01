# IMPORTS
import time
import random
from config import DATA_OUTPUT_PADDING

# SETUP CONNECTIONS
# ...



while True:
    time.sleep(1) # Interval to run measurements on


    # DATA: acceleration
    # dummy data for right now
    # units: km^2
    # output: [DATA_IMU_ACC]
    output_part1 = "[DATA_IMU_ACC]" # Battery percentage
    padding_length = DATA_OUTPUT_PADDING - len(output_part1)
    padding = " " * padding_length
    output_part1 = output_part1 + padding + "[" + str(100) + "]"

    # DATA: angular velocity
    # description/notes
    # units
    # output: [DATA_IMU_AV]
    
    output_part2 = "[DATA_IMU_AV]" # Battery percentage
    padding_length = DATA_OUTPUT_PADDING - len(output_part2)
    padding = " " * padding_length
    random_int = random.randint(-1,5)
    output_part2 = output_part2 + padding + "[" + str(random_int) + "]"
    
    
    # DATA: ...
    # description/notes
    # units
    # output: [DATA_BATTERY_...]

    output = output_part1 + "\n" + output_part2
    print(output, flush=True)