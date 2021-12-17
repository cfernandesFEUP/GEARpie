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

# AVOID CREATION OF PYCACHE FOLDER ============================================
import sys
sys.dont_write_bytecode = True

# IMPORT LIBRARIES ============================================================


from CLASSES import (GEAR_LIBRARY, MATERIAL_LIBRARY, CALC_GEOMETRY,
                     RIGID_LOAD_SHARING, FORCES_SPEEDS, CONTACT,
                     INVOLUTE_GEOMETRY, MESH_GENERATOR, OUTPUT_PRINT,
                     PLOTTING)

# GEAR GEOMETRY, MATERIAL AND FINISHING =======================================
# name of gear on library (includes geometry and surface finishing)
print('='*65)
print('{:^65s}'.format('GEARpie'))
print('.'*65)
print('{:^65s}'.format('MIT License, Carlos M.C.G. Fernandes, 2022'))
print('='*65)
print('\n')
print('Gear geometries available:')
print('C14, H501, H701, H951')
print('To use a new geometry, type NEW')
GEAR_NAME = str(input('Input gear geometry: ')).upper()

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
print('\nMaterials available:\n')
print('STEEL, ADI, POM, PA66, PEEK')
MAT_PINION = str(input('Pinion material (default: STEEL): ')
                 or 'STEEL').upper()
MAT_WHEEL = str(input('Wheel material (default: STEEL): ') or 'STEEL').upper()

# select element where is applied speed and torque (P - pinion, W - wheel)
stringPW = 'Select (P - Pinion or W - Wheel) to apply torque and speeed: '
element = str(input(stringPW)).upper()

# torque Nm
torque = float(input('Torque / Nm: '))

# speed rpm
speed = float(input('Speed / rpm: '))

# discretization of path of contact
size = 1000

# discretization of involute geometry
DISCRETIZATION = 100


# stress field position
POST = str(input('Stress field position along AE (A, B, C, D or E): ')).upper()
POSAE = 'A' + POST

# graphics
ANSWER_GRAPHICS = str(input('Graphical output (Y/N): ')).upper()

if ANSWER_GRAPHICS == 'Y':
    GRAPHICS = True
else:
    GRAPHICS = False

# element order
ANSWER_MESH = str(input('FEM mesh generation (Y/N): ')).upper()

if ANSWER_MESH == 'Y':
    MESH = True
    NODEM = int(
        input('Nº of nodes on meshing surface (tipically 11<n<41): '))
    ORDER = int(input('Element order (1/2): '))
    PTOOTH = int(input('Number of tooth for pinion mesh: '))
    WTOOTH = int(input('Number of tooth for wheel mesh: '))
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
GCONTACT = CONTACT.HERTZ(GMAT, GLUB, GEO, GPATH, GFS, POSAE)

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
    MESH_GENERATOR.MESHING('P', GEAR_NAME, GEO, Pprofile, PTOOTH, ORDER, NODEM)
    MESH_GENERATOR.MESHING('W', GEAR_NAME, GEO, Wprofile, WTOOTH, ORDER, NODEM)

# OUTPUT PRINT ================================================================
OUTPUT_PRINT.PRINTING(GEAR_NAME, GTYPE, GMAT, GEO, GFS, GCONTACT)

# OUTPUT GRAPHICS =============================================================
if GRAPHICS:
    PLOTTING.GRAPHICS(GPATH, GFS, GCONTACT)

# CLOSE PROGRAM ===============================================================
input("Press enter to exit")
# x = GPATH.xd
# y = GPATH.bpos
# X, Y = np.meshgrid(x, y)
# Sr = GPATH.lsum.T
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.plot_surface(X, Y, Sr, cmap='jet', edgecolor='k')
# # ax.view_init(10, 15)
# plt.show()
