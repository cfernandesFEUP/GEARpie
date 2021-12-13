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
    """Calculation of lines of contact length assuming a ridig load sharing"""
    # from numba import jit
    # @jit(nopython=True)
    def __init__(self, size, GEO):
        
        import numpy as np
        
        self.size = size
        
        self.COND_A = GEO.b*np.tan(GEO.betab)
        
        self.COND_B = GEO.epslon_alpha*GEO.pbt
        
        self.COND_C = GEO.epslon_beta*GEO.pbt
        
        self.COND_D = (GEO.epslon_alpha + GEO.epslon_beta)*GEO.pbt
        
        ## X DISCRETIZATION
        self.xx = np.linspace(0., self.COND_D, self.size)
        
        ## FACE WIDTH DISCRETIZATION
        self.bpos = np.linspace(0, GEO.b, len(self.xx))
    
        ## NUMBER OF TOOTH FOR THE ANALYSIS
        self.N = int(np.ceil(GEO.epslon_alpha + GEO.epslon_beta))
        
        self.kt = np.arange(-self.N, self.N + 1)
        
        ## CREATE VECTORS
        self.XC = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])
        
        self.Lh = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])
        
        self.L = np.zeros([len(self.xx), len(self.bpos)])
        
        ## POSITIONS ALONG PLANE OF ACTION
        for i in range(len(self.kt)):
            self.XC[i] = np.meshgrid(np.add(self.xx,self.kt[i]*GEO.pbt),\
                                self.bpos*np.tan(GEO.betab))[0]
        
        ## CONDITIONS FOR THE CALCULATION OF LINES IN CONTACT
        if GEO.epslon_beta < 1:
            self.indA = np.where((self.XC>=0)*(self.XC<self.COND_A))
            self.indB = np.where((self.XC>=self.COND_A)*(self.XC<self.COND_B))
            self.indC = np.where((self.XC>=self.COND_B)*(self.XC<self.COND_D))
            self.Lh[self.indA] = self.XC[self.indA]/np.sin(GEO.betab)
            self.Lh[self.indB] = GEO.b/np.cos(GEO.betab)
            self.Lh[self.indC] = GEO.b/np.cos(GEO.betab)\
                - (self.XC[self.indC] - self.COND_B)/np.sin(GEO.betab)
        else:
            self.indA = np.where((self.XC>=0)*(self.XC<self.COND_B))
            self.indB = np.where((self.XC>=self.COND_B)*(self.XC<self.COND_C))
            self.indC = np.where((self.XC>=self.COND_C)*(self.XC<self.COND_D))
            self.Lh[self.indA] = self.XC[self.indA]/np.sin(GEO.betab)
            self.Lh[self.indB] = self.COND_B/np.sin(GEO.betab)
            self.Lh[self.indC] = self.COND_B/np.sin(GEO.betab)\
                - (self.XC[self.indC] - self.COND_C)/np.sin(GEO.betab)
        
        ## CUT THE ARRAYS OVER THE PATH OF CONTACT
        self.L = np.sum(self.Lh, axis=0)
        
        self.C1 = self.xx < self.COND_B
        
        self.xf = self.xx[self.C1]/self.COND_B
        
        self.lsum = self.L[:, self.C1].T
        
        self.lxi = self.lsum[:,0]/GEO.b
        
        self.rr1 = ((self.xx*GEO.AE + GEO.T1A)**2 + GEO.rb1**2)**(1/2)
        
        self.rr2 = ((GEO.T2A - self.xx*GEO.AE)**2 + GEO.rb2**2)**(1/2)
        
        # curvature radius
        self.R1 = GEO.T1A + self.xf*GEO.AE
        self.R2 = GEO.T2A - self.xf*GEO.AE