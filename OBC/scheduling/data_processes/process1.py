import time
import random


while True:
    time.sleep(1)
    random_int = random.randint(1, 5)
    output = "Data: " + str(random_int)
    print(output, flush=True)