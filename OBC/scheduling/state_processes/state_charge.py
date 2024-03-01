# ///////////////////////////////////////////////////////////////// #
# CHARGING STATE
# ///////////////////////////////////////////////////////////////// #
import time


# FUNCTIONS
def __init__():
    print("Charging State Begin")
    on_loop(5)


def on_loop(repeat):
    for _ in range(repeat):
        # TO-DO: call the function inside the battery
        # ....

        print("Charging...", flush = True)
        time.sleep(1) 


# MAIN FUNCTION
__init__()
print("Charging State Complete", flush = True)
