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


class LCC:
    
    
    def __init__(self, GMAT, GEO, GFS, GCONTACT, T0, KA):

        import numpy as np
        # TEMPERATURE =========================================================
        self.TO = T0
        self.KA = KA
        # IN VDI 2736 is RLG = 1/k3 on page 11, Part 2
        # open gearbox free entry of air:   RLG = 0
        # partially open housing:           RLG = 0.015 to 0.045
        # closed housing:                   RLG 0.06
        self.RLG = 0.0
        self.A2V = 0.03
        
        if GMAT.MAT1 != GMAT.MAT2 and\
            GMAT.MAT1 == ('STEEL' or 'POM' or 'PA66'):
            # PLASTIC/STEEL
            self.kF = 6300
            self.kR = 895
        else:
            # PLASTIC/PLASTIC
            self.kF = 9000
            self.kR = 2148

        # GEAR TOOTH TEMPERATURE (FLANK)
        self.TF1 = (self.TO + GCONTACT.Pvzp*
                     (self.kF/(GEO.b*GEO.z1*(GFS.vt*GEO.m)**0.75) + 
                      self.RLG/self.A2V))
        self.TF2 = (self.TO + GCONTACT.Pvzp*
                     (self.kF/(GEO.b*GEO.z2*(GFS.vt*GEO.m)**0.75) + 
                      self.RLG/self.A2V))

        # GEAR TOOTH TEMPERATURE (ROOT)
        self.TR1 = (self.TO + GCONTACT.Pvzp*
                     (self.kR/(GEO.b*GEO.z1*(GFS.vt*GEO.m)**0.75) + 
                      self.RLG/self.A2V))
        self.TR2 = (self.TO + GCONTACT.Pvzp*
                     (self.kR/(GEO.b*GEO.z2*(GFS.vt*GEO.m)**0.75) + 
                      self.RLG/self.A2V))
        # EXCESS TEMPERATURE VERIFICATION =====================================
        
        
        # EXCESS LOAD VERIFICATION ============================================
        
        # ROOT STRESS =========================================================
        self.NL = 1e8
        # influence factor
        self.KF = self.KA
        # form factor
        self.zn1 = GEO.z1 / (np.cos(GEO.betab) ** 2 * np.cos(GEO.beta))
        self.zn2 = GEO.z2 / (np.cos(GEO.betab) ** 2 * np.cos(GEO.beta))
        self.dn1 = GEO.m*self.zn1
        self.dn2 = GEO.m*self.zn2
        self.dbn1 = self.dn1*np.cos(GEO.alpha)
        self.dbn2 = self.dn2*np.cos(GEO.alpha)
        if GEO.beta == 0:
            self.rfer = 0.375
        else:
            self.rfer = 0.3
        self.rfP = self.rfer*GEO.m
        self.hfP = GEO.hfP*GEO.m
        self.spr = 0
        self.G1 = self.rfP/GEO.m - self.hfP/GEO.m + GEO.x1
        self.G2 = self.rfP/GEO.m - self.hfP/GEO.m + GEO.x2
        self.Es = (np.pi/4*GEO.m - self.hfP * np.tan(GEO.alpha) +
                   self.spr/np.cos(GEO.alpha) - (1 - np.sin(GEO.alpha))*
                   self.rfP/np.cos(GEO.alpha))
        self.H1 = 2/self.zn1*(np.pi/2 - self.Es/GEO.m) - np.pi/3
        self.H2 = 2/self.zn2*(np.pi/2 - self.Es/GEO.m) - np.pi/3
        from scipy import optimize
        def eq1(inp):
            return inp - 2*self.G1/self.zn1*np.tan(inp) + self.H1
        self.vu1 = optimize.brentq(eq1, 0, np.pi/2.1)
        def eq2(inp):
            return inp - 2*self.G2/self.zn2*np.tan(inp) + self.H2
        self.vu2 = optimize.brentq(eq2, 0, np.pi/2.1)

        self.sFn1 = GEO.m*(self.zn1*np.sin(np.pi/3 - self.vu1) + 3**(1/2)*
                           (self.G1/np.cos(self.vu1) - self.rfP/GEO.m))
        self.sFn2 = GEO.m*(self.zn2*np.sin(np.pi/3 - self.vu2) + 3**(1/2)*
                           (self.G2/np.cos(self.vu2) - self.rfP/GEO.m))
        self.dan1 = self.dn1 + GEO.da1 - GEO.d1
        self.dan2 = self.dn2 + GEO.da2 - GEO.d2
        self.alpha_an1 = np.arccos(self.dbn1/self.dan1)
        self.alpha_an2 = np.arccos(self.dbn2/self.dan2)
        self.gamma_a1 = ((np.pi/2 + 2*GEO.x1*np.tan(GEO.alpha))/self.zn1 + 
                         np.tan(GEO.alpha) - GEO.alpha - 
                         np.tan(self.alpha_an1) + self.alpha_an1)
        self.gamma_a2 = ((np.pi/2 + 2*GEO.x2*np.tan(GEO.alpha))/self.zn2 + 
                         np.tan(GEO.alpha) - GEO.alpha - 
                         np.tan(self.alpha_an2) + self.alpha_an2)
        self.alphaFan1 = self.alpha_an1 - self.gamma_a1
        self.alphaFan2 = self.alpha_an2 - self.gamma_a2
        self.hFa1 = 0.5*GEO.m*((np.cos(self.gamma_a1) - np.sin(self.gamma_a1)*
                                np.tan(self.alphaFan1))*self.dan1/GEO.m - 
                               self.zn1*np.cos(np.pi/3 - self.vu1) - self.G1/
                               np.cos(self.vu1) + self.rfP/GEO.m)
        self.hFa2 = 0.5*GEO.m*((np.cos(self.gamma_a2) - np.sin(self.gamma_a2)*
                                np.tan(self.alphaFan2))*self.dan2/GEO.m - 
                               self.zn2*np.cos(np.pi/3 - self.vu2) - self.G2/
                               np.cos(self.vu2) + self.rfP/GEO.m)
        self.YFa1 = (6*(self.hFa1/GEO.m)*np.cos(self.alphaFan1)/
                     ((self.sFn1/GEO.m)**2*np.cos(GEO.alpha)))
        self.YFa2 = (6*(self.hFa2/GEO.m)*np.cos(self.alphaFan2)/
                     ((self.sFn2/GEO.m)**2*np.cos(GEO.alpha)))
        # stress correction factor
        self.Fact11 = 2*self.G1**2
        self.Fact12 = 2*self.G2**2
        self.Fact21 = np.cos(self.vu1)*(self.zn1*np.cos(self.vu1)**2 - 
                                        2*self.G1)
        self.Fact22 = np.cos(self.vu2)*(self.zn2*np.cos(self.vu2)**2 - 
                                        2*self.G2)
        self.rF1 = GEO.m*(self.rfP/GEO.m + self.Fact11/self.Fact21)
        self.rF2 = GEO.m*(self.rfP/GEO.m + self.Fact12/self.Fact22)
        self.LS1 = self.sFn1/self.hFa1
        self.LS2 = self.sFn2/self.hFa2
        self.qs1 = self.sFn1/(2*self.rF1)
        self.qs2 = self.sFn2/(2*self.rF2)
        self.YSa1 = (1.2 + 0.13*self.LS1)*self.qs1**(1./(1.21 + 2.3/self.LS1))
        self.YSa2 = (1.2 + 0.13*self.LS2)*self.qs2**(1./(1.21 + 2.3/self.LS2))
        # contact ratio factor
        self.Yeps = 0.25 + 0.75/GEO.epslon_alpha
        # helix angle factor
        if GEO.epslon_beta > 1:
            self.ebeta = 1
        else:
            self.ebeta = GEO.epslon_beta
        if GEO.beta > 30*np.pi/180:
            self.betaDIN = 30
        else:
            self.betaDIN = GEO.beta*180/np.pi
        self.Ybeta = 1 - self.ebeta*self.betaDIN / 120
        # stress correction factor
        self.YSt = 2
        # minimum safety factor root stress
        self.SFmin = 2
        # tooth root stress
        self.SigmaF1 = (GFS.ft/(GEO.b*GEO.m)*self.YFa1*self.YSa1*self.Yeps*
                        self.Ybeta)
        self.SigmaF2 = (GFS.ft/(GEO.b*GEO.m)*self.YFa2*self.YSa2*self.Yeps*
                        self.Ybeta)
        self.SigmaFG1 = GMAT.SigmaFlim1(self.TR1,self.NL)*self.YSt
        self.SigmaFG2 = GMAT.SigmaFlim2(self.TR2,self.NL)*self.YSt
        self.SigmaFP1 = self.SigmaFG1/self.SFmin
        self.SigmaFP2 = self.SigmaFG2/self.SFmin
        self.SF1 = self.SigmaFG1/self.SigmaF1
        self.SF2 = self.SigmaFG2/self.SigmaF2
        
        # FLANK STRESS ========================================================
        # influence factor
        self.KH = self.KA
        # elasticity factor
        self.ZE = (1/(np.pi*((1 - GMAT.v1**2)/GMAT.E1 + 
                             (1 - GMAT.v2**2)/GMAT.E2)))**(1/2)
        # zone factor
        self.ZH = (2*np.cos(GEO.betab)*np.cos(GEO.alphatw)/
              (np.cos(GEO.alphat)**2*np.sin(GEO.alphatw)))**(1/2)
        # contact ratio factor
        if GEO.epslon_beta < 1:
            self.ZEPS = ((4-GEO.epslon_alpha)*(1-GEO.epslon_beta)/3 + 
                         GEO.epslon_beta/GEO.epslon_alpha)**(1/2)
        else:
            self.ZEPS = (1/GEO.epslon_alpha)**(1/2)
        # helix angle factor
        self.ZBETA = (np.cos(GEO.beta))**(1/2)
        # surface roughness factor
        self.ZR = 1
        # flank stress
        self.SigmaH = (self.ZE*self.ZH*self.ZEPS*self.ZBETA*
                    (GFS.ft*(GEO.u+1)/(GEO.b*GEO.d1*GEO.u))**(1/2))
        self.SHmin = 1.4
        self.SigmaHP1 = GMAT.SigmaHlim1(self.TF1,self.NL)/self.SHmin*self.ZR
        self.SigmaHP2 = GMAT.SigmaHlim1(self.TF2,self.NL)/self.SHmin*self.ZR
        self.SH1 = self.SigmaHP1*self.SHmin/self.SigmaH
        self.SH2 = self.SigmaHP2*self.SHmin/self.SigmaH