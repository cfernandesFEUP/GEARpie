class MATERIAL:
    def __init__(self, MAT_NAME):

        default = 'No defined material'
        getattr(self, MAT_NAME, lambda: default)()

    def Input(self):
        self.E = float(input('Young modulus / MPa: '))
        self.v = float(input('Poisson coeficient: '))
        self.cp = float(input('Heat capacity: '))
        self.k = float(input('Heat conductivity / W/mK: '))
        self.rho = float(input('Density / kg/m3: '))
        self.SHlim = float(input('Contact fatigue limit / MPa: '))
        self.SFlim = float(input('Bending fatigue limit / MPa: '))

    def STEEL(self):
        self.E = 206e9
        self.v = 0.3
        self.cp = 465
        self.kg = 46 
        self.rho = 7830
        self.SHlim = 1500
        self.SFlim = 430
 
    def ADI(self):
        self.E = 210e9
        self.v = 0.26
        self.cp = 460.548
        self.kg = 55
        self.rho = 7850
        self.SHlim = 1500
        self.SFlim = 430
        
    def POM(self):
        self.E = 3.2e9
        self.v = 0.35
        self.cp = 1465  
        self.k = 0.3
        self.rho = 1415
        self.SHlim = 36 - 0.0012*Tbulk**2 + (1000 - 0.025*Tbulk**2)*NL** - 0.21
        self.SFlim = 26 - 0.0025*Tbulk**2 + 400*NL** - 0.2
    
    def PA66(self):
        self.E = 1.85e9
        self.v = 0.3
        self.cp = 1670
        self.k = 0.26 
        self.rho = 1140
        self.SHlim = 36 - 0.0012*Tbulk**2 + (1000 - 0.025*Tbulk**2)*NL** - 0.21
        self.SFlim = 30 - 0.22*Tbulk + (4600 - 900*Tbulk**0.3)*NL**( - 1/3)
        
    def PEEK(self):
        self.E = 3.65e9
        self.v = 0.38
        self.cp = 1472
        self.k = 0.25
        self.rho = 1320
        self.SHlim = 36 - 0.0012*Tbulk**2 + (1000 - 0.025*Tbulk**2)*NL** - 0.21# Nylon (PA66)
        self.SFlim = 30 - 0.22*Tbulk + (4600 - 900*Tbulk**0.3)*NL**( - 1/3) 