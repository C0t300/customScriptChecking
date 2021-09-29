import subprocess
import re
import sys
import copy

def formatin(i):
    s = ""
    for ii in i:
        s += "\t" + ii.replace("\n", " - ") + "\n"
    s = s[:-3]
    s += "\n"
    return s

def formatout(o):
    s = ""
    for l in o:
        buf = "\t"
        for d in l:
            buf += str(d) + " "
        s += buf + "\n"
    return s

inn = ["""3
3""",
"""25
1
"""]

out = [["6", "0"], ["26", "24"]]
outc = copy.deepcopy(out)

pythonScript = "example.py"

if len(inn) != len(out):
    print("Length of inn and out is not the same")
    sys.exit(1)

passed = True

index = 0

for i, checksc in zip(inn, out):
    checks = copy.deepcopy(checksc)
    index += 1
    proc = subprocess.run(["python3", pythonScript], text=True, input=i, capture_output=True)
    if proc.returncode != 0:
        fp = open("ERR.txt", "w")
        fp.write(proc.stderr)
        fp.close()
    retorno = proc.stdout.splitlines()
    retorno = list(filter(None, retorno))
    clone = checks.copy()
    length = len(checks)
    for linea in retorno:
        if any(i.isdigit() for i in linea):
            numbers = re.findall("\d+", linea)
            for n in numbers:
                if n in checks:
                    checks.remove(n)

    if len(checks) > 0:
        passed = False
        fp = open("bad" + str(index) + ".txt", "w")
        fp.write("checks should be: " + str(clone))
        fp.write("\n")
        fp.write("but checks is: " + str(checks))
        fp.close()

if passed:
    fp = open("testspassed.txt", "w")
    fp.write("All tests passed\n")
    fp.write("inputs: \n")
    fp.write(formatin(inn))
    fp.write("outputs: \n")
    fp.write(formatout(outc))
    fp.close()