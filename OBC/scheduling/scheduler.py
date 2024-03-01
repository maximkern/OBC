# ///////////////////////////////////////////////////////////////// #
# DONE step 1: run a process
# DONE step 2: run a process with real-time print updates
# DONE step 3: accomplish this with two or more programs
# DONE step 4: kill a program mid-run
# step 5: dynamically start up a process
# ///////////////////////////////////////////////////////////////// #


# IMPORTS
import multiprocessing
import subprocess
import queue
from OBC import helpers

# VARIABLES
root_dir = helpers.get_abs_path()
data_processes = [ # insert relative paths to these files
    root_dir + "/scheduling/data_processes/battery_percentage.py",     
    root_dir + "/scheduling/data_processes/imu_angularvelocity.py",     
    root_dir + "/scheduling/data_processes/imu_velocity.py",
]
state_processes = [ # insert relative paths to these files
    root_dir + "/scheduling/state_processes/state_bootup.py",           # state process id = 100, index = 0
    root_dir + "/scheduling/state_processes/state_detumble.py",         # state process id = 101, index = 1
    root_dir + "/scheduling/state_processes/state_charge.py",           # state process id = 102, index = 2
]


# STATE PROCESS IDS
# start at 100 to allow for process ids 0-99 to be data processes
state_processes_ids = {"bootup" : 100,
                       "detumble" : 101,
                       "charge" : 102}


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


# MAIN FUNCTION
if __name__ == "__main__":

    print("in main")

    # SETUP MULTIPROCESSING
    output_queue = multiprocessing.Queue()
    processes = []
    print("setup multiprocessing")


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

    while True:
        try:
            # OUTPUT PRINT STATEMENTS FROM PROCESSES
            process_id, output = output_queue.get_nowait()
            print(f"Process {process_id}: {output}")


            # OVERRIDE SWITCH
            # to be implemented


            # SEQUENTIAL SWITCH
            if "State Complete" in output:
                startup_state_process(process_id + 1, dynamic_vars)

            
            # DECIDE TO KILL
            if process_id == 1:
                if "4" in output or "5" in output:
                    print("Process 1 terminated, due to data output")
                    processes[process_id].terminate()

        except queue.Empty:
            pass
    