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

    def __init__(self, size, GEO):

        import numpy as np

        self.size = size

        self.COND_A = GEO.b*np.tan(GEO.betab)

        self.COND_B = GEO.epslon_alpha*GEO.pbt

        self.COND_C = GEO.epslon_beta*GEO.pbt

        self.COND_D = (GEO.epslon_alpha + GEO.epslon_beta)*GEO.pbt

        # X DISCRETIZATION
        self.xx = np.linspace(0., self.COND_D, self.size)

        # FACE WIDTH DISCRETIZATION
        self.DISC_SIZE_AE = self.COND_B/len(self.xx)
        self.DISC_b = int(GEO.b/self.DISC_SIZE_AE)
        self.bpos = np.linspace(0, GEO.b, self.DISC_b)

        # NUMBER OF TOOTH FOR THE ANALYSIS
        self.N = int(np.ceil(GEO.epslon_alpha + GEO.epslon_beta))

        self.kt = np.arange(-self.N, self.N + 1)

        # CREATE VECTORS
        self.XC = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])

        self.Lh = np.zeros([len(self.kt), len(self.xx), len(self.bpos)])

        self.L = np.zeros([len(self.xx), len(self.bpos)])

        # POSITIONS ALONG PLANE OF ACTION
        for i in range(len(self.kt)):
            self.XC[i] = (np.tile(self.xx, (len(self.bpos), 1)).T +
                          self.kt[i]*GEO.pbt +
                          np.tile(self.bpos*np.tan(GEO.betab),
                                  (len(self.xx), 1)))

        # CONDITIONS FOR THE CALCULATION OF LINES IN CONTACT
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

        # CUT THE ARRAYS OVER THE PATH OF CONTACT
        self.L = np.sum(self.Lh, axis=0)

        self.C1 = self.xx < self.COND_B

        self.xf = self.xx[self.C1]/self.COND_B

        self.lsum = self.L[self.C1, :]

        self.lxi = self.lsum[:, 0]/GEO.b

        self.rr1 = ((self.xx*GEO.AE + GEO.T1A)**2 + GEO.rb1**2)**(1/2)

        self.rr2 = ((GEO.T2A - self.xx*GEO.AE)**2 + GEO.rb2**2)**(1/2)

        # DIMENSIONAL PATH CONTACT COORDINATE
        self.xd = self.xf*GEO.AE

        # CURVATURE RADIUS (1 - pinion, 2 - wheel)
        self.R1 = GEO.T1A + self.xd
        self.R2 = GEO.T2A - self.xd
        self.Req = 1/((1/self.R1) + (1/self.R2))/np.cos(GEO.betab)
