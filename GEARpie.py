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
from CLASSES import (GEAR_LIBRARY, MATERIAL_LIBRARY, LUBRICANT_LIBRARY,
                     LOAD_STAGES, CALC_GEOMETRY, RIGID_LOAD_SHARING, 
                     FORCES_SPEEDS, CONTACT, INVOLUTE_GEOMETRY, DIN3990, 
                     VDI2736, MESH_GENERATOR, OUTPUT_PRINT, PLOTTING)

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
GEAR_TYPE = str(input('Input gear geometry: ')).upper()
# GEAR SELECTION ==============================================================
GTYPE = GEAR_LIBRARY.GEAR(GEAR_TYPE)
# GEAR MATERIALS ==============================================================
# pinion and wheel material
print('Materials available:')
print('STEEL, ADI, POM, PA66')
MAT_PINION = str(input('Pinion material (default: STEEL): ')
                 or 'STEEL').upper()
MAT_WHEEL = str(input('Wheel material (default: STEEL): ') or 'STEEL').upper()
# LUBRICANT ===================================================================
# lubricant
B_STR = 'Base Oil (M - mineral, P - PAO, E - ester, G - polyglicol, D - dry): '
BASE_NAME = str(input(B_STR)).upper()
if BASE_NAME == 'D':
    GLUB = None
    T0 = float(input('Ambient temperature / \u00b0C: '))
else:
    LUB_NAME = str(input('ISO VG grade (32 to 680): ')).upper()
    Tlub = float(input('Lubricant temperature / \u00b0C: '))
    GLUB = LUBRICANT_LIBRARY.LUBRICANT(BASE_NAME, LUB_NAME, Tlub)
# select element where is applied speed and torque (P - pinion, W - wheel)
PW_STR = 'Select (P - Pinion, W - Wheel or F - FZG) to apply torque and speed: '
element = str(input(PW_STR)).upper()
if element == 'F':
    STAGE = LOAD_STAGES.FZG()
    torque = STAGE.torque
    speed = float(input('FZG motor speed / rpm: '))
else:
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
    DIM_MESH = int(input('Mesh dimension (2/3): '))
    DIM = str(DIM_MESH)+'D'
    ORDER = int(input('Element order (1/2): '))
    PTOOTH = int(input('Number of tooth for pinion mesh: '))
    NODEP = int(
        input('Nº of nodes on pinion meshing surface: '))
    WTOOTH = int(input('Number of tooth for wheel mesh: '))
    NODEW = int(
        input('Nº of nodes on wheel meshing surface: '))
else:
    MESH = False

# ASSIGN GEAR MATERIALS =======================================================
GMAT = MATERIAL_LIBRARY.MATERIAL(MAT_PINION, MAT_WHEEL)
# GEAR GEOMETRY ACCORDING TO MAAG BOOK ========================================
GEO = CALC_GEOMETRY.MAAG(GTYPE)
# LINES OF CONTACT ASSUMING A RIGID LOAD SHARING (SPUR AND HELICAL) ===========
GPATH = RIGID_LOAD_SHARING.LINES(size, GEO)
# FORCES AND SPEEDS ===========================================================
GFS = FORCES_SPEEDS.OPERATION(element, torque, speed, GEO, GPATH)
# GEAR CONTACT QUANTITIES (PRESSURE, FILM THICKNESS, POWER LOSS) ==============
GCONTACT = CONTACT.HERTZ(GMAT, GLUB, GEO, GPATH, GFS, POSAE)
# LOAD CARRYING CAPACITY ======================================================
KA = 1.25
if MAT_PINION == ('STEEL' or 'ADI') and MAT_WHEEL == ('STEEL' or 'ADI')\
    and GLUB is not None:
    GL40 = LUBRICANT_LIBRARY.LUBRICANT(BASE_NAME, LUB_NAME, 40)
    GLCC = DIN3990.LCC(GMAT, GEO, GFS, KA, GL40)
else:
    try:
        GLCC = VDI2736.LCC(GMAT, GEO, GFS, GPATH, GCONTACT, T0, KA)
    except:
        GLCC = VDI2736.LCC(GMAT, GEO, GFS, GPATH, GCONTACT, Tlub, KA)
# INVOLUTE PROFILE GEOMETRY ===================================================
Pprofile = INVOLUTE_GEOMETRY.LITVIN('P', GEO, DISCRETIZATION)
Wprofile = INVOLUTE_GEOMETRY.LITVIN('W', GEO, DISCRETIZATION)
# INVOLUTE PROFILE GEOMETRY ===================================================
if MESH:
    MESH_GENERATOR.MESHING('P', GTYPE, GEO, Pprofile, PTOOTH, ORDER, NODEP, DIM)
    MESH_GENERATOR.MESHING('W', GTYPE, GEO, Wprofile, WTOOTH, ORDER, NODEW, DIM)
# OUTPUT PRINT ================================================================
OUTPUT_PRINT.PRINTING(GTYPE, GMAT, GLUB, GEO, GFS, GCONTACT, GLCC)
# OUTPUT GRAPHICS =============================================================
if GRAPHICS:
    PLOTTING.GRAPHICS(GPATH, GFS, GCONTACT)
# CLOSE PROGRAM ===============================================================
input("Press enter to exit")