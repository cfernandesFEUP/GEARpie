import os

## REMOVE LINES
linelist = open("PC14.inp").readlines()
newfile = open('meshP.inp', 'w')
flag = 1
for line in linelist:
    if line.startswith("*ELEMENT, type=CPS4"):
        flag = 0
    if line.startswith("*ELEMENT, type=C3D8"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
       newfile.writelines(line)

linelist = open("meshP.inp").readlines()
newfile = open('meshP.inp', 'w')
flag=1
for line in linelist:
    if line.startswith("*Heading"):
        flag = 0
    if line.startswith("*NODE"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
        newfile.writelines(line)

## REMOVE LINES
linelist = open("WC14.inp").readlines()
newfile = open('meshW.inp', 'w')
flag = 1
for line in linelist:
    if line.startswith("*ELEMENT, type=CPS4"):
        flag = 0
    if line.startswith("*ELEMENT, type=C3D8"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
       newfile.writelines(line)

linelist = open("meshW.inp").readlines()
newfile = open('meshW.inp', 'w')
flag=1
for line in linelist:
    if line.startswith("*Heading"):
        flag = 0
    if line.startswith("*NODE"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
        newfile.writelines(line)

## RUN CalculiX CGX
os.system("cgx -b preP.fbd")
os.system("cgx -b preW.fbd")
