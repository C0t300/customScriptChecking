import subprocess
import re
import sys
import copy
from pathlib import Path
import os

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

clear = input("Clean all txt files? (This will erase all .txt files that contain bad or ERR o passed in this folder) [y/N]: ")
deletes = ["bad", "testspassed", "ERR"]
if clear.upper() == "Y":
    cwd = Path.cwd()
    for p in cwd.iterdir():
        if p.is_file():
            if p.suffix == ".txt" and any(x in p.name for x in deletes):
                p.unlink()
        elif p.is_dir():
            for pp in p.iterdir():
                if pp.is_file():
                    if pp.suffix == ".txt" and any(x in pp.name for x in deletes):
                        pp.unlink()

    keep = input(".txt deleted. Do you want to keep going with the checking? [Y/n]: ")
    if keep.upper() == "N":
        sys.exit()

inFolders = input("Do you want to check in folders? It only supports one folder deep. [y/N]: ")
if inFolders.upper() == "Y":
    inFolders = True
else:
    inFolders = False

#Change with inputs, should be strings with \n for different inputs
inn = ["""3
3""",
"""25
1
"""]

#Change with outputs, should be lists of lists for things you might wait from the program
out = [["6", "0"], ["26", "24"]]
outc = copy.deepcopy(out)

if not inFolders:
    pythonScript = input("Enter python script name: ")
    if pythonScript == "":
        pythonScript = "example.py"

if len(inn) != len(out):
    print("Length of inn and out is not the same")
    sys.exit(1)

if inFolders:
    cwd = Path.cwd()
    for p in cwd.iterdir():
        if p.is_dir():
            for pys in p.iterdir():
                if pys.suffix == ".py":
                    os.chdir(p)
                    pythonScript = pys
                    passed = True
                    index = 0

                    for i, checksc in zip(inn, out):
                        checks = copy.deepcopy(checksc)
                        index += 1
                        print(pys.name + " - " + str(index) + " of " + str(len(inn)))
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
                            fp.write("checks should be empty, check was: " + str(clone))
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
else:
    passed = True
    index = 0
    for i, checksc in zip(inn, out):
        checks = copy.deepcopy(checksc)
        index += 1
        print(str(index) + " of " + str(len(inn)))
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
            fp.write("checks should be empty, check was: " + str(clone))
            fp.write("\n")
            fp.write("but checks is: " + str(checks))
            fp.close()
        else:
            fp = open("test" + str(index) + ".txt", "w")
            fp.write("Output test " + str(index) + " passed. \n")
            fp.write(proc.stdout)
            fp.close()

    if passed:
        fp = open("testspassed.txt", "w")
        fp.write("All tests passed\n")
        fp.write("inputs: \n")
        fp.write(formatin(inn))
        fp.write("outputs: \n")
        fp.write(formatout(outc))
        fp.close()