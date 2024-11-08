# ///////////////////////////////////////////////////////////////// #
# SCHEDULER.PY
# ///////////////////////////////////////////////////////////////// #
# 
# ///////////////////////////////////////////////////////////////// #
# DONE step 1: run a process
# DONE step 2: run a process with real-time print updates
# DONE step 3: accomplish this with two or more programs
# DONE step 4: kill a program mid-run
# WORKING step 5: dynamically start up a process
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
import multiprocessing
import subprocess
import queue
import os
import re


# VARIABLES
# checkpoints for FSM
checkpoint = False
deployed_already = False

# processes
scheduling_dir = os.path.dirname(os.path.abspath(__file__))

data_processes = [ # insert relative paths to these files
    scheduling_dir + "/data_processes/data_battery.py",            # data process id = 1
    scheduling_dir + "/data_processes/data_imu.py",                # data process id = 2
    scheduling_dir + "/data_processes/data_star_tracker.py",       # data process id = 3
]
state_processes = [ # insert relative paths to these files
    scheduling_dir + "/state_processes/state_bootup.py",           # state process id = 100, index = 0
    scheduling_dir + "/state_processes/state_detumble.py",         # state process id = 101, index = 1
    scheduling_dir + "/state_processes/state_charge.py",           # state process id = 102, index = 2
    scheduling_dir + "/state_processes/state_antennas.py",         # state process id = 103, index = 3
    scheduling_dir + "/state_processes/state_comms.py",            # state process id = 104, index = 4
    scheduling_dir + "/state_processes/state_deploy.py",           # state process id = 105, index = 5
    scheduling_dir + "/state_processes/state_orient.py",           # state process id = 106, index = 6
]

# STATE PROCESS IDS
# start at 100 to allow for process ids 0-99 to be data processes
state_processes_ids = {"bootup"     : 100,
                       "detumble"   : 101,
                       "charge"     : 102,
                       "antennas"   : 103,
                       "comms"      : 104,
                       "deploy"     : 105,
                       "orient"     : 106}


