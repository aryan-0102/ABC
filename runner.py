import subprocess
import time

from datetime import datetime
st = time.time()
def write_log(message, logfile='log.txt'):
    with open(logfile, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")


scripts = ["requirement.sh","heatmap.py","abc_all.py","iteration.py","abctest.py",
           "a_Star.py","dijkstra.py","comapre.py","comparision_time_graph.py","scheduling.py","del_time.py"]
Comments = ["Checking requirements......","Plotting Customer data .....","Running Artificial Bee Colony Algorithm......",
            "Plotting Graph.......","Generating routes.....","Checking new routes using A* Algorithm......",
            "Running Dijkstra Algorithm......","Comparing the results ......","Adding graph........","Optimising scheduling.....","Finishing up"]

def log_error(script_name, error_message):
    with open("error.txt", "a") as error_file:
        error_file.write(f"\n--- Errors from {script_name} ---\n")
        error_file.write(error_message)
        error_file.write("\n-------------------------------\n")
st  = time.time()
k = 0
error = 0
for i, j in zip(scripts, Comments):

    start_time = time.time()
    write_log(f"Starting {i}...")
    print(k+1,"of 11")
    k +=1
    print(j)
    if i == "abc_all.py":
        pass
        print()
        print("This might take a while...")
        print()

    else:
        result = subprocess.run(['python', i], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        print("Completed..",i)

    end_time = time.time()
    write_log(f"Finished {i}... in {end_time - start_time:.4f} seconds")

    if result.stderr:
        log_error(i, result.stderr)
        error += 1

print("Generating Final Report......")
result = subprocess.run(['python', "report.py"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
if result.stderr:
    log_error("report.py", result.stderr)
    error += 1
else:
    pass

if error == 0:
    print("Program ran successfully. Check logs at log.txt")
else:
    print("Something went wrong. Check log.txt")
