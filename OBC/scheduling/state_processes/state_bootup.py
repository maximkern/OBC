import time


def __init__():
    # initialize parameters
    time.sleep(0.1) 


def on_loop():
    # do some task for ... seconds
    print("Task In-Progress")
    time.sleep(5) 


__init__()
on_loop()
print("Bootup Complete")
