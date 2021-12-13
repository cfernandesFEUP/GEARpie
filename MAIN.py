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

import sys
sys.dont_write_bytecode = True
import GEAR_LIBRARY, CALC_GEOMETRY, RIGID_LOAD_SHARING, FORCES_SPEEDS,\
    INVOLUTE_GEOMETRY, MESH_GENERATOR, PLOTTING

## INPUT ######################################################################

# name of gear on library ()
GEAR_NAME = 'C14'

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

## GEAR SELECTION #############################################################
Gtype = GEAR_LIBRARY.GEAR(GEAR_NAME)

## OPERATING CONDITIONS #######################################################
if torque is str:
    torque = torque

## GEAR GEOMETRY ACCORDING TO MAAG BOOK #######################################
Ggeo = CALC_GEOMETRY.MAAG(Gtype)

## LINES OF CONTACT ASSUMING A RIGID LOAD SHARING (SPUR AND HELICAL) ##########

Glines = RIGID_LOAD_SHARING.LINES(size, Ggeo)

## FORCES AND SPEEDS ##########################################################
Goper = FORCES_SPEEDS.OPERATION(element, torque, speed, Ggeo, Glines)

## INVOLUTE PROFILE GEOMETRY ##################################################

Pprofile = INVOLUTE_GEOMETRY.LITVIN('P', Ggeo, DISCRETIZATION)
Wprofile = INVOLUTE_GEOMETRY.LITVIN('W', Ggeo, DISCRETIZATION)

## INVOLUTE PROFILE GEOMETRY ##################################################
Pmesh = MESH_GENERATOR.MESHING('P', GEAR_NAME, Ggeo, Pprofile, 4)
Wmesh = MESH_GENERATOR.MESHING('W', GEAR_NAME, Ggeo, Wprofile, 5)

## GRAPHICS ###################################################################
# Ploted = PLOTTING.GRAPHICS(Glines, Goper)
