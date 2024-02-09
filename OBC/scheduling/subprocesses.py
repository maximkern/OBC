# ///////////////////////////////////////////////////////////////// #
# DONE step 1: run a process
# DONE step 2: run a process with real-time print updates
# DONE step 3: accomplish this with two or more programs
# DONE step 4: kill a program mid-run
# ///////////////////////////////////////////////////////////////// #



# IMPORTS
import multiprocessing
import subprocess
import queue


# VARIABLES
process_scripts = [ # insert relative paths to these files
"OBC/scheduling/testing/process0.py",
"OBC/scheduling/testing/process1.py",
"OBC/scheduling/testing/process2.py",
]


# RUN SCRIPT FUNCTION
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


# MAIN FUNCTION
if __name__ == "__main__":

    # setup printing to console
    output_queue = multiprocessing.Queue()

    stop_event1 = multiprocessing.Event()
    stop_event2 = multiprocessing.Event()

    # make a process for each piece of work to do
    processes = []
    process0 = multiprocessing.Process(target=run_script, args=(process_scripts[0], output_queue, stop_event1, 0))
    process0.start()
    processes.append(process0)
    process1 = multiprocessing.Process(target=run_script, args=(process_scripts[1], output_queue, stop_event2, 1))
    process1.start()
    processes.append(process1)

    # dynamically output data or print statements from each process
    try:
        while True:
            try:
                process_id, output = output_queue.get_nowait()
                print(f"Process {process_id} ", output)

                # determine whether to kill the process
                if process_id == 1:
                    if "4" in output or "5" in output:
                        print("Process 1 terminated, due to data output")
                        processes[process_id].terminate()
                
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping specific processes.")