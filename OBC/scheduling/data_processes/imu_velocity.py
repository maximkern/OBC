import time
import random

# in time, we won't generate a random int, it'll be a function from the subsystem that we call

while True:
    time.sleep(2)
    random_int = random.randint(1, 100)
    output = "[DATA_VE] [Data: " + str(random_int) + "]"
    print(output, flush=True)