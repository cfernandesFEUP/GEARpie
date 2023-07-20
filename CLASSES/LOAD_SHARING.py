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


class LINES:
    """Calculation of lines of contact length assuming a ridig load sharing model"""

    def __init__(self, size, GEO, GMAT, Pprofile, Wprofile):

        import numpy as np
        # contact size
        self.size = size
        # condition A
        self.COND_A = GEO.b*np.tan(GEO.betab)
        # condition B
        self.COND_B = GEO.epslon_alpha*GEO.pbt
        # condition C
        self.COND_C = GEO.epslon_beta*GEO.pbt
        # condition D
        self.COND_D = (GEO.epslon_alpha + GEO.epslon_beta)*GEO.pbt
        # x discretization
        self.xx = np.linspace(0., self.COND_D, self.size)
        # face width discretization
        self.DISC_SIZE_AE = self.COND_B/len(self.xx)
        self.DISC_b = int(GEO.b/self.DISC_SIZE_AE)
        self.bpos = np.linspace(0, GEO.b, self.DISC_b)
        # number of tooth for the analysis
        self.N = int(np.ceil(GEO.epslon_alpha + GEO.epslon_beta))
        self.kt = np.arange(-self.N, self.N + 1)
        # create arrays
        self.XC = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])
        self.Lh = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])
        self.L = np.zeros([len(self.xx), len(self.bpos)])
        
        # offset discretization according to the kth tooth
        for i in range(len(self.kt)):
            self.XC[i] = (np.tile(self.xx, (len(self.bpos), 1)).T +
                          self.kt[i]*GEO.pbt +
                          np.tile(self.bpos*np.tan(GEO.betab),
                                  (len(self.xx), 1)))
        
        # conditions (A to D) to calculate contacting lines
        if GEO.epslon_beta < 1:
            self.indA = np.where((self.XC >= 0)*(self.XC < self.COND_A))
            self.indB = np.where((self.XC >= self.COND_A)
                                 * (self.XC < self.COND_B))
            self.indC = np.where((self.XC >= self.COND_B)
                                 * (self.XC < self.COND_D))
            self.Lh[self.indA] = self.XC[self.indA]/np.sin(GEO.betab)
            self.Lh[self.indB] = GEO.b/np.cos(GEO.betab)
            self.Lh[self.indC] = GEO.b/np.cos(GEO.betab)\
                - (self.XC[self.indC] - self.COND_B)/np.sin(GEO.betab)
        else:
            self.indA = np.where((self.XC >= 0)*(self.XC < self.COND_B))
            self.indB = np.where((self.XC >= self.COND_B)
                                 * (self.XC < self.COND_C))
            self.indC = np.where((self.XC >= self.COND_C)
                                 * (self.XC < self.COND_D))
            self.Lh[self.indA] = self.XC[self.indA]/np.sin(GEO.betab)
            self.Lh[self.indB] = self.COND_B/np.sin(GEO.betab)
            self.Lh[self.indC] = self.COND_B/np.sin(GEO.betab)\
                - (self.XC[self.indC] - self.COND_C)/np.sin(GEO.betab)

        # cut the arrays after out of contact
        self.L = np.sum(self.Lh, axis=0)
        self.C1 = self.xx < self.COND_B
        # final x coordinate along path of contact
        self.xf = self.xx[self.C1]/self.COND_B
        self.XF = self.XC[:,self.C1,:]
        # sum of contacting lines
        self.lsum = self.L[self.C1, :]
        # number of lines simultaneously in contact
        self.lxi = self.lsum[:, 0]/GEO.b
        # x coordinate converted into radius
        self.rr1 = ((self.xx*GEO.AE + GEO.T1A)**2 + GEO.rb1**2)**(1/2)
        self.rr2 = ((GEO.T2A - self.xx*GEO.AE)**2 + GEO.rb2**2)**(1/2)
        # dimensional path of contact
        self.xd = self.xf*GEO.AE
        # curvature radius (1 - pinion, 2 - wheel)
        self.R1 = GEO.T1A + self.xd
        self.R2 = GEO.T2A - self.xd
        self.Req = 1/((1/self.R1) + (1/self.R2))/np.cos(GEO.betab)
        # LOAD SHARING ========================================================
        # PEM LOAD SHARING
        def inv(alpha):
            return np.tan(alpha) - alpha
        
        def STIFFNESS(E, v, b, yC, rC, gammaC, alphaC, profile, rsh, rb, rf, rt, z, alpha, ha):
            Cs = 1.2
            G = E/(2*(1+v))
            x = -profile.xLS[profile.yLS<=yC]
            y = profile.yLS[profile.yLS<=yC]
            eY = 2*x
            kPbI = 12/(E*b)*(((yC-y)*np.cos(alphaC)\
                              -rC*np.sin(gammaC)*np.sin(alphaC))**2/eY**3)
            kPsI = Cs/(G*b)*(np.cos(alphaC))**2/eY
            kPcI = 1/(E*b)*(np.sin(alphaC))**2/eY
            ## FOUNDATION
            thetaf = (np.pi/2 + 2*np.tan(alpha)*(ha-rt)+2*rt/np.cos(alpha))/z
            uf = yC - rf
            sf = 2*rb*thetaf
            h = rf/rsh
            L = -5.574e-5/thetaf**2 -1.9986e-3*h**2 -2.3015e-4*h/thetaf\
                + 4.7702e-3/thetaf + 0.0271*h + 6.8045
            M = 60.111e-5/thetaf**2 + 28.100e-3*h**2 -83.431e-4*h/thetaf\
                  -9.9256e-3/thetaf + 0.1624*h + 0.9086
            P = -50.952e-5/thetaf**2 + 185.5e-3*h**2 + 0.0538e-4*h/thetaf\
                  + 53.300e-3/thetaf + 0.2895*h + 0.9236
            Q = -6.2042e-5/thetaf**2 + 9.0889e-3*h**2 -4.0964e-4*h/thetaf\
                + 7.8297e-3/thetaf -0.1472*h + 0.6904
            kPfI = np.cos(alphaC)**2/(E*b)*\
                (L*(uf/sf)**2+M*(uf/sf)+P*(1+Q*(np.tan(alphaC))**2))
            kPtI = kPbI + kPsI + kPcI 
            return np.trapz(kPtI,y) + kPfI

        ## INITIAL
        self.s1 = np.pi*GEO.m/2 + 2*GEO.x1*GEO.m*np.tan(GEO.alpha)
        self.s2 = np.pi*GEO.m/2 + 2*GEO.x2*GEO.m*np.tan(GEO.alpha)

        self.rC1 = np.sqrt((GEO.T1A+self.xd)**2 + GEO.rb1**2)
        self.rC2 = np.sqrt((GEO.T2A-self.xd)**2 + GEO.rb2**2)
        
        self.alphaM1 = np.arccos(GEO.rb1/self.rC1)
        self.alphaM2 = np.arccos(GEO.rb2/self.rC2)
        self.gammaC1 = (self.s1/(GEO.d1) + (inv(GEO.alphat) - inv(self.alphaM1)))
        self.gammaC2 = (self.s2/(GEO.d2) + (inv(GEO.alphat) - inv(self.alphaM2)))
        
        self.alphaC1 = self.alphaM1 - self.gammaC1
        self.alphaC2 = self.alphaM2 - self.gammaC2

        self.yC1 = GEO.rb1/np.cos(self.alphaC1)
        self.yC2 = GEO.rb2/np.cos(self.alphaC2)

        self.kP1 = np.zeros(len(self.rC1))
        self.kP2 = np.zeros(len(self.rC2))

        for j in range(len(self.rC1)):
            self.kP1[j] = STIFFNESS(GMAT.E1,GMAT.v1,GEO.b1,self.yC1[j],
                                    self.rC1[j],self.gammaC1[j],
                                    self.alphaC1[j],Pprofile, GEO.rsh1, GEO.rb1, 
                                    GEO.rf1, GEO.rfP, GEO.z1, GEO.alpha, GEO.haP)
            self.kP2[j] = STIFFNESS(GMAT.E2,GMAT.v2,GEO.b2,self.yC2[j],
                                    self.rC2[j],self.gammaC2[j],
                                    self.alphaC2[j],Wprofile, GEO.rsh2, GEO.rb2, 
                                    GEO.rf2, GEO.rfP, GEO.z2, GEO.alpha, GEO.haP)
        self.Eeq = ((1-GMAT.v1**2)/GMAT.E1 + (1-GMAT.v2**2)/GMAT.E2)**-1
        self.kH = 4/(np.pi*self.Eeq*min(GEO.b1,GEO.b2))
        self.K0 = (self.kP1 + self.kP2)**-1
        self.KA = np.zeros(len(self.K0))
        self.KA[:len(self.K0[self.xd>=GEO.AD])] = self.K0[self.xd>=GEO.AD]
        self.KB = np.zeros(len(self.K0))
        self.KB[(len(self.K0)-len(self.K0[self.xd<=GEO.AB])):] =\
              self.K0[self.xd<=GEO.AB]
        self.KT = self.K0 + self.KA + self.KB
        self.LS = self.K0/(self.K0+self.KB+self.KA)
        self.LS3D = np.tile(self.LS, (len(self.bpos), 1)).T