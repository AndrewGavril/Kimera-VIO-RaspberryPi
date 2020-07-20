import subprocess
import time


path_to_lib = "../dependences/FlameGraph/"
if path_to_lib[-1] != '/':
    path_to_lib += "/"

p = subprocess.Popen(["./scripts/stereoVIOEuroc.bash", "-p", "/home/andrew/work/kimera_project/V1_01_easy"])
pid = p.pid
time.sleep(0.5)
perf = subprocess.call(["perf", "record", "-F", "99", "-a", "-g", "--", "sleep", "30"])
p.wait()

with open("out.perf", "w") as file:
    print("a")
    p = subprocess.call("perf script".split(), stdout=file)
with open("out.folded", "w") as file:
    p = subprocess.call((path_to_lib + "stackcollapse-perf.pl out.perf").split(), stdout=file)
with open("kernel.svg", "w") as file:
    p = subprocess.call((path_to_lib + "flamegraph.pl out.folded").split(), stdout=file)
