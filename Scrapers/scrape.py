import argparse
import sys
import re

argparser = argparse.ArgumentParser()
argparser.add_argument("file_num", type=int)
argparser.add_argument("--mode", "-m", type=str, default="max_flow", choices=["max_flow", "min_path"])
args = argparser.parse_args(sys.argv[1:])

file_num = args.file_num

with open("{0}.dat".format(file_num), 'r') as data:
    lines = data.readlines()

    incidence_matrix = []
    for line in lines[4:]:
        if line.strip() == "":
            break
        incidence_matrix.append([int(d) for d in re.findall(r"-?[01]", line)])

    # assert all([len(arr) == m for arr in incidence_matrix])

    capacities = [int(b) for b in re.findall("\d", lines[-3])]
    costs = [int(c) for c in re.findall("\d", lines[-2])]


n = len(incidence_matrix)
m = len(incidence_matrix[0])

links = []
for link in [[node[i] for node in incidence_matrix] for i in range(m)]:
    origin, end = -1, -1
    for i, num in enumerate(link):
        if num == 1:
            origin = i
        elif num == -1:
            end = i

    assert origin != -1 and end != -1
    links.append((origin, end))


with open("{0}_formatted.dat".format(file_num), 'w') as out:
    out.write("param n := {0};\n\n".format(n))

    out.write("set LINKS :=\n")
    for i, j in links:
        out.write("{0} {1}\n".format(i+1, j+1))
    out.write(';\n\n')

    if args.mode == "max_flow":
        out.write("param Capacities :=\n")
        for a, (i, j) in enumerate(links):
            out.write("{0} {1}\t\t{2}\n".format(i+1, j+1, capacities[a]))
        out.write(';\n\n')
    elif args.mode == "min_path":
        out.write("param Costs :=\n")
        for a, (i, j) in enumerate(links):
            out.write("{0} {1}\t\t{2}\n".format(i+1, j+1, costs[a]))
        out.write(';\n\n')
