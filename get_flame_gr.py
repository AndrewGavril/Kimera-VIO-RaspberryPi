import subprocess
import time
import psutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

path_to_lib = "../dependences/FlameGraph/"
if path_to_lib[-1] != '/':
    path_to_lib += "/"

p = subprocess.Popen("./scripts/stereoVIOEuroc.bash -p /home/andrew/work/kimera_project/V1_01_easy".split())
time.sleep(1)
current_process = psutil.Process()
kimera_process_id = int(current_process.children(recursive=True)[1].pid)
pids = [str(kimera_process_id)]
print((bcolors.OKGREEN + "{}" + bcolors.ENDC).format(kimera_process_id))

with open("stereoVioPids.txt", "w+") as file:
    pstree = subprocess.call(["pstree", "-p", str(kimera_process_id)], stdout=file)

with open("stereoVioPids.txt", "r") as file:
    for line in file:
        pid = line[line.find("{stereoVIOEuroc}(") + len("{stereoVIOEuroc}("):-2]
        pids.append(pid)

pids = ",".join(pids)
print(pids)

perf = subprocess.Popen("perf record -F 99 -p {} -g -- sleep 15".format(pids).split())
perf.wait()
p.wait()

with open("out.perf", "w+") as file:
    p = subprocess.call("perf script".split(), stdout=file)
with open("out.folded", "w+") as file:
    p = subprocess.call((path_to_lib + "stackcollapse-perf.pl out.perf").split(), stdout=file)
with open("kernel.svg", "w+") as file:
    p = subprocess.call((path_to_lib + "flamegraph.pl out.folded").split(), stdout=file)
