import time


def __init__():
    # initialize parameters
    time.sleep(0.1) 


def on_loop():
    # do some task for ... seconds
    print("Task In-Progress")
    time.sleep(2) 


__init__()
while True:
    on_loop()
    time.sleep(0.1)