# RUN A PROCESS
def run_script(script_name, output_queue, stop_event, process_id):
    # to run the script, we need an interpreter, the python interpreter is located at the file "/usr/bin/python3"
    # PIPE = make a standard pipe, which allows for standard communication across channels, in this case the I/O channel 
    process = subprocess.Popen(["/usr/bin/python3", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_queue.put((process_id, output.strip()))


# CREATE NEW STATE PROCESS 
def startup_state_process(process_id, dynamic_vars):
    dynamic_vars["stop_event" + str(process_id)] = multiprocessing.Event()
    dynamic_vars["process" + str(process_id)]  = multiprocessing.Process(target=run_script, args=(state_processes[process_id-100], output_queue, dynamic_vars["stop_event" + str(process_id)], process_id))
    dynamic_vars["process" + str(process_id)].start()
    processes.append(dynamic_vars["process" + str(process_id)])


# FUNCTION TO STOP PROCESS
def stop_state_process(process_id, dynamic_vars):
    stop_event = dynamic_vars.get("stop_event" + str(process_id))
    process = dynamic_vars.get("process" + str(process_id))
    
    if stop_event is not None:
        stop_event.set()  # Signal the process to stop if it checks for this event
        
    if process is not None:
        process.terminate()  # Forcefully terminate the process
        process.join()  # Wait for the process to terminate

def extract_data(output):
    data_value = re.search(r'\[([-+]?\d+)\]', output)
    if data_value:
        return data_value.group(1)
    
def extract_data_multiple(output):
    data_values = re.findall(r'\[([-+]?\d+(?:,\s*[-+]?\d+)*)\]', output)
    values_list = [int(num) for num in data_values[0].split(',')]
    return values_list

# MAIN FUNCTION
if __name__ == "__main__":

    # SETUP MULTIPROCESSING
    output_queue = multiprocessing.Queue()
    processes = []

    # FIRE THE "BOOTUP STATE PROCESS"
    stop_event100 = multiprocessing.Event()
    process100 = multiprocessing.Process(target=run_script, args=(state_processes[0], output_queue, stop_event100, 100))
    process100.start()
    processes.append(process100)


    # FIRE UP "DATA PROCESSES"
    dynamic_vars = {}
    for i in range(1, len(data_processes) + 1):
        dynamic_vars["stop_event" + str(i)] = multiprocessing.Event()
        dynamic_vars["process" + str(i)]  = multiprocessing.Process(target=run_script, args=(data_processes[i-1], output_queue, dynamic_vars["stop_event" + str(i)], i))
        dynamic_vars["process" + str(i)].start()
        processes.append(dynamic_vars["process" + str(i)])
    
    current_state = "bootup"

    while True:
        try:
            # OUTPUT PRINT STATEMENTS FROM PROCESSES
            process_id, output = output_queue.get_nowait()
            print(f"{output}")
            
            # OVERRIDE SWITCH
            # DATA_BP = battery percentage
            # regardless of the current state, these MUST be done
            if "DATA_BP" in output and int(output[11:-1].strip()) <= 20:
                current_state = "charge"
                startup_state_process(process_id + 1, dynamic_vars)
                continue


            # STARTUP => ...
            if "[STATE_BOOTUP] [Ended]" in output:
                # start up DETUMBLE
                current_state = "detumble"
                startup_state_process(101, dynamic_vars)


            # DETUMBLE => ...
            if current_state == "detumble":
                # if this line has data, extract it
                value = extract_data(output)
                # see if this threshold occurs: this will always have data
                if "DATA_IMU_AV" in output and int(value) <= 0: # TODO: fine-tune the threshold on lower and upper
                    current_state = "charge"
                    # stop DETUMBLE
                    stop_state_process(101, dynamic_vars)
                    print("\n[STATE_DETUMBLE] [Ended] \n", flush = True)
                    # start up CHARGE
                    startup_state_process(102, dynamic_vars)
                    continue


            # CHARGE => ...
            if current_state == "charge":
                # if this line has data, extract it
                value = extract_data(output)
                # TODO: change to 95, currently at 75 to allow for faster testing
                if "DATA_BATTERY_BP" in output and int(value) >= 75:
                    current_state = "antennas"
                    # stop CHARGE
                    stop_state_process(102, dynamic_vars)
                    print("\n[STATE_CHARGE] [Ended] \n", flush = True)
                    # start up ANTENNAS
                    startup_state_process(103, dynamic_vars)
                    continue


            # ANTENNAS => ...
            if current_state == "antennas":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 50:
                    checkpoint = True
                if checkpoint and "DATA_STARTRACKER_POS" in output:
                    values = extract_data_multiple(output)
                    if values[0] > 90 and values[1] > 90 and values[2] > 90:
                        checkpoint = False
                        current_state = "comms"
                        # stop ANTENNAS
                        stop_state_process(103, dynamic_vars)
                        print("\n[STATE_ANTENNAS] [Ended] \n", flush = True)
                        # start up COMMS
                        startup_state_process(104, dynamic_vars)
                        continue


            # COMMS => ...
            if current_state == "comms":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 50:
                    checkpoint = True
                # TODO: change threshold
                if checkpoint and "DATA_IMU_AV" in output and int(value) <= 1:
                    checkpoint = False
                    # stop COMMS
                    stop_state_process(104, dynamic_vars)
                    print("\n[STATE_COMMS] [Ended] \n", flush = True)
                    if not deployed_already:
                        # start up DEPLOY
                        deployed_already = True
                        current_state = "deploy"
                        startup_state_process(105, dynamic_vars)
                        continue
                    else:
                        # start up ORIENT
                        current_state = "orient"
                        startup_state_process(106, dynamic_vars)
                        continue
           

            # DEPLOY PAYLOAD => ...
            if current_state == "deploy":
                # if this line has data, extract it
                value = extract_data(output)
                if "DATA_BATTERY_BP" in output and int(value) >= 30:
                # TODO: wait until deploy is done
                    # stop DEPLOY
                    current_state = "orient"
                    stop_state_process(105, dynamic_vars)
                    print("\n[STATE_DEPLOY] [Ended] \n", flush = True)
                    # start up ORIENT
                    startup_state_process(106, dynamic_vars)
                    continue


            # ORIENT PAYLOAD => ...
            if current_state == "orient":
                if "DATA_STARTRACKER_POS" in output:
                    values = extract_data_multiple(output)
                    if values[0] > 90 and values[1] > 90 and values[2] > 90:
                        # TODO: wait until orient is done
                        # stop ORIENT
                        stop_state_process(106, dynamic_vars)
                        print("\n[STATE_ORIENT] [Ended] \n", flush = True)
                        # start up COMMS
                        current_state = "comms"
                        startup_state_process(104, dynamic_vars)
                        continue


            # DECIDE TO KILL
            # if process_id == 1:
            #   if "4" in output or "5" in output:
            #        print("Process 1 terminated, due to data output")
            #        processes[process_id].terminate()

        except queue.Empty:
            pass
    