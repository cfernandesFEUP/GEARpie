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
# sys.path.insert(0, "/usr/local/gmsh/lib")
import numpy as np
import gmsh
class MESHING:
    """Calculation of cylindrical gear geometry according to MAAG book"""
    # from numba import jit
    # @jit(nopython=True)
    def __init__(self, GEAR_ELEMENT, GEAR_NAME, GEO, PROFILE, NZ):
        ## convert to meter
        '''Generate the gear mesh with GMSH Python API'''
        
        if GEAR_ELEMENT == 'P':
            z = GEO.z1
            b = GEO.b1
            ra = GEO.ra1
            r = GEO.r1
            rs = GEO.dshaft1/2
            xc = 0
            yc = 0
            alfaZ = np.pi/z
        elif GEAR_ELEMENT == 'W':
            z = GEO.z2
            b = GEO.b2
            ra = GEO.ra2
            r = GEO.r2
            rs = GEO.dshaft2/2
            xc = 0
            yc = GEO.al
            alfaZ = np.pi/z
            rot = np.pi + 2*(NZ-1)*alfaZ - alfaZ
        
        PF = 1.2
        
        gmsh.initialize(sys.argv)
    
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.option.setNumber("Geometry.CopyMeshingMethod", 1)
        
        model = gmsh.model
        geog = model.geo
            
        # create GMSH model
        model.add(str(GEAR_NAME))
        
        geog.synchronize()
            
        PC = model.geo.addPoint(0, 0, b/2)
        
        # involiute
        PIl, PIr = [], []
        for i in range(len(PROFILE.xI)):
            PIl.append(geog.addPoint(PROFILE.xI[i], PROFILE.yI[i], b/2))
        for j in range(len(PROFILE.xI)):
            PIr.append(geog.addPoint(-PROFILE.xI[j], PROFILE.yI[j], b/2))
        
        CIl = geog.addSpline(PIl)
        CIr = geog.addSpline(PIr)
        
        # root fillet
        PFl, PFr = [], []
        for k in range(len(PROFILE.xRF-1)):
            PFl.append(geog.addPoint(PROFILE.xRF[k], PROFILE.yRF[k], b/2))
        PFl.append(PIl[0])
        for l in range(len(PROFILE.xRF-1)):
            PFr.append(geog.addPoint(-PROFILE.xRF[l], PROFILE.yRF[l], b/2))
        PFr.append(PIr[0])
        CFl = geog.addSpline(PFl)
        CFr = geog.addSpline(PFr)
        
        # tip circle
        PA = geog.addPoint(0, ra, b/2)
        CAl = geog.addCircleArc(PIl[-1], PC, PA)
        CAr = geog.addCircleArc(PIr[-1], PC, PA)   
        
        # shaft hole
        PS = geog.addPoint(0, rs, b/2)
        PSl = geog.addPoint(-rs*np.sin(alfaZ), rs*np.cos(alfaZ), b/2)
        PSr = geog.addPoint(rs*np.sin(alfaZ), rs*np.cos(alfaZ), b/2)
        CSl = geog.addCircleArc(PSl, PC, PS)
        CSr = geog.addCircleArc(PSr, PC, PS)
        
        # sides
        RCENTRAL = ra-1.05*PF*GEO.m*2.25
        MCx = -RCENTRAL*np.sin(alfaZ)
        MCy = RCENTRAL*np.cos(alfaZ)
        
        PLM = geog.addPoint(MCx, MCy, b/2)
        PRM = geog.addPoint(-MCx, MCy, b/2)
        CL = geog.addLine(PSl,PLM)
        CLu = geog.addLine(PLM,PFl[0])
        CR = geog.addLine(PSr,PRM)
        CRu = geog.addLine(PRM,PFr[0])
        
        # internal lines
        PMM = geog.addPoint(0, RCENTRAL, b/2) 
        CIHbl = geog.addLine(PLM,PMM)
        CIHbr = geog.addLine(PRM,PMM)
        CIVb = geog.addLine(PS,PMM)
        CIVu = geog.addLine(PMM,PA)
        CIHul = geog.addLine(PIl[0],PMM)
        CIHur = geog.addLine(PIr[0],PMM)  
        
        # curve loops
        CLAl = geog.addCurveLoop([CSl,CIVb,-CIHbl,-CL])
        CLAr = geog.addCurveLoop([-CSr,CR,CIHbr,-CIVb])
        CLBl = geog.addCurveLoop([CIHbl,-CIHul,-CFl,-CLu])
        CLBr = geog.addCurveLoop([-CIHbr,CRu,CFr,CIHur])
        CLCl = geog.addCurveLoop([CIHul,CIVu,-CAl,-CIl])
        CLCr = geog.addCurveLoop([CIr,CAr,-CIVu,-CIHur])
        
        SAl = geog.addPlaneSurface([CLAl])
        SAr = geog.addPlaneSurface([CLAr])
        
        SBl = geog.addPlaneSurface([CLBl])
        SBr = geog.addPlaneSurface([CLBr])
        
        SCl = geog.addPlaneSurface([CLCl])
        SCr = geog.addPlaneSurface([CLCr])
        
        # transfinite lines
        # thF = np.arccos(rb/ra)
        # thP = np.arccos(rb/r)
        # Sinvol = rb*(np.tan(thF)**2-np.tan(thP)**2)/2
        # ce = 0.25 # 3
        # eS = (-0.2*ce + 1.2)*min(a[-1])*1e3
        nM = 15#^int(Sinvol/eS)
        nR = nM//2+1
        nB = nM//2+1
        nAXIAL = 30
        coef = 1
        
        geog.mesh.setTransfiniteCurve(CAl,nB,'Progression',-coef)
        geog.mesh.setTransfiniteCurve(CAr,nB,'Progression',-coef)
        geog.mesh.setTransfiniteCurve(CIHul,nB,'Progression',-coef)
        geog.mesh.setTransfiniteCurve(CIHur,nB,'Progression',-coef)
        geog.mesh.setTransfiniteCurve(CLu,nB)
        geog.mesh.setTransfiniteCurve(CRu,nB)
        
        geog.mesh.setTransfiniteCurve(CIl,nM)
        geog.mesh.setTransfiniteCurve(CIr,nM)
        
        geog.mesh.setTransfiniteCurve(CIVu,nM)
        
        geog.mesh.setTransfiniteCurve(CFl,nR)
        geog.mesh.setTransfiniteCurve(CFr,nR)
        # geog.mesh.setTransfiniteCurve(CIVm,nR)
        
        geog.mesh.setTransfiniteCurve(CIVb,nB,'Progression',coef)
        geog.mesh.setTransfiniteCurve(CL,nB,'Progression',coef)
        geog.mesh.setTransfiniteCurve(CR,nB,'Progression',coef)
        
        geog.mesh.setTransfiniteCurve(CIHbl,nB,'Progression',-coef)
        geog.mesh.setTransfiniteCurve(CIHbr,nB,'Progression',-coef)
        
        geog.mesh.setTransfiniteCurve(CSl,nB)
        geog.mesh.setTransfiniteCurve(CSr,nB)
        
        geog.mesh.setTransfiniteSurface(SAl)
        geog.mesh.setTransfiniteSurface(SAr)
        geog.mesh.setTransfiniteSurface(SBl)
        geog.mesh.setTransfiniteSurface(SBr)
        geog.mesh.setTransfiniteSurface(SCl)
        geog.mesh.setTransfiniteSurface(SCr)
        
        geog.synchronize()
        
        self.helix = 2*np.sin(GEO.beta)/r
        self.twist = b*self.helix
        
        if GEAR_ELEMENT == 'W':
            geog.rotate(model.getEntities(dim = 2), 0, 0, 0, 0, 0, 1, rot)
            geog.translate(model.getEntities(dim = 2), xc, yc, 0)
        
        geog.synchronize()
        
        surfaces = model.getEntities(dim = 2)
        
        # extrusion  
        if NZ > 1:
            for j in range(1, NZ):
                cp = geog.copy(surfaces)            
                if GEAR_ELEMENT =='P':
                    geog.rotate(cp, 0, 0, 0, 0, 0, 1, -2*j*alfaZ)
                elif GEAR_ELEMENT == 'W':
                    geog.rotate(cp, xc, yc, 0, 0, 0, 1, -2*j*alfaZ)
                         
            geog.synchronize()
            surfROT = model.getEntities(dim = 2)
            
            # twist
            for surf in surfROT:
                geog.twist([surf], 0, 0, 0, 0, 0, -b, 0, 0, 1,\
                          self.twist,numElements=[nAXIAL],recombine=True)
        else:
              geog.twist(([2,SAl],[2,SAr],[2,SBl],[2,SBr],[2,SCl],[2,SCr]),\
                                0, 0, 1, 0, 0, -b, 0, 0, 1,\
                                self.twist, numElements=[nAXIAL],recombine=True) 
        geog.synchronize()
        
        self.VOLS = model.getEntities(dim = 3)
              
        self.ADD = 27*NZ+NZ-1
        self.OFFSET = 22
        self.Bshaft = [self.ADD, self.OFFSET+self.ADD]
        self.Btip = [96+self.ADD, 114+self.ADD]
        self.Broot = [52+self.ADD, 52+self.OFFSET+self.ADD]
        self.Bmesh = [110+self.ADD]
        self.Bnmesh = [100+self.ADD]
        self.BsidesF = [1,2,3,4,5,6]
        self.BsidesB = [13+self.ADD,13+self.OFFSET+self.ADD,\
                       13+2*self.OFFSET+self.ADD,13+3*self.OFFSET+self.ADD,\
                           13+4*self.OFFSET+self.ADD,13+5*self.OFFSET+self.ADD]

        ## PHYSICAL BOUNDARIES ============================================
        for i in range(1,NZ):
            self.Bshaft.extend([self.Bshaft[0]+i*132, self.Bshaft[1]+i*132])
            self.Btip.extend([self.Btip[0]+i*132, self.Btip[1]+i*132])
            self.Broot.extend([self.Broot[0]+i*132, self.Broot[1]+i*132])
            self.Bmesh.append(self.Bmesh[0]+i*132)
            self.Bnmesh.append(self.Bnmesh[0]+i*132)
            self.BsidesF.extend([self.BsidesF[j]+i*28+4*j-10 for j in range(6)])
            self.BsidesB.extend([j+i*132 for j in self.BsidesB])
            
        model.addPhysicalGroup(2, self.Bshaft, 1)
        model.setPhysicalName(2, 1, GEAR_ELEMENT+'SHAFT')    
        model.addPhysicalGroup(2, self.Btip, 2)
        model.setPhysicalName(2, 2, GEAR_ELEMENT+'TIP')
        model.addPhysicalGroup(2, self.Broot, 3)
        model.setPhysicalName(2, 3, GEAR_ELEMENT+'ROOT')
        model.addPhysicalGroup(2, self.Bmesh, 4)
        model.setPhysicalName(2, 4, GEAR_ELEMENT+'MESH')
        model.addPhysicalGroup(2, self.Bnmesh, 5)
        model.setPhysicalName(2, 5, GEAR_ELEMENT+'OMESH')
        model.addPhysicalGroup(2, self.Bnmesh+self.Btip+self.Broot, 6)
        model.setPhysicalName(2, 6, GEAR_ELEMENT+'NO-MESH')
        model.addPhysicalGroup(2, self.BsidesF+self.BsidesB, 7)
        model.setPhysicalName(2, 7, GEAR_ELEMENT+'SIDES')
        if NZ>=3:
            if GEAR_ELEMENT == 'P':
                for j in range(3):
                    model.addPhysicalGroup(2, [self.Bmesh[0]+j*132], 8+j)
                    model.setPhysicalName(2, 8+j, GEAR_ELEMENT+'CONT'+str(j+1))
                for j in range(3):
                    model.addPhysicalGroup(2, [self.Broot[1]+j*132], 11+j)
                    model.setPhysicalName(2, 11+j, GEAR_ELEMENT+'ROOT'+str(j+1))
            elif GEAR_ELEMENT == 'W':
                for j in range(3):
                    model.addPhysicalGroup(2, [self.Bmesh[-2]-j*132], 8+j)
                    model.setPhysicalName(2, 8+j, GEAR_ELEMENT+'CONT'+str(j+1))
                for j in range(3):
                    model.addPhysicalGroup(2, [self.Broot[-3]-j*132], 11+j)
                    model.setPhysicalName(2, 11+j, GEAR_ELEMENT+'ROOT'+str(j+1))
                
        model.addPhysicalGroup(3, [EL[1] for EL in self.VOLS], 1)
        model.setPhysicalName(3, 1, 'Gear' + GEAR_ELEMENT)
        
        # left/right
        if NZ < z:      
            model.addPhysicalGroup(2, [12+self.ADD], 14)
            model.setPhysicalName(2, 14, GEAR_ELEMENT+'LEFT')
            model.addPhysicalGroup(2, [26+self.ADD+(NZ-1)*132], 15)
            model.setPhysicalName(2, 15, GEAR_ELEMENT+'RIGHT')
            model.addPhysicalGroup(2, [12+self.ADD,26+self.ADD+(NZ-1)*132]\
                                   +self.Bshaft, 16)
            model.setPhysicalName(2, 16, GEAR_ELEMENT+'SLR')

        # generate mesh
        geog.synchronize()
        if GEAR_ELEMENT == 'W':
            gmsh.option.setNumber("Mesh.FirstElementTag", 10000000)
            gmsh.option.setNumber("Mesh.FirstNodeTag", 1000000)
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
        gmsh.option.setNumber("Mesh.ElementOrder", 1)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
        gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)
        model.mesh.generate(3)
        print('MESH CREATED')
        
        # save mesh
        file = GEAR_ELEMENT + str(GEAR_NAME)
        gmsh.write('Mesh/' + file + ".inp")
        print('SAVING MESH')
        gmsh.fltk.run()
        gmsh.finalize()
        print('FINISH!')