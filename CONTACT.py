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
    """Calculation of forces and speeds along path of contact"""
    def __init__(self, MAT, LUB, GEO, GPATH, GFSPEED):
        import numpy as np
        
        ## HERTZ ##############################################################
        # effective Young modulus
        self.Eeq = 1/((1 - MAT.v1**2)/MAT.E1 + (1 - MAT.v2**2)/MAT.E2)
        
        # equivalent radius
        self.Req = 1/((1/GPATH.R1) + (1/GPATH.R2))/np.cos(GEO.betab)
        
        # Hertz half-width (a)
        self.aH = (GFSPEED.fnx[:,0]*self.Eeq/(np.pi*self.Req))**(1/2)
        
        # maximum Hertz pressure
        self.p0 = (GFSPEED.fnx[:,0]*self.Eeq/(np.pi*self.Req))**(1/2)
        
        # pitch point maximum Hertz presure
        self.indP = np.argmin(np.abs(GPATH.xd - GEO.AC))
        self.p0I = (GFSPEED.fbn*self.Eeq/(GPATH.lsum[self.indP,0]*\
                                          np.pi*GEO.ReqI))**(1/2)
        
        # mean contact pressure
        self.pm = GFSPEED.fnx[:,0]/(2*self.aH)
        
        # pitch point mean contact pressure
        self.pmI = GFSPEED.fbn/(2*self.aH)
        
        ## POWER LOSS #########################################################
        ## coefficient of friction according to Schlenk
        self.CoF = 0.048*((GFSPEED.fbn/GPATH.lxi.min())/(GFSPEED.vsumc*\
                        GEO.ReqI))**0.2*LUB.miu**(-0.05)*GEO.Ram**0.25*LUB.xl
        
        # mean power loss
        self.Pvzp = GFSPEED.Pin*GFSPEED.HVL*self.CoF
        
        # local power loss
        # self.PvzpL = GFSPEED.fnx*GFSPEED.vg*self.CoF
        
        # # 
        # self.thermal1 = MAT.k1*MAT.rho1*MAT.cp1*GFSPEED.vr1
        
        # self.thermal2 = MAT.k2*MAT.rho2*MAT.cp2*GFSPEED.vr2
        
        # # heat partition factors: 1 - pinion, 2- wheel
        # self.beta1 = self.thermal1/(self.thermal1 + self.thermal2)
        # self.beta2 = self.thermal2/(self.thermal1 + self.thermal2)
        
        # # instantaneous heat generation: 1 - pinion, 2- wheel
        # self.Qvzp1 = self.beta1*GFSPEED.fnx*GFSPEED.vg*self.CoF
        # self.Qvzp2 = self.beta2*GFSPEED.fnx*GFSPEED.vg*self.CoF
        
        # # average heat generation: 1 - pinion, 2- wheel
        # self.Qvzp1m = self.Qvzp1*self.aH/(np.pi*GPATH.R1)
        # self.Qvzp2m = self.Qvzp2*self.aH/(np.pi*GPATH.R2)
        
        ## FILM THICKNESS #####################################################