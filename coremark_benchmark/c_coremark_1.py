import os
import sys
import subprocess


f = open("results-coremark1","w")
f.write("Coremark1\n")
f.close()

i = 0
while i<2:
    i += 1
    proc = subprocess.Popen(['./coremark_1.exe'],stdout=subprocess.PIPE)
    f = open("results-coremark1","a+")
    f.write("###################################")
    while True:
        line = proc.stdout.readline()
        if line != '':
            f.write(line)
        else:
            break
    f.close()
