import subprocess
import time
import psutil
import argparse
import sys


class Params:
    pass


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_kimera(kimera, fg_lib, dataset):
    p = subprocess.Popen("{} -p {}".format(kimera, dataset).split())
    time.sleep(3)
    current_process = psutil.Process()
    kimera_process_id = int(current_process.children(recursive=True)[1].pid)
    pids = [str(kimera_process_id)]
    print((Colors.OKGREEN + "{}" + Colors.ENDC).format(kimera_process_id))
    with open("stereoVioPids.txt", "w+") as file:
        subprocess.call(["pstree", "-p", str(kimera_process_id)], stdout=file)
    with open("stereoVioPids.txt", "r") as file:
        for line in file:
            pid = line[line.find("{stereoVIOEuroc}(") + len("{stereoVIOEuroc}("):-2]
            pids.append(pid)
    pids = ",".join(pids)
    print(pids)
    create_flame_graph(pids, fg_lib)
    p.wait()


def create_flame_graph(pids, fg_lib):
    perf = subprocess.Popen("perf record -F 99 -p {} -g -- sleep 30".format(pids).split())
    perf.wait()
    with open("out.perf", "w+") as file:
        subprocess.call("perf script".split(), stdout=file)
    with open("out.folded", "w+") as file:
        subprocess.call((fg_lib + "stackcollapse-perf.pl out.perf").split(), stdout=file)
    with open("kernel.svg", "w+") as file:
        subprocess.call((fg_lib + "flamegraph.pl out.folded").split(), stdout=file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating flage graph for Kimera-VIO.')
    parser.add_argument('-fg_path', type=str, nargs=1, metavar='FlameGraphRepoPath',
                        help='path to the flame graph repo.', required=True)
    parser.add_argument('-k_path', type=str, nargs=1, metavar='KimeraRepoPath',
                        help='path to the Kimera-VIO repo.', required=True)
    parser.add_argument('-dataset_path', type=str, nargs=1, metavar='EurocDatasetPath',
                        help='path to the Euroc dataset.', required=True)
    params = parser.parse_args(sys.argv[1:], namespace=Params)
    fg_lib = params.fg_path[0]
    if fg_lib[-1] != '/':
        fg_lib += "/"
    k_lib = params.k_path[0]
    dataset = params.dataset_path[0]
    run_kimera(k_lib, fg_lib, dataset)
