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


class LUBRICANT:
    def __init__(self, BASE_NAME, LUB_GRADE, Tlub):
        import numpy as np
        default = 'No defined lubricant'
        getattr(self, BASE_NAME+LUB_GRADE, lambda: default)()
        
        self.TL = Tlub
        self.NAME = BASE_NAME+LUB_GRADE
        # density calculation
        self.rho = self.rho0 + self.alphaT*self.rho0*(self.TL - 15) 
        
        # ASTM D341
        self.niu = -self.c + 10**(10**(self.m - 
                                       self.n*np.log10(self.TL + 273.15)))
        self.miu = self.niu*self.rho
        self.beta = (self.n*(self.niu + self.c)*np.log(self.niu + self.c)
                    /(self.niu*(self.TL + 273.15)))
        self.piezo = self.s*(self.niu**self.t)*1e-9
        self.k = 120*(1 - 0.0005*(self.TL)/3)/self.rho

    def M320(self):
        self.m = 9.0658
        self.n = 3.4730
        self.c = 0.7
        self.rho0 = 0.902
        self.alphaT = -5.8e-4
        self.cp = 2306.93
        self.s = 1.390
        self.t = 0.9904
        self.mubl = 0.1
        self.muEHD = 0.02
        self.xl = 0.85


