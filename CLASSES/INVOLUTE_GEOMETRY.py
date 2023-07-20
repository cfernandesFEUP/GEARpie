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


class LITVIN:
    """Generate the tooth profile of involute gears according to LITVIN"""

    def __init__(self, GEAR_ELEMENT, GEO, DISCRETIZATION):
        import numpy as np
        # assign geometry
        if GEAR_ELEMENT == 'P':
            z = GEO.z1
            rb = GEO.rb1
            ra = GEO.ra1
            rf = GEO.rf1
            r = GEO.r1
            x = GEO.x1
        elif GEAR_ELEMENT == 'W':
            z = GEO.z2
            rb = GEO.rb2
            ra = GEO.ra2
            rf = GEO.rf2
            r = GEO.r2
            x = GEO.x2

        ## RACK POINTS
        self.A = (GEO.hfP*GEO.m - x*GEO.m)*np.tan(GEO.alpha) +\
            GEO.rhoF*(1-np.sin(GEO.alpha))/np.cos(GEO.alpha)
        self.B = GEO.hfP*GEO.m - x*GEO.m - GEO.rhoF

        ## ANGLE FOR THE START OF INVOLUTE (from page 281 Litvin book)
        ## FOR UNDERCUT, MAY NOT WORK
        ## tan(alphaG) = tan(alpha) - 4*(m - x*m)/(z*m*sin(2*alpha))
        self.alphaG = np.arctan(np.tan(GEO.alpha) - 2*(GEO.m-x*GEO.m)/
                               (r*np.sin(2*GEO.alpha)))
                        
        def angleI(phiI):
            res = r*phiI*np.cos(GEO.alpha)*np.sin(phiI+GEO.alpha)+((-r*phiI - self.A)\
            /np.cos(np.arctan(self.B/(-r*phiI-self.A)))+GEO.rhoF)\
                *np.sin(phiI+np.arctan(self.B/(-r*phiI-self.A)))
            return res
        
        from scipy import optimize
        

        ## INVOLUTE PROFILE
        self.alphaA = np.arccos(rb/ra)
        self.phiB = optimize.brentq(angleI,-GEO.alpha,GEO.alpha)
        self.phiE = np.tan(self.alphaA) - np.tan(GEO.alpha)
        self.phi = np.linspace(self.phiB, self.phiE, DISCRETIZATION)
        self.Xinv = r*(np.sin(self.phi) - self.phi*np.cos(GEO.alpha)*
                     np.cos(self.phi+GEO.alpha))
        self.Yinv = r*(np.cos(self.phi) + self.phi*np.cos(GEO.alpha)*
                     np.sin(self.phi+GEO.alpha))

        ## ROOT TROCHOID PROFILE
        self.phiT = np.linspace(-self.A/r, self.phiB, DISCRETIZATION//3)[1::]
        self.lam = np.arctan(self.B/(-r*self.phiT-self.A))
        self.Xtroch = r*np.sin(self.phiT) + ((-r*self.phiT-self.A)/np.cos(self.lam) 
                                         + GEO.rhoF)*np.cos(self.phiT + self.lam)
        self.Ytroch = r*np.cos(self.phiT) - ((-r*self.phiT-self.A)/np.cos(self.lam) + 
                                         GEO.rhoF)*np.sin(self.phiT + self.lam)
        
        ## TRANSFORM MATRIX
        ## TOOTH THICKNESS ON REFERENCE CIRCLE
        self.s = np.pi*GEO.m/2 + 2*x*GEO.m*np.tan(GEO.alpha)
        self.rot = self.s/(2*r) ## HALF ANGLE DUE TO THICKNESS ON REFERENCE CIRCLE
        ## [cos(rot) -sin(rot) 0 ;
        ##  sin(rot)  cos(rot) 0 ;
        ##  0         0        1 ]
            
        self.XinvT = self.Xinv*np.cos(self.rot) - self.Yinv*np.sin(self.rot)
        self.YinvT = self.Xinv*np.sin(self.rot) + self.Yinv*np.cos(self.rot)

        self.XtrochT = self.Xtroch*np.cos(self.rot) - self.Ytroch*np.sin(self.rot)
        self.YtrochT = self.Xtroch*np.sin(self.rot) + self.Ytroch*np.cos(self.rot)

        ## CONCATENATE INVOLUTE AND TROCHOID
        ## YOU NEED TO FIND THE INTERSECTION BETWEEN TROCHOID 
        ## AND DEDDENDUM TO EXCLUDE ALL POINTS ON THE LEFT 
        ## (NOW IS EXCLUDING THE FIRST POINT ONLY, WHICH MAY NOT WORK FOR ALL CASES)
        self.XprofT =  np.concatenate((self.XtrochT, self.XinvT), axis=0)
        self.YprofT =  np.concatenate((self.YtrochT, self.YinvT), axis=0)

        ## ONE TURN DIVIDED BY TOOH
        ## TOOTH ROTATION
        self.aROOT = np.pi/z

        ## DEDDENDUM CIRCLE
        self.Xd = np.linspace(-rf*np.sin(self.aROOT), 
                              self.XprofT[0], DISCRETIZATION//4)
        self.Yd = (rf**2 - self.Xd**2)**(1/2)

        ## ADDENDUM CIRCLE
        self.Xa = np.linspace(self.XprofT[-1], -self.XprofT[-1], 
                              DISCRETIZATION//4)
        self.Ya = (ra**2 - self.Xa**2)**(1/2)

        ## CONCATENATE GEOMETRY
        self.xGEO = np.concatenate((self.Xd, self.XprofT, self.Xa, 
                                    -self.XprofT[::-1], -self.Xd[::-1]), axis=0)
        self.yGEO = np.concatenate((self.Yd, self.YprofT, self.Ya,
                                    self.YprofT[::-1], self.Yd[::-1]), axis=0)
        self.xRF = np.concatenate((self.Xd, self.XtrochT[1::]), axis=0)
        self.yRF = np.concatenate((self.Yd, self.YtrochT[1::]), axis=0)
        self.xLS = np.concatenate((self.Xd, self.XprofT), axis=0)
        self.yLS = np.concatenate((self.Yd, self.YprofT), axis=0)