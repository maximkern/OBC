# ///////////////////////////////////////////////////////////////// #
# DONE step 1: run a process
# DONE step 2: run a process with real-time print updates
# DONE step 3: accomplish this with two or more programs
# step 4: kill a program mid-run
# ///////////////////////////////////////////////////////////////// #



# IMPORTS
import multiprocessing
import subprocess
import queue


# VARIABLES
processes = [ # insert relative paths to these files
"OBC/scheduling/testing/process1.py",
"OBC/scheduling/testing/process2.py",
"OBC/scheduling/testing/process3.py",
]


# RUN SCRIPT FUNCTION
def run_script(script_name, output_queue, stop_event):
    # to run the script, we need an interpreter, the python interpreter is located at the file "/usr/bin/python3"
    # PIPE = make a standard pipe, which allows for standard communication across channels, in this case the I/O channel 

    process = subprocess.Popen(["/usr/bin/python3", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_queue.put(output.strip())


# MAIN FUNCTION
if __name__ == "__main__":

    # setup printing to console
    output_queue = multiprocessing.Queue()

    # setup needing to stop a process
    stop_event1 = multiprocessing.Event()
    stop_event2 = multiprocessing.Event()
    stop_event3 = multiprocessing.Event()

    # make a process for each piece of work to do
    script1_process = multiprocessing.Process(target=run_script, args=(processes[0], output_queue, stop_event1))
    script1_process.start()
    script2_process = multiprocessing.Process(target=run_script, args=(processes[1], output_queue, stop_event2))
    script2_process.start()
    script3_process = multiprocessing.Process(target=run_script, args=(processes[2], output_queue, stop_event3))
    script3_process.start()

    # dynamically output data or print statements from each process
    try:
        while script1_process.is_alive() or script2_process.is_alive() or script3_process.is_alive():
            try:
                output = output_queue.get_nowait()
                print(output)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping specific processes.")
        stop_event1.set()