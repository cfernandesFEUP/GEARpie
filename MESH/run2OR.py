import os

## REMOVE LINES
linelist = open("PC14.inp").readlines()
newfile = open('meshP.inp', 'w')
flag = 1

for line in linelist:
    if line.startswith("*ELEMENT, type=T3D3"):
        flag = 0
    if line.startswith("*ELEMENT, type=C3D20"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
       newfile.writelines(line)

## REMOVE LINES
linelist = open("WC14.inp").readlines()
newfile = open('meshW.inp', 'w')
flag = 1

for line in linelist:
    if line.startswith("*ELEMENT, type=T3D3"):
        flag = 0
    if line.startswith("*ELEMENT, type=C3D20"):
        flag = 1
    if flag and not line.startswith("EndModuleData"):
       newfile.writelines(line)

## RUN CalculiX CGX
os.system("cgx -b preP.fbd")
os.system("cgx -b preW.fbd")
