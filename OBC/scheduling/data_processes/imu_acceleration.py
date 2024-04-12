import time
import random
from ...subsystems.imu import IMU

# in time, we won't generate a random int, it'll be a function from the subsystem that we call

gyro = IMU()

while True:
    time.sleep(0.5)
    acc_x, acc_y, acc_z, vel_x, vel_y, vel_z = gyro.get_velocity()

    output = "[DATA_AX] [" + str(acc_x) + "]" + "[DATA_AY] [" + str(acc_y) + "]" + "[DATA_AZ] [" + str(acc_z) + "]"
    
    print(output, flush=True)