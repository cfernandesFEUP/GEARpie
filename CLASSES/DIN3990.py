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
    """Calculation of load carrying capacity according to DIN 3990 method C"""
    
    def __init__(self, GMAT, GEO, GFS, KA, GL40):

        import numpy as np
        self.KA = KA
        # stiffness
        self.zn1 = GEO.z1 / (np.cos(GEO.betab) ** 2 * np.cos(GEO.beta))
        self.zn2 = GEO.z2 / (np.cos(GEO.betab) ** 2 * np.cos(GEO.beta))
        self.C1 = 0.04723
        self.C2 = 0.15551
        self.C3 = 0.25791
        self.C4 = -0.00635
        self.C5 = -0.11654
        self.C6 = -0.00193
        self.C7 = -0.24188
        self.C8 = 0.00529
        self.C9 = 0.00182
        self.ql = (self.C1 + self.C2/self.zn1 + self.C3/self.zn2 + 
                   self.C4*GEO.x1 + (self.C5*GEO.x1)/self.zn1 + 
                   self.C6*GEO.x2 + (self.C7*GEO.x1)/self.zn2 + 
                   self.C8*GEO.x1**2 + self.C9 *GEO.x2**2)
        self.clth = 1/self.ql
        self.CM = 0.8
        self.CR = 1
        self.CB = 1
        if GFS.ft*self.KA/GEO.b < 100:
            self.cl = (self.clth*self.CM*self.CR*self.CB*np.cos(GEO.beta)*
                       ((GFS.ft*self.KA/GEO.b)/100)**0.25)
        else:
            self.cl = self.clth*self.CM*self.CR*self.CB*np.cos(GEO.beta)
        self.cgama = self.cl*(0.75*GEO.epslon_alpha + 0.25)

        # internal dynamic factor (KV)
        Ca = 0 ## tip relief
        # mean diameter
        self.dm1 = GEO.ra1 + GEO.rf1
        self.dm2 = GEO.ra2 + GEO.rf2
        # equivalent mass
        self.mred = ((np.pi/8)*(self.dm1/(2*GEO.rb1))**2*
            (self.dm1**2/(1/(1e-9*GMAT.rho1) + 1/(1e-9*GMAT.rho2*GEO.u**2))))
        # critical seed
        self.nE1 = 30000/(np.pi*GEO.z1)*np.sqrt(self.cgama/self.mred)
        # ressonance ratio
        self.N = GFS.speed1/self.nE1
        if GFS.ft*self.KA/GEO.b <= 100:
            self.NS = 0.85
        else:
            self.NS = 0.5 + 0.35*(GFS.ft*self.KA/(100*GEO.b))**(1/2)
        # pitch deviation effect
        if GEO.epslon_gama <= 2:
            self.Cv1 = 0.32
            self.Cv2 = 0.34
            self.Cv3 = 0.23
            self.Cv4 = 0.90
            self.Cv5 = 0.47
            self.Cv6 = 0.47
        else:
            self.Cv1 = 0.32
            self.Cv2 = 0.57/(GEO.epslon_gama - 0.3)
            self.Cv3 = 0.096/(GEO.epslon_gama - 1.56)
            self.Cv4 = (0.57 - 0.05*GEO.epslon_gama)/(GEO.epslon_gama - 1.44)
            self.Cv5 = 0.47
            self.Cv6 = 0.12/(GEO.epslon_gama - 1.74)
        if GEO.epslon_gama <= 1.5:
            self.Cv7 = 0.75
        elif GEO.epslon_gama > 1.5 or GEO.epslon_gama <= 2.5:
            self.Cv7 = 0.125 * np.sin(np.pi * (GEO.epslon_gama - 2)) + 0.875
        elif GEO.epslon_gama > 2.5:
            self.Cv7 = 1
        #Cay1 = (1 / 18) * (sigmaHlim1 / 97 - 18.45) ** 2 + 1.5
        #Cay2 = (1 / 18) * (sigmaHlim2 / 97 - 18.45) ** 2 + 1.5
        #Cay = 0.5 * (Cay1 + Cay2)
        self.fpb = 0.3*(GEO.m + 0.4*np.sqrt(2*GEO.r2)) + 4
        self.falpha = 2.5*np.sqrt(GEO.m) + 0.17*(2*GEO.r2)**(1/2) + 0.5
        self.fbeta = 0.1*(2*GEO.r2)**(1/2) + 0.63*GEO.b**(1/2) + 4.2
        self.yp = 0.0758*self.fpb
        self.yf = 0.075*self.falpha
        self.fpb_eff = self.fpb - self.yp
        self.falpha_eff = self.falpha - self.yf
        self.Bp = self.cl*self.fpb_eff/(self.KA*(GFS.ft/GEO.b))
        self.Bf = self.cl*self.falpha_eff/(self.KA*(GFS.ft/GEO.b))
        self.Bk = abs(1 - self.cl*Ca/(self.KA*(GFS.ft/GEO.b)))
        if self.N <= self.NS:
            self.Kr = ((self.Cv1*self.Bp) + (self.Cv2*self.Bf) + 
                       (self.Cv3*self.Bk))
            self.KV = (self.N*self.Kr) + 1
        elif self.N > self.NS or self.N <= 1.15:
            self.KV = ((self.Cv1 * self.Bp) + (self.Cv2 * self.Bf) + 
                       (self.Cv4 * self.Bk) + 1)
        elif self.N >= 1.5:
            self.KV = (self.Cv5 * self.Bp) + (self.Cv6 * self.Bf) + self.Cv7
        
        # face load factors (KHB and KFB)
        self.fm = GFS.ft*self.KA*self.KV
        ## DIN 3990
        ## BHB = 1
        #KlHB = 1.00
        # slHB = 0.05
        # gama = (abs(BHB + KlHB * slHB / (d[0] ** 2) * (d[0] / dsh) ** 4 - 0.3) + 0.3) * (b / d[0]) ** 2
        # fsh0 = 0.023 * gama
        # fsh = fsh0 * fm / b
        self.fsh = 0
        self.fma = 0.5*self.fbeta
        self.fbetax = 1.33*self.fsh + self.fma
        self.ybeta = 0.15*self.fbetax
        # xbeta = 0.85
        if self.ybeta > 6:
            self.ybeta = 6
        self.fbetay = self.fbetax - self.ybeta
        self.KHBope = self.fbetay*self.cgama/(2*self.fm/GEO.b)
        if self.KHBope >= 1:
            self.KHB = (2*self.fbetay*self.cgama/(self.fm/GEO.b))**(1/2)
            self.bcalb = ((2*self.fm/GEO.b)/(self.fbetay*self.cgama))**(1/2)
        elif self.KHBope < 1:
            self.KHB = 1 + self.fbetay*self.cgama/(2*self.fm/GEO.b)
        ## bcalb = 0.5 + (fm / b) / (fbetay * cgama)
        self.h1 = GEO.ra1 - GEO.rf1
        self.h2 = GEO.ra2 - GEO.rf2
        if self.h1 > self.h2:
            self.h = self.h1
        else:
            self.h = self.h2
        
        if self.h/GEO.b > (1/3):
            self.hsb = 1 / 3
        else:
            self.hsb = self.h/GEO.b
        
        self.NF = 1/(1 + self.hsb + self.hsb**2)
        self.KFB = self.KHB ** self.NF
        
        # transverse load factors(KHA and KFA)
        self.fth = GFS.ft*self.KA*self.KV*self.KHB
        self.yalpha = 0.075*self.fpb
        if GEO.epslon_gama <= 2:
            self.KHA = GEO.epslon_gama/2*(0.9 + 0.4*self.cgama*
                                          (self.fpb - self.yalpha)/
                                          (self.fth/GEO.b))
        else:
            self.KHA = (0.9 + 0.4*(2*(GEO.epslon_gama - 1)/
                                   GEO.epslon_gama)**(1/2)*self.cgama*
                        (self.fpb - self.yalpha)/(self.fth/GEO.b))
        # contact ratio factor
        if GEO.epslon_beta < 1:
            self.ZEPS = ((4 - GEO.epslon_alpha)*(1 - GEO.epslon_beta)/3 +
                          GEO.epslon_beta/GEO.epslon_alpha)**(1/2)
        else:
            self.ZEPS = (1/GEO.epslon_alpha)**(1/2)
        if self.KHA > GEO.epslon_gama/(GEO.epslon_alpha*self.ZEPS**2):
            self.KHA =GEO. epslon_gama/(GEO.epslon_alpha*self.ZEPS**2)
        elif self.KHA <= 1:
            self.KHA = 1
        self.KFA = self.KHA
        self.KH = self.KA*self.KV*self.KHB*self.KHA
        self.KF = self.KA*self.KV*self.KFB*self.KFA
        # pinion and wheel factors
        self.M1 = (np.tan(GEO.alphatw)/
                   (((GEO.ra1**2/GEO.rb1**2 - 1)**(1/2) - 2*np.pi/GEO.z1)*
                    ((GEO.ra2**2/GEO.rb2**2 - 1)**(1/2) - 
                     (GEO.epslon_alpha - 1)*2*np.pi/GEO.z2))**(1/2))
        self.M2 = (np.tan(GEO.alphatw)/
                   (((GEO.ra2**2/GEO.rb2**2 - 1)**(1/2) - 2*np.pi/GEO.z2)*
                    ((GEO.ra1**2/GEO.rb1**2 - 1)**(1/2) - 
                     (GEO.epslon_alpha - 1)*2*np.pi/GEO.z1))**(1/2))
        
        if GEO.epslon_beta >= 1:
            self.ZP = 1
            self.ZW = 1
        else:
            self.ZP = self.M1 - GEO.epslon_beta*(self.M1 - 1)
            self.ZW = self.M2 - GEO.epslon_beta*(self.M2 - 1)
            if self.ZP < 1:
                self.ZP = 1
            if self.ZW < 1:
                self.ZW = 1

        # elasticity factor
        self.ZE = (1/(np.pi*((1 - GMAT.v1**2)/GMAT.E1 + 
                             (1 - GMAT.v2**2)/GMAT.E2)))**(1/2)
        
        # zone factor
        self.ZH = (2*np.cos(GEO.betab)*np.cos(GEO.alphatw)/
              (np.cos(GEO.alphat)**2*np.sin(GEO.alphatw)))**(1/2)
        # helix angle factor
        self.ZBETA = (np.cos(GEO.beta))**(1/2)
        # Lubrication coefficient
        self.ZL = 0.91 + 0.36 / (1.2 + 134/GL40.niu)**2
        self.vt = np.pi*GFS.speed1*GEO.r1/30000
        # speed factor
        self.ZV = 0.93 + 0.14/(0.8 + 32/self.vt) ** 0.5
        # surface factor
        self.ZR = 1.02*(GEO.al**(1/3)/(GEO.RzS))**0.08
        self.ZLUB = self.ZL*self.ZV*self.ZR
        # FLANK STRESS ========================================================
        self.SigmaH0 = (self.ZE*self.ZH*self.ZEPS*self.ZBETA*
                    (GFS.ft*(GEO.u+1)/(GEO.b*GEO.d1*GEO.u))**(1/2))
        self.SigmaH1 = self.ZP*self.SigmaH0*self.KH**(1/2)
        self.SigmaH2 = self.ZW*self.SigmaH0*self.KH**(1/2)
        self.SHmin = 1.0
        self.SigmaHP1 = GMAT.SigmaHlim1/self.SHmin*self.ZLUB
        self.SigmaHP2 = GMAT.SigmaHlim2/self.SHmin*self.ZLUB
        self.SH1 = self.SigmaHP1*self.SHmin/self.SigmaH1
        self.SH2 = self.SigmaHP2*self.SHmin/self.SigmaH2
        # tooth form factor (YF)
        if GEO.beta == 0:
            self.rfer = 0.375
        else:
            self.rfer = 0.3
        self.rfP = self.rfer*GEO.m
        self.hfP = GEO.hfP*GEO.m
        self.spr = 0
        self.dn1 = GEO.m*self.zn1
        self.dn2 = GEO.m*self.zn2
        self.dbn1 = self.dn1*np.cos(GEO.alpha)
        self.dbn2 = self.dn2*np.cos(GEO.alpha)
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
        self.epslon_alphan = GEO.epslon_alpha/(np.cos(GEO.betab)**2)
        self.FCT11 = ((self.dan1/2)** 2 - (self.dbn1/2)**2)**0.5
        self.FCT12 = ((self.dan2/2)** 2 - (self.dbn2/2)**2)**0.5
        self.FCT21 = (np.pi*GEO.d1*np.cos(GEO.beta)*np.cos(GEO.alpha)/GEO.z1
                      *(self.epslon_alphan - 1))
        self.FCT22 = (np.pi*GEO.d2*np.cos(GEO.beta)*np.cos(GEO.alpha)/GEO.z2
                      *(self.epslon_alphan - 1))
        self.FCT31 = (self.dbn1/2)**2
        self.FCT32 = (self.dbn2/2)**2
        self.den1 = 2*((self.FCT11 - self.FCT21)**2 + self.FCT31)**0.5
        self.den2 = 2*((self.FCT12 - self.FCT22)**2 + self.FCT32)**0.5
        self.alpha_en1 = np.arccos(self.dbn1/self.den1)
        self.alpha_en2 = np.arccos(self.dbn2/self.den2)
        self.gamma_e1 = ((np.pi/2 + 2*GEO.x1*np.tan(GEO.alpha))/self.zn1 + 
                         np.tan(GEO.alpha) - GEO.alpha - 
                         np.tan(self.alpha_en1) + self.alpha_en1)
        self.gamma_e2 = ((np.pi/2 + 2*GEO.x2*np.tan(GEO.alpha))/self.zn2 + 
                         np.tan(GEO.alpha) - GEO.alpha - 
                         np.tan(self.alpha_en2) + self.alpha_en2)
        self.alphaFen1 = self.alpha_en1 - self.gamma_e1
        self.alphaFen2 = self.alpha_en2 - self.gamma_e2
        self.hFe1 = 0.5*GEO.m*((np.cos(self.gamma_e1) - np.sin(self.gamma_e1)*
                                np.tan(self.alphaFen1))*self.den1/GEO.m - 
                               self.zn1*np.cos(np.pi/3 - self.vu1) - self.G1/
                               np.cos(self.vu1) + self.rfP/GEO.m)
        self.hFe2 = 0.5*GEO.m*((np.cos(self.gamma_e2) - np.sin(self.gamma_e2)*
                                np.tan(self.alphaFen2))*self.den2/GEO.m - 
                               self.zn2*np.cos(np.pi/3 - self.vu2) - self.G2/
                               np.cos(self.vu2) + self.rfP/GEO.m)
        self.YF1 = (6*(self.hFe1/GEO.m)*np.cos(self.alphaFen1)/
                    ((self.sFn1/GEO.m)**2*np.cos(GEO.alpha)))
        self.YF2 = (6*(self.hFe2/GEO.m)*np.cos(self.alphaFen2)/
                    ((self.sFn2/GEO.m)**2*np.cos(GEO.alpha)))
        # stress correction factor (YS) 
        self.Fact11 = 2*self.G1**2
        self.Fact12 = 2*self.G2**2
        self.Fact21 = np.cos(self.vu1)*(self.zn1*np.cos(self.vu1)**2 - 
                                        2*self.G1)
        self.Fact22 = np.cos(self.vu2)*(self.zn2*np.cos(self.vu2)**2 - 
                                        2*self.G2)
        self.rF1 = GEO.m*(self.rfP/GEO.m + self.Fact11/self.Fact21)
        self.rF2 = GEO.m*(self.rfP/GEO.m + self.Fact12/self.Fact22)
        self.LS1 = self.sFn1/self.hFe1
        self.LS2 = self.sFn2/self.hFe2
        self.qs1 = self.sFn1/(2*self.rF1)
        self.qs2 = self.sFn2/(2*self.rF2)
        self.YS1 = (1.2 + 0.13*self.LS1)*self.qs1**(1./(1.21 + 2.3/self.LS1))
        self.YS2 = (1.2 + 0.13*self.LS2)*self.qs2**(1./(1.21 + 2.3/self.LS2))
        # helix angle factor (YB)
        if GEO.epslon_beta > 1:
            self.ebeta = 1
        else:
            self.ebeta = GEO.epslon_beta
        if GEO.beta > 30*np.pi/180:
            self.betaDIN = 30
        else:
            self.betaDIN = GEO.beta*180/np.pi
        
        self.YB = 1 - self.ebeta*self.betaDIN / 120
        # notch sensitivity factor (YdelT)
        self.YdelT1 = 0.9434 + 0.0231*(1 + 2*self.qs1)**0.5
        self.YdelT2 = 0.9434 + 0.0231*(1 + 2*self.qs2)**0.5
        # # YdelT = 0.44 * YS + 0.12 # static analysis
        # surface factor (YRrelT)
        self.YRrelT1 = 0.957
        self.YRrelT2 = 0.957
        # if GTYPE.Rz[0] < 1:
        #     self.RzDIN1 = 1
        # else:
        #     self.RzDIN1 = GTYPE.Rz[0]
        # if GTYPE.Rz[1]  < 1:
        #     self.RzDIN2 = 1
        # else:
        #     self.RzDIN2 = GTYPE.Rz[1]
        # self.YRrelT1 = 1.674 - 0.529 * (self.RzDIN1 + 1) ** 0.1
        # self.YRrelT2 = 1.674 - 0.529 * (self.RzDIN2 + 1) ** 0.1
        # 5.306 - 4.203 * (RzDIN + 1) ** 0.01
        # # YRrelT = 4.299 - 3.259 * (RzDIN + 1) ** 0.0058
        # ROOT STRESS =========================================================
        self.SigmaFlim = 430
        self.SFmin = 1.4
        self.Yst = 2
        self.SigmaFE1 = GMAT.SigmaFlim1*self.Yst
        self.SigmaFE2 = GMAT.SigmaFlim2*self.Yst
        self.SigmaF01 = GFS.ft/(GEO.b*GEO.m)*self.YF1*self.YS1*self.YB
        self.SigmaF02 = GFS.ft/(GEO.b*GEO.m)*self.YF2*self.YS2*self.YB
        self.SigmaF1 = self.SigmaF01*self.KF
        self.SigmaF2 = self.SigmaF02*self.KF
        self.SigmaFG1 = self.SigmaFE1*self.YdelT1*self.YRrelT1
        self.SigmaFG2 = self.SigmaFE2*self.YdelT2*self.YRrelT2
        self.SigmaFP1 = self.SigmaFG1/self.SFmin
        self.SigmaFP2 = self.SigmaFG1/self.SFmin
        self.SF1 = self.SigmaFG1/self.SigmaF1
        self.SF2 = self.SigmaFG2/self.SigmaF2
