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
GEAR_NAME = 'C14'

# pinion and wheel material
MAT_PINION = 'STEEL'
MAT_WHEEL = 'STEEL'

# LUBRICANT ===================================================================
# lubricant


class lub:
    def __init__(self):
        self.miu = 30
        self.xl = 0.85


GLUB = lub()

# select element when is applied speed and torque (P - pinion, W - wheel)
element = 'P'

# torque Nm
torque = 200

# speed rpm
speed = 1000

# discretization of path of contact
size = 1000

# discretization of involute geometry
DISCRETIZATION = 100

# element order
MESH = True

ORDER = 1

NODEM = 21

# graphics
GRAPHICS = True

# GEAR SELECTION ==============================================================
GTYPE = GEAR_LIBRARY.GEAR(GEAR_NAME)

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
