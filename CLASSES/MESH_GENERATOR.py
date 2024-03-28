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


class MESHING:
    '''Generate the gear mesh with GMSH Python API'''

    def __init__(self, GEAR_ELEMENT, GTYPE, GEO, PROFILE, NZ,
                 ORDER, NODEM, DIM_MESH):

        import sys
        import numpy as np
        import gmsh

        if GEAR_ELEMENT == 'P':
            z = GEO.z1
            b = GEO.b1
            ra = GEO.ra1
            r = GEO.r1
            rs = GEO.dshaft1/2
            xc = 0
            yc = 0
            self.alfaZ = np.pi/z
            self.helix = b*np.tan(GEO.beta)
            self.twist = self.helix/r
            rot = self.alfaZ
        elif GEAR_ELEMENT == 'W':
            z = GEO.z2
            b = GEO.b2
            ra = GEO.ra2
            r = GEO.r2
            rs = GEO.dshaft2/2
            xc = 0
            yc = GEO.al
            self.alfaZ = np.pi/z
            self.helix = -b*np.tan(GEO.beta)
            self.twist = self.helix/r
            rot = np.pi + 2*(NZ-1)*self.alfaZ - 2*self.alfaZ

        PF = 1.2

        gmsh.initialize(sys.argv)

        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.option.setNumber("Geometry.CopyMeshingMethod", 1)

        model = gmsh.model
        geog = model.geo

        # create GMSH model
        model.add(str(GTYPE.GEAR_NAME))

        geog.synchronize()
        if DIM_MESH=='3D':
            zv = b/2
        elif DIM_MESH=='2D':
            zv = 0
        PC = model.geo.addPoint(0, 0, zv)
        # involiute
        PIl, PIr = [], []
        for i in range(len(PROFILE.XinvT)):
            PIl.append(geog.addPoint(PROFILE.XinvT[i], PROFILE.YinvT[i], zv))
        for j in range(len(PROFILE.XinvT)):
            PIr.append(geog.addPoint(-PROFILE.XinvT[j], PROFILE.YinvT[j], zv))

        CIl = geog.addSpline(PIl)
        CIr = geog.addSpline(PIr)

        # root fillet
        PFl, PFr = [], []
        for ks in range(len(PROFILE.xRF-1)):
            PFl.append(geog.addPoint(PROFILE.xRF[ks], PROFILE.yRF[ks], zv))
        PFl.append(PIl[0])

        for ls in range(len(PROFILE.xRF-1)):
            PFr.append(geog.addPoint(-PROFILE.xRF[ls], PROFILE.yRF[ls], zv))
        PFr.append(PIr[0])

        CFl = geog.addSpline(PFl)
        CFr = geog.addSpline(PFr)

        # tip circle
        PA = geog.addPoint(0, ra, zv)
        CAl = geog.addCircleArc(PIl[-1], PC, PA)
        CAr = geog.addCircleArc(PIr[-1], PC, PA)

        # shaft hole
        PS = geog.addPoint(0, rs, zv)
        PSl = geog.addPoint(-rs*np.sin(self.alfaZ), rs*np.cos(self.alfaZ), zv)
        PSr = geog.addPoint(rs*np.sin(self.alfaZ), rs*np.cos(self.alfaZ), zv)
        CSl = geog.addCircleArc(PSl, PC, PS)
        CSr = geog.addCircleArc(PSr, PC, PS)

        # sides
        RCENTRAL = ra-1.05*PF*GEO.m*2.25
        MCx = -RCENTRAL*np.sin(self.alfaZ)
        MCy = RCENTRAL*np.cos(self.alfaZ)

        PLM = geog.addPoint(MCx, MCy, zv)
        PRM = geog.addPoint(-MCx, MCy, zv)
        CL = geog.addLine(PSl, PLM)
        CLu = geog.addLine(PLM, PFl[0])
        CR = geog.addLine(PSr, PRM)
        CRu = geog.addLine(PRM, PFr[0])

        # internal lines
        PMM = geog.addPoint(0, RCENTRAL, zv)
        CIHbl = geog.addLine(PLM, PMM)
        CIHbr = geog.addLine(PRM, PMM)
        CIVb = geog.addLine(PS, PMM)
        CIVu = geog.addLine(PMM, PA)
        CIHul = geog.addLine(PIl[0], PMM)
        CIHur = geog.addLine(PIr[0], PMM)

        # curve loops
        CLAl = geog.addCurveLoop([CSl, CIVb, -CIHbl, -CL])
        CLAr = geog.addCurveLoop([-CSr, CR, CIHbr, -CIVb])
        CLBl = geog.addCurveLoop([CIHbl, -CIHul, -CFl, -CLu])
        CLBr = geog.addCurveLoop([-CIHbr, CRu, CFr, CIHur])
        CLCl = geog.addCurveLoop([CIHul, CIVu, -CAl, -CIl])
        CLCr = geog.addCurveLoop([CIr, CAr, -CIVu, -CIHur])

        SAl = geog.addPlaneSurface([CLAl])
        SAr = geog.addPlaneSurface([CLAr])

        SBl = geog.addPlaneSurface([CLBl])
        SBr = geog.addPlaneSurface([CLBr])

        SCl = geog.addPlaneSurface([CLCl])
        SCr = geog.addPlaneSurface([CLCr])

        nR = NODEM//4+1
        nB = NODEM//4+1
        nAXIAL = 2*NODEM
        coef = 1

        geog.mesh.setTransfiniteCurve(CAl, nB, 'Progression', -coef)
        geog.mesh.setTransfiniteCurve(CAr, nB, 'Progression', -coef)
        geog.mesh.setTransfiniteCurve(CIHul, nB, 'Progression', -coef)
        geog.mesh.setTransfiniteCurve(CIHur, nB, 'Progression', -coef)
        geog.mesh.setTransfiniteCurve(CLu, nB)
        geog.mesh.setTransfiniteCurve(CRu, nB)

        geog.mesh.setTransfiniteCurve(CIl, NODEM)
        geog.mesh.setTransfiniteCurve(CIr, NODEM)

        geog.mesh.setTransfiniteCurve(CIVu, NODEM)

        geog.mesh.setTransfiniteCurve(CFl, nR)
        geog.mesh.setTransfiniteCurve(CFr, nR)
        # geog.mesh.setTransfiniteCurve(CIVm,nR)

        geog.mesh.setTransfiniteCurve(CIVb, nB, 'Progression', coef)
        geog.mesh.setTransfiniteCurve(CL, nB, 'Progression', coef)
        geog.mesh.setTransfiniteCurve(CR, nB, 'Progression', coef)

        geog.mesh.setTransfiniteCurve(CIHbl, nB, 'Progression', -coef)
        geog.mesh.setTransfiniteCurve(CIHbr, nB, 'Progression', -coef)

        geog.mesh.setTransfiniteCurve(CSl, nB)
        geog.mesh.setTransfiniteCurve(CSr, nB)

        geog.mesh.setTransfiniteSurface(SAl)
        geog.mesh.setTransfiniteSurface(SAr)
        geog.mesh.setTransfiniteSurface(SBl)
        geog.mesh.setTransfiniteSurface(SBr)
        geog.mesh.setTransfiniteSurface(SCl)
        geog.mesh.setTransfiniteSurface(SCr)

        geog.synchronize()

        geog.rotate(model.getEntities(dim=2), 0, 0, 0, 0, 0, 1, rot)
        geog.translate(model.getEntities(dim=2), xc, yc, 0)

        geog.synchronize()

        surfaces = model.getEntities(dim=2)

        # extrusion
        if NZ > 1:
            for j in range(1, NZ):
                cp = geog.copy(surfaces)
                geog.rotate(cp, xc, yc, 0, 0, 0, 1, -2*j*self.alfaZ)

            geog.synchronize()
            if DIM_MESH =='3D':
                surfROT = model.getEntities(dim=2)
                # twist
                for surf in surfROT:
                    geog.twist([surf], xc, yc, 0, 0, 0, -b, 0, 0, 1,
                           self.twist, numElements=[nAXIAL], recombine=True)
        else:
            ## 2D MESH
            if DIM_MESH =='3D':
                geog.twist(([2, SAl], [2, SAr], [2, SBl], [2, SBr], [2, SCl],
                        [2, SCr]), 0, 0, 1, 0, 0, -b, 0, 0, 1, self.twist,
                       numElements=[nAXIAL], recombine=True)

        geog.synchronize()

        if DIM_MESH =='3D':
            self.VOLS = model.getEntities(dim=3)
    
            self.ADD = 27*NZ+NZ-1
            self.OFFSET = 22
            self.Bshaft = [self.ADD, self.OFFSET+self.ADD]
            self.Btip = [96+self.ADD, 114+self.ADD]
            self.Broot = [52+self.ADD, 52+self.OFFSET+self.ADD]
            self.Bmesh = [110+self.ADD]
            self.Bnmesh = [100+self.ADD]
            self.BsidesF = [1, 2, 3, 4, 5, 6]
            self.BsidesB = [13+self.ADD, 13+self.OFFSET+self.ADD,
                            13+2*self.OFFSET+self.ADD, 13+3*self.OFFSET+self.ADD,
                            13+4*self.OFFSET+self.ADD, 13+5*self.OFFSET+self.ADD]

            # PHYSICAL BOUNDARIES ============================================
            for i in range(1, NZ):
                self.Bshaft.extend([self.Bshaft[0]+i*132, self.Bshaft[1]+i*132])
                self.Btip.extend([self.Btip[0]+i*132, self.Btip[1]+i*132])
                self.Broot.extend([self.Broot[0]+i*132, self.Broot[1]+i*132])
                self.Bmesh.append(self.Bmesh[0]+i*132)
                self.Bnmesh.append(self.Bnmesh[0]+i*132)
                self.BsidesF.extend(
                    [self.BsidesF[j]+i*28+4*j-10 for j in range(6)])
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
    
            if NZ >= 3:
                if GEAR_ELEMENT == 'P':
                    for j in range(NZ):
                        model.addPhysicalGroup(2, [self.Bmesh[0]+j*132], 8+j)
                        model.setPhysicalName(2, 8+j, GEAR_ELEMENT+'CONT'+str(j+1))
                    for j in range(NZ):
                        model.addPhysicalGroup(2, [self.Broot[1]+j*132], 8+NZ+j)
                        model.setPhysicalName(
                            2, 8+NZ+j, GEAR_ELEMENT+'ROOT'+str(j+1))
                elif GEAR_ELEMENT == 'W':
                    for j in range(NZ):
                        model.addPhysicalGroup(2, [self.Bmesh[-2]-j*132], 8+j)
                        model.setPhysicalName(2, 8+j, GEAR_ELEMENT+'CONT'+str(j+1))
                    for j in range(NZ):
                        model.addPhysicalGroup(2, [self.Broot[-3]-j*132], 8+NZ+j)
                        model.setPhysicalName(
                            2, 8+NZ+j, GEAR_ELEMENT+'ROOT'+str(j+1))
    
            model.addPhysicalGroup(3, [EL[1] for EL in self.VOLS], 1)
            model.setPhysicalName(3, 1, 'Gear' + GEAR_ELEMENT)
    
            # left/right
            if NZ < z:
                model.addPhysicalGroup(2, [12+self.ADD, 56+self.ADD], 8+2*NZ)
                model.setPhysicalName(2, 8+2*NZ, GEAR_ELEMENT+'LEFT')
                model.addPhysicalGroup(2, [26+self.ADD+(NZ-1)*132,
                                           70+self.ADD+(NZ-1)*132], 8+2*NZ+1)
                model.setPhysicalName(2, 8+2*NZ+1, GEAR_ELEMENT+'RIGHT')
                model.addPhysicalGroup(2, [12+self.ADD, 56+self.ADD,
                                           26+self.ADD+(NZ-1)*132,
                                           70+self.ADD+(NZ-1)*132]
                                       + self.Bshaft, 8+2*NZ+2)
                model.setPhysicalName(2, 8+2*NZ+2, GEAR_ELEMENT+'SLR')

        # generate mesh
        geog.synchronize()
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
        gmsh.option.setNumber("Mesh.ElementOrder", ORDER)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
        gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 1)
        if DIM_MESH=='3D':
            if GEAR_ELEMENT == 'W':
                gmsh.option.setNumber("Mesh.FirstElementTag", 4000000)
                gmsh.option.setNumber("Mesh.FirstNodeTag", 4000000)
            model.mesh.generate(3)
        elif DIM_MESH=='2D':
            if GEAR_ELEMENT == 'W':
                gmsh.option.setNumber("Mesh.FirstElementTag", 4000000)
                gmsh.option.setNumber("Mesh.FirstNodeTag", 4000000)
            model.mesh.generate(2)
            
        print('MESH CREATED')

        # save mesh
        #gmsh.fltk.run()
        file = GEAR_ELEMENT + str(GTYPE.GEAR_NAME)
        gmsh.write('MESH/' + file + ".inp")
        print('SAVING MESH')
        gmsh.finalize()
        print('FINISH!')
