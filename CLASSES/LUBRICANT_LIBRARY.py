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
    """Library with ISO VG grade lubricants"""

    def __init__(self, BASE_NAME, LUB_GRADE, Tlub):
        import numpy as np
        default = 'No defined lubricant'
        getattr(self, BASE_NAME, lambda: default)()
        getattr(self, BASE_NAME+LUB_GRADE, lambda: default)()
        # lubricant temperature
        self.TL = Tlub
        self.NAME = BASE_NAME+LUB_GRADE
        # density calculation
        self.rho = self.rho0 + self.alphaT*self.rho0*(self.TL - 15)
        # ASTM D341
        self.c = 0.7
        self.niu = -self.c + 10**(10**(self.m - 
                                       self.n*np.log10(self.TL + 273.15)))
        # dynamic viscosity
        self.miu = self.niu*self.rho
        # thermo-viscosity coefficient
        self.beta = (self.n*(self.niu + self.c)*np.log(self.niu + self.c)
                    /(self.niu*(self.TL + 273.15)))
        # piezo-viscosity
        self.piezo = self.s*(self.niu**self.t)*1e-9
        # thermal conductivity
        self.k = 120*(1 - 0.0005*(self.TL)/3)/self.rho

    def M(self):
        self.rho0 = 0.902
        self.alphaT = -5.8e-4
        self.cp = 2306.93
        self.s = 1.390
        self.t = 0.9904
        self.mubl = 0.1
        self.muEHD = 0.02
        self.xl = 0.846
     
    def P(self): 
        self.rho0 = 0.859
        self.alphaT = -5.5e-4
        self.cp = 2306.93
        self.s = 1.360
        self.t = 0.6605
        self.mubl = 0.1
        self.muEHD = 0.02
        self.xl = 0.65
        
    def E(self): 
        self.rho0 = 0.915
        self.alphaT = -8.1e-4
        self.cp = 2306.93
        self.s = 1.335
        self.t = 0.7382
        self.mubl = 0.1
        self.muEHD = 0.02
        self.xl = 0.65
    
    def G(self): 
        self.rho0 = 1.059
        self.alphaT = -7.1e-4
        self.cp = 2306.93
        self.s = 1.485
        self.t = 0.5489
        self.mubl = 0.1
        self.muEHD = 0.02
        self.xl = 0.585
        
    def M320(self):
        self.m = 9.0658
        self.n = 3.4730
        
    def P320(self): 
        self.m = 7.3514
        self.n = 2.7865
    
    def P150(self):
        self.m = 7.646383
        self.n = 2.928541
        
    def E320(self):
        self.m = 7.5823
        self.n = 2.8802
        
    def G320(self):
        self.m = 5.7597
        self.n = 2.1512


