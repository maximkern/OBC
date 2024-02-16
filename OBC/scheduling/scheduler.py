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


# VARIABLES
data_processes = [ # insert relative paths to these files
    "OBC/scheduling/data_processes/battery_percentage.py",
    "OBC/scheduling/data_processes/imu_angularvelocity.py",
    "OBC/scheduling/data_processes/imu_velocity.py",
]
state_processes = [ # insert relative paths to these files
    "OBC/scheduling/state_processes/state_bootup.py",
    "OBC/scheduling/state_processes/state_detumble.py",
    "OBC/scheduling/state_processes/state_charge.py",
]


# RUN SCRIPT
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


# CREATE NEW PROCESS 
def startup_process():
    print("not yet implemented")


# MAIN FUNCTION
if __name__ == "__main__":

    # SETUP MULTIPROCESSING
    output_queue = multiprocessing.Queue()
    processes = []


    # FIRE THE "BOOTUP STATE PROCESS"
    stop_event0 = multiprocessing.Event()
    process0 = multiprocessing.Process(target=run_script, args=(state_processes[0], output_queue, stop_event0, 0))
    process0.start()
    processes.append(process0)


    # FIRE UP "DATA PROCESSES"
    dynamic_vars = {}
    for i in range(1, len(data_processes)):
        dynamic_vars["stop_event" + str(i)] = multiprocessing.Event()
        dynamic_vars["process" + str(i)]  = multiprocessing.Process(target=run_script, args=(data_processes[1], output_queue, dynamic_vars["stop_event" + str(i)], i))
        dynamic_vars["process" + str(i)].start()
        processes.append(dynamic_vars["process" + str(i)])


    # OUTPUT PRINT STATEMENTS FROM PROCESSES
    try:
        while True:
            try:
                process_id, output = output_queue.get_nowait()
                print(f"Process {process_id}: {output}")

                # determine whether to kill the process
                if process_id == 1:
                    if "4" in output or "5" in output:
                        print("Process 1 terminated, due to data output")
                        processes[process_id].terminate()
                
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping specific processes.")