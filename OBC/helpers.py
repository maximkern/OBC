########################################
# File containing helper functions
########################################
import os

def get_abs_path():
    root = os.path.dirname(os.path.abspath(__file__))
    return root

if __name__ == "__main__":
    get_abs_path()