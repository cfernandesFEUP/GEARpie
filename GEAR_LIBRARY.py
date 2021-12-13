class GEAR:
    def __init__(self, NAME):

        default = 'No Gear Selected Input'
        getattr(self, NAME, lambda: default)()

    def Input(self):
        self.alpha = float(input('Pressure angle / º: '))
        self.beta = float(input('Helix angle / º: '))
        self.m = float(input('Gear module / mm: '))
        self.z = [float(input('z1: ')), float(input('z2: '))]
        self.x = [float(input('x1: ')), float(input('x2: '))]
        self.b = [float(input('b1: ')), float(input('b2: '))]
        self.dshaft = [float(input('ds1: ')), float(input('ds2: '))]
        self.al = None
        self.haP = float(input('Addednum coefficient: '))
        self.hfP = float(input('Deddednum coefficient: '))
        self.rfP = float(input('Root radius coefficient: '))

    def C14(self):
        self.alpha = 20.0
        self.beta = 0.0
        self.m = 4.5
        self.z = [16, 24]
        self.x = [0.1817, 0.1715]
        self.b = [14., 14.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        
    def H501(self):
        self.alpha = 20.
        self.beta = 15.
        self.m = 4.5
        self.z = [20, 30]
        self.x = [0.1809, 0.0891]
        self.b = [23., 23.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38


    def H701(self):
        self.alpha = 20.
        self.beta = 15.
        self.m = 2.5
        self.z = [28, 42]
        self.x = [0.2290, 0.1489]
        self.b = [17., 17.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        
    def H951(self):
        self.alpha = 20.
        self.beta = 15.
        self.m = 1.75
        self.z = [38, 57]
        self.x = [1.6915, 2.0003]
        self.b = [21.2418, 21.2418]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
 