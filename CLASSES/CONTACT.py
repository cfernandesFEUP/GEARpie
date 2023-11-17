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


class HERTZ:
    """Calculation of contact stresses, power loss and \
    film thickness along path of contact"""

    def __init__(self, GMAT, GLUB, GEO, GPATH, GFS, POSAE):
        import numpy as np
        # tile speeds
        self.vg3D = np.tile(GFS.vg, (len(GPATH.bpos), 1)).T
        self.vr13D = np.tile(GFS.vr1, (len(GPATH.bpos), 1)).T
        self.vr23D = np.tile(GFS.vr2, (len(GPATH.bpos), 1)).T
        self.vr3D = np.tile(GFS.vr, (len(GPATH.bpos), 1)).T
        # HERTZ ===============================================================
        # effective Young modulus
        self.Eeq = 1/((1 - GMAT.v1**2)/GMAT.E1 + (1 - GMAT.v2**2)/GMAT.E2)
        # equivalent radius
        self.R13D = np.tile(GPATH.R1, (len(GPATH.bpos), 1)).T
        self.R23D = np.tile(GPATH.R2, (len(GPATH.bpos), 1)).T
        self.Req = 1/((1/self.R13D) + (1/self.R23D))/np.cos(GEO.betab)
        # pitch point index
        self.indP = np.argmin(np.abs(GPATH.xd - GEO.AC))
        # Hertz half-width (aH)
        self.aH = 2*(GFS.fnx*self.Req/(np.pi*self.Eeq))**(1/2)
        # Hertz half-width at pitch point (aHI)
        self.aHI = self.aH[self.indP, 0]
        # maximum Hertz pressure
        self.p0 = (GFS.fnx*self.Eeq/(np.pi*self.Req))**(1/2)
        # maximum Hertz presure at pitch point 
        self.p0I = (GFS.fbn*self.Eeq/(GPATH.lsum[self.indP, 0] *
                                      np.pi*GEO.ReqI))**(1/2)
        # mean contact pressure
        self.pm = self.p0*np.pi/4
        # mean contact pressure at pitch point
        self.pmI = self.p0I*np.pi/4
        # FILM THICKNESS ======================================================
        if GLUB == None:
            pass
        else:
            # 
            self.L = GLUB.beta*(GLUB.miu/1000)*(self.vr3D**2)/GLUB.k
            # inlet shear heating
            self.phiT = 1/(1 + 0.1*(1 + 14.8*(self.vg3D**0.83))*(self.L**0.64))
            # central film thickness
            self.U = 1e-6*GLUB.miu*self.vr3D/(self.Req*self.Eeq)
            self.G = 1e6*GLUB.piezo*self.Eeq
            self.W = GFS.fnx/(self.Req*self.Eeq)
            self.h0 = 1.95*self.Req*(self.U*self.G)**(8/11)*self.W**(-1/11)
            self.hm = 2.65*self.Req*self.U**(0.7)*self.G**(0.54)*self.W**(-0.13)
            self.h0C = self.phiT*self.h0*1e3
            self.hmC = self.phiT*self.hm*1e3
            self.Lambda0C = self.h0C/GEO.Rrms
            self.LambdamC = self.hmC/GEO.Rrms
        # POWER LOSS ==========================================================
        if GLUB == None:
            # according to VDI 2736
            if GMAT.MAT1 == GMAT.MAT2 == 'POM':
                self.CoF = 0.28
            elif GMAT.MAT1 == GMAT.MAT2 == 'PA66':
                self.CoF = 0.40
            elif GMAT.MAT1 != GMAT.MAT2 and GMAT.MAT1 == ('POM' or 'PA66'):
                self.CoF = 0.18
            elif GMAT.MAT1 != GMAT.MAT2 and\
                GMAT.MAT1 == ('STEEL' or 'POM' or 'PA66'):
                 self.CoF = 0.2
            elif GMAT.MAT1 == GMAT.MAT2 == 'STEEL':
                self.CoF = 0.8
        else:
            # coefficient of friction according to Schlenk
            self.CoF = (0.048 * ((GFS.fbn / (GEO.b*GPATH.lxi.min())) /
                                 (GFS.vsumc * GEO.ReqI))**0.2 *
                        GLUB.miu**(-0.05) * GEO.Ram**0.25 * GLUB.xl)
            # coefficient of friction according to Fernandes
            self.Sp = (GFS.vsumc*GLUB.miu*GLUB.piezo**0.5)/(1000*GFS.fbn**0.5)
            self.Sg = ((GEO.Ram*1e-6)/
                       (1e-6*GEO.b*GPATH.lxi.min()*GEO.ReqI)**(1/2))
            self.CoFF = 0.014*(1/self.Sp)**0.25*self.Sg**0.25*GLUB.xl
            # coefficient of friction according to Matsumoto
            self.DM = GEO.RzS/self.hmC
            self.xiM = 0.5*np.log10(self.DM)
            self.CoFM = self.xiM*GLUB.mubl + (1-self.xiM)*GLUB.muEHD
        # normal force with friction
        self.signVG = (GFS.vr1-GFS.vr2)/abs(GFS.vr1-GFS.vr2)
        self.fnx_COF = GFS.fnx[:, 0]*GEO.rb1/(
            GEO.rb1+(GEO.T1A+GPATH.xf*GEO.epslon_alpha)*self.CoF*self.signVG)
        # numerical gear loss factor according to Wimmer
        self.INTEGRAND = GFS.fnx*self.vg3D/(GFS.fbt*GFS.vtb)
        self.HVL = np.trapz(
            np.trapz(self.INTEGRAND, GPATH.bpos), GPATH.xd)/GEO.pbt
        # average power loss
        self.Pvzp = GFS.Pin*self.HVL*self.CoF
        # local power loss
        self.PvzpL = GFS.fnx*self.vg3D*self.CoF
        #
        self.thermal1 = (GMAT.k1*GMAT.rho1*GMAT.cp1*self.vr13D)**(1/2)
        self.thermal2 = (GMAT.k2*GMAT.rho2*GMAT.cp2*self.vr23D)**(1/2)
        # heat partition factors: 1 - pinion, 2- wheel
        self.beta1 = self.thermal1/(self.thermal1 + self.thermal2)
        self.beta2 = self.thermal2/(self.thermal1 + self.thermal2)
        # instantaneous heat generation: 1 - pinion, 2- wheel
        self.qvzp1 = self.beta1*self.pm*self.vg3D*self.CoF
        self.qvzp2 = self.beta2*self.pm*self.vg3D*self.CoF
        # average heat generation: 1 - pinion, 2- wheel
        self.qvzp1m = self.qvzp1*self.aH/(np.pi*self.R13D)
        self.qvzp2m = self.qvzp2*self.aH/(np.pi*self.R23D)

        self.qvzp1ms = self.beta1*GFS.fnx*self.vg3D*self.CoF/(np.pi*2*self.R13D)
        self.qvzp2ms = self.beta2*GFS.fnx*self.vg3D*self.CoF/(np.pi*2*self.R23D)
        # CONTACT STRESSES ====================================================
        # stress field position along path of contact index
        if POSAE == 'AA':
            self.indS = 0
        else:
            self.indS = np.argmin(np.abs(GPATH.xd - eval('GEO.' + POSAE)))
        # Hertz half-width at desired position
        self.aHS = self.aH[self.indS, 0]
        # create stress field arrays
        self.DISC_X = 150
        self.DISC_Z = 200
        self.xa = np.tile(np.linspace(-1.5, 1.5, self.DISC_X),
                          (self.DISC_Z, 1)).T
        self.za = np.tile(np.linspace(
            0.00001, 2., self.DISC_Z), (self.DISC_X, 1))
        # create x and z arrays
        self.xH = self.xa*self.aHS
        self.zH = self.za*self.aHS
        self.B = 1/self.Req[self.indS, 0]
        self.M = ((self.aHS + self.xH)**2 + self.zH**2)**(1/2)
        self.N = ((self.aHS - self.xH)**2 + self.zH**2)**(1/2)
        self.phi1 = np.pi*(self.M + self.N)/(self.M*self.N *
                                             (2*self.M*self.N + 2 *
                                              self.xH**2 +
                                              2*self.zH**2 -
                                              2*self.aHS**2)**(1/2))
        self.phi2 = np.pi*(self.M - self.N)/(self.M*self.N *
                                             (2*self.M*self.N + 2 *
                                              self.xH**2 +
                                              2*self.zH**2 -
                                              2*self.aHS**2)**(1/2))
        ## stress components
        self.SX = (-self.aHS*self.B*self.Eeq*
                   (self.zH*((self.aHS**2 + 2*self.zH**2 + 2*self.xH**2)* 
                               self.phi1 / self.aHS - 2*np.pi/self.aHS -
                                               3*self.xH*self.phi2)
                    + self.CoF*((2*self.xH**2 - 2*self.aHS**2 - 2*self.zH**2)*
                                self.phi2 + 2*np.pi*self.xH/self.aHS + 
                                2*self.xH*(self.aHS**2 - self.xH**2 - 
                                           self.zH**2)*self.phi1/self.aHS))
                   /np.pi)
        self.SY = (-2*self.aHS*self.B*self.Eeq*GMAT.v1 *
                   (self.zH*((self.aHS**2 + self.zH**2 + self.xH**2) *
                             self.phi1/self.aHS - np.pi/self.aHS -
                             2*self.xH*self.phi2) + self.CoF*
                    ((self.xH**2 - self.aHS**2 - self.zH**2)*self.phi2 + 
                     np.pi*self.xH / self.aHS + self.xH*
                     (self.aHS**2 - self.xH**2 - self.zH**2) * 
                     self.phi1/self.aHS))/np.pi)
        self.SZ = (-self.aHS*self.B*self.Eeq *
                   (self.zH*(self.aHS*self.phi1 - self.xH*self.phi2) +
                    self.CoF*self.zH**2*self.phi2)/np.pi)
        self.TXZ = (-self.aHS*self.B*self.Eeq*
                    (self.zH**2*self.phi2 + self.CoF*
                     ((2*self.xH**2 + self.aHS**2 + 2*self.zH**2)*
                      self.phi1*self.zH / self.aHS - 2*np.pi*self.zH/self.aHS -
                      3*self.xH*self.zH*self.phi2))/np.pi)
        self.Tmax = 0.5*(self.SX-self.SZ)
        self.Toct = ((self.SX-self.SY)**2 + (self.SY-self.SZ) ** 2 +
                     (self.SZ-self.SX)**2)**(1/2)/3
        self.SMises = ((self.SX-self.SY)**2 + (self.SY-self.SZ) ** 2 +
                       (self.SZ-self.SX)**2 + 6*self.TXZ**2)**(1/2)/np.sqrt(2)
