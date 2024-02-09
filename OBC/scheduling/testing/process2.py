import time
import random

while True:
    time.sleep(2)
    random_int = random.randint(1, 100)
    output = "Data: " + str(random_int)
    print(output, flush=True)