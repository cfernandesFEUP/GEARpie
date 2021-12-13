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
import numpy as np
class LITVIN:
    """Calculation of cylindrical gear geometry according to MAAG book"""
    # from numba import jit
    # @jit(nopython=True)
    def __init__(self, GEAR_ELEMENT, GEO, DISCRETIZATION):
        ## convert to meter
        '''Generate the tooth profile of involute gears according to \n
        LITVIN'''
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
    
        # involute function
        def inv(angles):
            return np.tan(angles) - angles
       
        # tooth rotation
        self.aROOT = np.pi/z
        
        # point A
        self.aA = np.pi*GEO.mt/4 - GEO.m*np.tan(GEO.alphat)-GEO.rhoF*np.cos(GEO.alphat) 
        
        self.bA = 1.25*GEO.m - x*GEO.m - GEO.rhoF  
        
        self.alphaG = np.arctan(np.tan(GEO.alphat) - 4*(GEO.m-x*GEO.m)\
                                /(GEO.mt*z*np.sin(2*GEO.alphat)))
        
        self.rG = r*np.cos(GEO.alphat)/(np.cos(self.alphaG))
        
        # root fillet
        self.thetaR = np.linspace(0, np.pi/2-GEO.alphat, DISCRETIZATION)
        
        self.phi = (self.aA - self.bA*np.tan(self.thetaR))/r
        
        self.xfP = GEO.rhoF*np.sin(self.thetaR - self.phi) +\
            self.aA*np.cos(self.phi) - self.bA*np.sin(self.phi)\
                + r*(np.sin(self.phi) - self.phi*np.cos(self.phi))
        
        self.yfP = -GEO.rhoF*np.cos(self.thetaR - self.phi) -\
            self.aA*np.sin(self.phi) - self.bA*np.cos(self.phi)\
                + r*(np.cos(self.phi) + self.phi*np.sin(self.phi)) 
       
        self.xF = self.xfP*np.cos(self.aROOT) - self.yfP*np.sin(self.aROOT)
        
        self.yF = self.xfP*np.sin(self.aROOT) + self.yfP*np.cos(self.aROOT)
        
        self.rG = (self.xF[-1]**2+self.yF[-1]**2)**(1/2)
        
        # involute profile
        self.thI = np.arccos(rb/self.rG)
        self.thF = np.arccos(rb/ra)
        self.theta = np.linspace(self.thI + inv(self.thI),\
                                 self.thF + inv(self.thF), DISCRETIZATION)
        self.xe = rb*(np.sin(self.theta) - self.theta*np.cos(self.theta))
        self.ye = rb*(np.cos(self.theta) + self.theta*np.sin(self.theta))
        self.aBASE = -np.arctan(self.xF[-1]/self.yF[-1]) + inv(self.thI)
        self.xI = self.xe*np.cos(self.aBASE) - self.ye*np.sin(self.aBASE)
        self.yI = self.xe*np.sin(self.aBASE) + self.ye*np.cos(self.aBASE)
        
        # deddendum circle
        self.xd = np.linspace(-rf*np.sin(self.aROOT), self.xF[0], DISCRETIZATION)
        self.yd = (rf**2 - self.xd**2)**(1/2)
        
        # addendum circle
        self.xa = np.linspace(self.xI[-1], -self.xI[-1], DISCRETIZATION//5)
        self.ya = (ra**2 - self.xa**2)**(1/2)
        
        # concatenate
        self.xGEO = np.concatenate((self.xd, self.xF, self.xI, self.xa,\
                    -self.xI[::-1], -self.xF[::-1], -self.xd[::-1]), axis=0)
        self.yGEO = np.concatenate((self.yd, self.yF, self.yI, self.ya,\
                    self.yI[::-1], self.yF[::-1], self.yd[::-1]), axis=0)
        self.xRF = np.concatenate((self.xd, self.xF), axis=0)
        self.yRF = np.concatenate((self.yd, self.yF), axis=0)
