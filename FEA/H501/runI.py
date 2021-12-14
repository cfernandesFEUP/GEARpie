import os
import multiprocessing

## REMOVE LINES
flag = 1
with open("../../MESH/PH501.inp") as infile, open('meshP.inp', "w") as outfile:
    for line in infile:
        if line.startswith("*Heading"):
            flag = 0
        if line.startswith("*NODE"):
            flag = 1
       	if line.startswith("*ELEMENT, type=CPS4"):
            flag = 0
       	if line.startswith("*ELEMENT, type=C3D8"):
            flag = 1
       	if flag and not line.startswith("EndModuleData"):
            outfile.writelines(line)

flag = 1
with open("../../MESH/WH501.inp") as infile, open('meshW.inp', "w") as outfile:
    for line in infile:
        if line.startswith("*Heading"):
            flag = 0
        if line.startswith("*NODE"):
            flag = 1
       	if line.startswith("*ELEMENT, type=CPS4"):
            flag = 0
       	if line.startswith("*ELEMENT, type=C3D8"):
            flag = 1
       	if flag and not line.startswith("EndModuleData"):
            outfile.writelines(line)

## REPLACE ELEMENT TYPE
with open("meshP.inp") as infile:
    filedata = infile.read()
newfile = filedata.replace('C3D8', 'C3D8I')
with open("meshP.inp", 'w') as outfile:    
    outfile.write(newfile)
    
with open("meshW.inp") as infile:
    filedata = infile.read()
newfile = filedata.replace('C3D8', 'C3D8I')
with open("meshW.inp", 'w') as outfile:    
    outfile.write(newfile)

## RUN CalculiX CGX
os.system("cgx -b preP.fbd")
os.system("cgx -b preW.fbd")

## RUN CalculiX CCX
os.environ['OMP_NUM_THREADS'] = str(multiprocessing.cpu_count())
os.system("ccxR CONT")

## CONVERT FILE
os.system("ccx2paraview CONT.frd vtu")
