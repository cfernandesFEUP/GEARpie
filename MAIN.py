'''MIT License

Copyright (c) 2022 Carlos M.C.G. Fernandes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

# IMPORT LIBRARIES ============================================================
from CLASSES import (GEAR_LIBRARY, MATERIAL_LIBRARY, CALC_GEOMETRY,
                     RIGID_LOAD_SHARING, FORCES_SPEEDS, CONTACT,
                     INVOLUTE_GEOMETRY, MESH_GENERATOR, OUTPUT_PRINT,
                     PLOTTING)

# import matplotlib.pyplot as plt
# import numpy as np

import sys
# AVOID CREATION OF PYCACHE FOLDER ============================================
sys.dont_write_bytecode = True


# GEAR GEOMETRY, MATERIAL AND FINISHING =======================================
# name of gear on library (includes geometry and surface finishing)
print('-'*50)
print('{:^50s}'.format('GeaR-Software\tC. Fernandes, 2022'))
print('-'*50)
print('Gear geometries available:')
print('C14, H501, H701, H951')
print('To use a new geometry, type New')
GEAR_NAME = str(input('Input gear geometry: '))

# GEAR SELECTION ==============================================================
GTYPE = GEAR_LIBRARY.GEAR(GEAR_NAME)


# LUBRICANT ===================================================================
# lubricant


class lub:
    def __init__(self):
        self.miu = 30
        self.xl = 0.85


GLUB = lub()

# pinion and wheel material
print('Materials available:')
print('STEEL, ADI, POM, PA66, PEEK')
print('To use a new geometry, type New')
MAT_PINION = str(input('Pinion material (default: STEEL): ') or 'STEEL')
MAT_WHEEL = str(input('Wheel material (default: STEEL): ') or 'STEEL')

# select element where is applied speed and torque (P - pinion, W - wheel)
stringPW = 'Select (P - Pinion or W - Wheel) to apply torque and speeed: '
element = str(input(stringPW))

# torque Nm
torque = float(input('Torque / Nm: '))

# speed rpm
speed = float(input('Speed / rpm: '))

# discretization of path of contact
size = 1000

# discretization of involute geometry
DISCRETIZATION = 100

# graphics
ANSWER_GRAPHICS = str(input('Graphical output (Y/N): '))

if ANSWER_GRAPHICS == 'Y':
    GRAPHICS = True
else:
    GRAPHICS = False

# element order
ANSWER_MESH = str(input('FEM mesh generation (Y/N): '))

if ANSWER_MESH == 'Y':
    MESH = True
    NODEM = int(input('Number of nodes on meshing surface: '))
    ORDER = int(input('Element order (1/2): '))
else:
    MESH = False

# ASSIGN GEAR MATERIALS =======================================================
GMAT = MATERIAL_LIBRARY.MATERIAL(MAT_PINION, MAT_WHEEL)

# FZG LOAD STAGE CONDITIONS ===================================================
if torque is str:
    torque = torque

# GEAR GEOMETRY ACCORDING TO MAAG BOOK ========================================
GEO = CALC_GEOMETRY.MAAG(GTYPE)

# LINES OF CONTACT ASSUMING A RIGID LOAD SHARING (SPUR AND HELICAL) ===========
GPATH = RIGID_LOAD_SHARING.LINES(size, GEO)

# FORCES AND SPEEDS ===========================================================
GFS = FORCES_SPEEDS.OPERATION(element, torque, speed, GEO, GPATH)

# GEAR CONTACT QUANTITIES (PRESSURE, FILM THICKNESS, POWER LOSS) ==============
GCONTACT = CONTACT.HERTZ(GMAT, GLUB, GEO, GPATH, GFS)

# INVOLUTE PROFILE GEOMETRY ===================================================
Pprofile = INVOLUTE_GEOMETRY.LITVIN('P', GEO, DISCRETIZATION)
Wprofile = INVOLUTE_GEOMETRY.LITVIN('W', GEO, DISCRETIZATION)

# thF = np.arccos(GEO.rb1/GEO.ra1)
# thP = np.arccos(GEO.rb1/GEO.r1)
# Sinvol = GEO.rb1*(np.tan(thF)**2-np.tan(thP)**2)/2
# ce = 0.25
# eS = (-0.2*ce + 1.2)*GCONTACT.aH.min()
# NODEM = int(Sinvol/eS)

# INVOLUTE PROFILE GEOMETRY ===================================================
if MESH:
    MESH_GENERATOR.MESHING('P', GEAR_NAME, GEO, Pprofile, 3, ORDER, NODEM)
    MESH_GENERATOR.MESHING('W', GEAR_NAME, GEO, Wprofile, 4, ORDER, NODEM)

# OUTPUT PRINT ================================================================
OUTPUT_PRINT.PRINTING(GEAR_NAME, GTYPE, GMAT, GEO, GFS, GCONTACT)

# OUTPUT GRAPHICS =============================================================
if GRAPHICS:
    PLOTTING.GRAPHICS(GPATH, GFS, GCONTACT)

# x = GPATH.xd
# y = GPATH.bpos
# X, Y = np.meshgrid(x, y)
# Sr = GPATH.lsum.T
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.plot_surface(X, Y, Sr, cmap='jet', edgecolor='k')
# # ax.view_init(10, 15)
# plt.show()
