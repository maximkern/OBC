# ///////////////////////////////////////////////////////////////// #
# step 1: run a process (done)
# step 2: run a process with real-time print updates (done)
# step 3: accomplish this with two or more programs (done)
# step 4: kill a program mid-run (NOT YET DONE)
# ///////////////////////////////////////////////////////////////// #



# IMPORTS
import threading
import subprocess
import queue


# VARIABLES
processes = [ # give relative paths to this file
"OBC/scheduling/testing/process1.py",
"OBC/scheduling/testing/process2.py",
"OBC/scheduling/testing/process3.py",
]


# RUN SCRIPT FUNCTION
def run_script(script_name, output_queue, stop_event):
    # open the process using "Popen" because it allows you to output things dynamically/in real-time 
    process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while not stop_event.is_set():
        output = process.stdout.readline()
        if output == '' and process.poll() is not None: break
        if output: output_queue.put(output.strip())


# MAIN FUNCTION
if __name__ == "__main__":
    # setup printing to console
    output_queue = queue.Queue()

    # setup needing to stop a thread
    stop_event1 = threading.Event()
    stop_event2 = threading.Event()
    stop_event3 = threading.Event()

    # make a thread for each piece of work to do
    script1_thread = threading.Thread(target=run_script, args=(processes[0], output_queue, stop_event1))
    script1_thread.start()
    script2_thread = threading.Thread(target=run_script, args=(processes[1], output_queue, stop_event2))
    script2_thread.start()
    script3_thread = threading.Thread(target=run_script, args=(processes[2], output_queue, stop_event3))
    script3_thread.start()

    # dynamically output data or print statements from each thread
    try: 
        while script1_thread.is_alive() or script2_thread.is_alive() or script3_thread.is_alive():
            try:
                output = output_queue.get_nowait()
                print(output)
            except queue.Empty: 
                pass
    except KeyboardInterrupt:
        print("Keyboard interrupt. Stopping specific threads.")
        stop_event1.set()  

    