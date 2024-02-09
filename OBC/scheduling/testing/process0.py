import time
import random

while True:
    time.sleep(0.25)
    random_int = random.randint(1, 25)
    output = "Data: " + str(random_int)
    print(output, flush=True)