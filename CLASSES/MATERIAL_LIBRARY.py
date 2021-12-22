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


class LIBRARY_MAT:
    """Library with typical gear materials"""

    def __init__(self, MAT_NAME):

        default = 'No defined material'
        getattr(self, MAT_NAME, lambda: default)()

    def Input(self):
        self.E = float(input('Young modulus / MPa: '))
        self.v = float(input('Poisson coeficient: '))
        self.cp = float(input('Heat capacity: '))
        self.k = float(input('Heat conductivity / W/mK: '))
        self.rho = float(input('Density / kg/m3: '))

    def STEEL(self):
        self.E = 206e3
        self.v = 0.3
        self.cp = 465
        self.k = 46
        self.rho = 7830
        self.SigmaHlim = 1500
        self.SigmaFlim = 430

    def ADI(self):
        self.E = 210e3
        self.v = 0.26
        self.cp = 460.548
        self.k = 55
        self.rho = 7850
        self.SigmaHlim = 700
        self.SigmaFlim = 250

    def POM(self):
        self.E = 3.2e3
        self.v = 0.35
        self.cp = 1465
        self.k = 0.3
        self.rho = 1415
        self.SigmaHlim = None
        def SHlimPOM(temp,cycles):
            if temp > 120: temp = 120
            return 36 - 0.0012*temp**2 + (1000 - 0.025*temp**2)*cycles**(-0.21)
        self.SigmaHlim = SHlimPOM
        def SFlimPOM(temp, cycles):
            if temp > 120: temp = 120
            SFL = 26 - 0.0025*temp**2 + 400*cycles**(-0.2)
            return SFL
        self.SigmaFlim = SFlimPOM

    def PA66(self):
        self.E = 1.85e3
        self.v = 0.3
        self.cp = 1670
        self.k = 0.26
        self.rho = 1140
        def SHlimPA66(temp,cycles):
            if temp > 120: temp = 120
            SHL = 36 - 0.0012*temp**2 + (1000 - 0.025*temp**2)*cycles**(-0.21)
            return SHL 
        self.SigmaHlim = SHlimPA66
        def SFlimPA66(temp,cycles):
            if temp > 120: temp = 120
            SFL = 30 - 0.22*temp + (4600 - 900*temp**(0.3))*cycles**(-1/3)
            return SFL
        self.SigmaFlim = SFlimPA66
        
class MATERIAL:
    """Assign a material to pinion and wheel"""

    def __init__(self, PINION_MAT, WHEEL_MAT):

        Pmaterial = LIBRARY_MAT(PINION_MAT)
        self.MAT1 = PINION_MAT 
        self.E1 = Pmaterial.E
        self.v1 = Pmaterial.v
        self.cp1 = Pmaterial.cp
        self.k1 = Pmaterial.k
        self.rho1 = Pmaterial.rho
        self.SigmaHlim1 = Pmaterial.SigmaHlim
        self.SigmaFlim1 = Pmaterial.SigmaFlim
        
        Wmaterial = LIBRARY_MAT(PINION_MAT)
        self.MAT2 = WHEEL_MAT
        self.E2 = Wmaterial.E
        self.v2 = Wmaterial.v
        self.cp2 = Wmaterial.cp
        self.k2 = Wmaterial.k
        self.rho2 = Wmaterial.rho
        self.SigmaHlim2 = Wmaterial.SigmaHlim
        self.SigmaFlim2 = Wmaterial.SigmaFlim