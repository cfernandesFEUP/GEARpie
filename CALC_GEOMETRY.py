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
class MAAG:
    """Calculation of cylindrical gear geometry according to MAAG book"""
    # from numba import jit
    # @jit(nopython=True)
    def __init__(self, alpha, beta, m, z, x, b, dshaft, haP, hfP, rfP, al):
        
        import numpy as np
        from scipy import optimize
        
        self.alpha = np.radians(alpha)
    
        self.beta = np.radians(beta)    

        self.m = m
        
        self.z1, self.z2  = z[0], z[1]      

        self.x1, self.x2  = x[0], x[1]   

        self.b1, self.b2 = b[0], b[1]
        
        self.b = min(self.b1, self.b2)
        
        self.dshaft1, self.dshaft2 = dshaft[0], dshaft[1]
        
        self.haP = 1
        
        self.hfP = 1.25
        
        self.rhoF = rfP*self.m
        
        self.al = al

        # transmission ratio
        self.u = self.z2/self.z1
        
        # transverse module
        self.mt = self.m/np.cos(self.beta)
        
        # transverse pressure angle
        self.alphat = np.arctan(np.tan(self.alpha)/np.cos(self.beta))
        
        # base helix angle
        self.betab = np.arcsin(np.sin(self.beta)*np.cos(self.alpha))

        # base pitch          
        self.pb = np.pi*self.m*np.cos(self.alpha)
        
        # transverse pitch
        self.pt = np.pi*self.mt

        # transverse base pitch                         
        self.pbt = self.pt*np.cos(self.alphat)
        
        # reference diameter
        self.d1 = self.mt*self.z1
        self.d2 = self.mt*self.z2
        self.r1 = self.d1/2
        self.r2 = self.d2/2
        
        # base diameter              
        self.db1 = self.d1*np.cos(self.alphat)   
        self.db2 = self.d2*np.cos(self.alphat) 
        self.rb1, self.rb2 = self.db1/2, self.db2/2
        
        # reference center distance
        self.a = (self.d1 + self.d2)/2
        
        # working axis distance
        if self.al:
            self.alphatw = np.arccos(self.a*np.cos(self.alphat)/self.al)
        else:
            # involute working pressure angle
            self.inv_alphatw = np.tan(self.alphat) - self.alphat\
                + (2*np.tan(self.alpha)*(self.x1+self.x2)/(self.z1+self.z2))
        
            def funOPT(xx,inv_a):
                return inv_a - np.tan(xx) + xx 
            self.alphatw = optimize.brentq(funOPT, 0.0, 0.7, \
                                           args=(self.inv_alphatw))
            
            self.al = (self.db1+self.db2)/(2*np.cos(self.alphatw))  
        
        def involute(ang):
            return np.tan(ang) - ang
        
        # working pitch diameter              
        self.dl1 = 2*self.al/(self.u + 1)                                      
        self.dl2 = 2*self.u*self.al/(self.u + 1)
        self.rl1, self.rl2 = self.dl1/2, self.dl2/2
        
        # addendum reduction factor
        self.k = (self.z1+self.z2)/2*(((involute(self.alphatw)\
                - involute(self.alphat))/np.tan(self.alpha)) - \
            1/np.cos(self.beta)*(np.cos(self.alphat)/np.cos(self.alphatw) - 1))
        
        # tip diameter
        self.da1 = self.d1 + 2*self.m*(self.haP + self.x1 - self.k)
        self.da2 = self.d2 + 2*self.m*(self.haP + self.x2 - self.k)  
        
        self.ra1, self.ra2 = self.da1/2, self.da2/2

        # root diameter
        self.df1 = self.d1 + 2*self.m*(self.x1 - self.hfP)
        self.df2 = self.d2 + 2*self.m*(self.x2 - self.hfP)                                  
        self.rf1, self.rf2 = self.df1/2, self.df2/2
        
        # transverse profile angle at tooth tip
        self.alpha_a1 = np.arccos(self.db1/self.da1)
        self.alpha_a2 = np.arccos(self.db2/self.da2)
        
        # addendum contact ratio                 
        self.epslon_a1 = self.z1*(np.tan(self.alpha_a1)\
                                  - np.tan(self.alphatw))/(2*np.pi) 
        self.epslon_a2 = self.z2*(np.tan(self.alpha_a2)\
                                  - np.tan(self.alphatw))/(2*np.pi) 
        
        # transverse contact ratio
        self.epslon_alpha = self.epslon_a1 + self.epslon_a2
        
        # overlap contact ratio
        self.epslon_beta = self.b*np.tan(self.betab)/self.pbt
        
        self.epslon_gama = self.epslon_alpha + self.epslon_beta
       
        # length of path of addendum contact
        self.galpha1 = self.rb1*(np.tan(self.alpha_a1) - np.tan(self.alphatw))       
        self.galpha2 = self.rb2*(np.tan(self.alpha_a2) - np.tan(self.alphatw))
        
        # length of path of contact
        self.galpha = self.galpha1 + self.galpha2
        
        # equivalent curvature radius on pitch point
        self.Req = 1/(1/(self.rl1*np.sin(self.alphatw))\
            + 1/(self.rl2*np.sin(self.alphatw))) 
            
        self.T1T2 = self.al*np.sin(self.alphatw)
        
        # positions along line of action length (wheel)
        self.T2A = (self.ra2**2 - self.rb2**2)**(1/2)
        self.T2B = self.T1T2 - self.T2A - self.pbt
        self.T2C = self.rl2*np.sin(self.alphatw)
        self.T2D = self.T2A - self.pbt
        
        # positions along line of action length (pinion)
        self.T1A = self.T1T2 - self.T2A
        self.T1B = self.T1T2- self.T2A - self.pbt
        self.T1C = self.rl1*np.sin(self.alphatw)
        self.T1D = self.T1T2 - self.T2D
        self.T1E = (self.ra1**2 - self.rb1**2)**(1/2)
        
        # positions along path of contact
        self.AE = self.T1E - self.T1A
        self.AB = self.T1B - self.T1A
        self.AC = self.T1C - self.T1A
        self.AD = self.T1D - self.T1A
        
        # radius along the path of contact
        self.rA1 = (self.T1A**2 + self.rb1**2)**(1/2)
        self.rB1 = (self.T1B**2 + self.rb1**2)**(1/2)
        self.rD1 = (self.T1D**2 + self.rb1**2)**(1/2)
        self.rA2 = ((self.T2A - self.AE)**2 + self.rb2**2)**(1/2)
        self.rB2 = ((self.T2A - self.AD)**2 + self.rb2**2)**(1/2)
        self.rD2 = ((self.T2A - self.AB)**2 + self.rb2**2)**(1/2)
        
        ## GEAR LOSS FACTOR ACCORDING TO OHLENDORF
        self.HV = (1-self.epslon_alpha + self.epslon_a1**2 + self.epslon_a2**2)*\
            np.pi*(self.u+1)/(self.z1*self.u*np.cos(self.betab))