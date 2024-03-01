import time


def __init__():
    # initialize parameters
    time.sleep(0.1) 


def on_loop(repeat):
    # do some task for ... seconds
    for _ in range(repeat):
        print("Charging...", flush = True)
    time.sleep(2) 



time.sleep(2)
print("State Complete", flush = True)
