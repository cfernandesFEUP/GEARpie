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


class GEAR:
    """Library with gear geometries and input prompt for new gear geometries"""

    def __init__(self, GEAR_TYPE):

        default = 'No Gear Selected Input'
        getattr(self, GEAR_TYPE, lambda: default)()

    def NEW(self):
        self.GEAR_NAME = input('Gear name: ').upper()
        self.alpha = float(
            input('Pressure angle (default: 20) / \u00b0: ') or '20')
        self.beta = float(input('Helix angle / \u00b0: '))
        self.m = float(input('Gear module / mm: '))
        self.z = [float(input('z1: ')), float(input('z2: '))]
        self.x = [float(input('Pinion profile shift x1: ')),
                  float(input('Wheel profile shift x2: '))]
        self.addendum_reduction = str(input('Calculate addendum reduction factor (Y/N): ')).upper()
        self.b = [float(input('Pinion facewith b1: ')),
                  float(input('Wheel facewith b2: '))]
        self.dshaft = [float(input('Pinion shaft ds1: ')),
                       float(input('Wheel shaft ds2: '))]
        self.al = None
        self.haP = float(input('Addendum coefficient (default: 1): ') or '1')
        self.hfP = float(
            input('Deddendum coefficient (default: 1.25): ') or '1.25')
        self.rfP = float(
            input('Root radius coefficient (default: 0.38): ') or '0.38')
        print('Gear surface finishing:')
        self.Ra = [float(input('Ra1 (default: 0.6) / \u03BCm: ') or '0.6'),
                   float(input('Ra2 (default: 0.6) / \u03BCm: ') or '0.6')]
        self.Rq = [float(input('Rq1 (default: 0.7) / \u03BCm: ') or '0.7'),
                   float(input('Rq2 (default: 0.7) / \u03BCm: ') or '0.7')]
        self.Rz = [float(input('Rz1 (default: 4.8) / \u03BCm: ') or '4.8'),
                   float(input('Rz2 (default: 4.8) / \u03BCm: ') or '4.8')]

    def C14(self):
        self.GEAR_NAME = 'C14'
        self.alpha = 20.0
        self.beta = 0.0
        self.m = 4.5
        self.z = [16, 24]
        self.x = [0.1817, 0.1715]
        self.addendum_reduction = 'N'
        self.b = [14., 14.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        self.Ra = [0.4, 0.31]
        self.Rq = [0.51, 0.4]
        self.Rz = [4.8, 4.8]

    def S30(self):
        self.GEAR_NAME = 'S30'
        self.alpha = 20.0
        self.beta = 0.0
        self.m = 2.0
        self.z = [30, 30]
        self.x = [0.0, 0.0]
        self.addendum_reduction = 'N'
        self.b = [15., 15.]
        self.dshaft = [16., 16.]
        self.al = 60.
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.25
        self.Ra = [0.6, 0.6]
        self.Rq = [0.7, 0.7]
        self.Rz = [4.8, 4.8]

    def H501(self):
        self.GEAR_NAME = 'H501'
        self.alpha = 20.
        self.beta = 15.
        self.m = 3.5
        self.z = [20, 30]
        self.x = [0.1809, 0.0891]
        self.addendum_reduction = 'N'
        self.b = [23., 23.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        self.Ra = [0.6, 0.6]
        self.Rq = [0.7, 0.7]
        self.Rz = [4.8, 4.8]

    def H701(self):
        self.GEAR_NAME = 'H701'
        self.alpha = 20.
        self.beta = 15.
        self.m = 2.5
        self.z = [28, 42]
        self.x = [0.2290, 0.1489]
        self.addendum_reduction = 'N'
        self.b = [17., 17.]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        self.Ra = [0.6, 0.6]
        self.Rq = [0.7, 0.7]
        self.Rz = [4.8, 4.8]

    def H951(self):
        self.GEAR_NAME = 'H951'
        self.alpha = 20.
        self.beta = 15.
        self.m = 1.75
        self.z = [38, 57]
        self.x = [1.6915, 2.0003]
        self.addendum_reduction = 'N'
        self.b = [21.2418, 21.2418]
        self.dshaft = [30., 30.]
        self.al = None
        self.haP = 1.
        self.hfP = 1.25
        self.rfP = 0.38
        self.Ra = [0.6, 0.6]
        self.Rq = [0.7, 0.7]
        self.Rz = [4.8, 4.8]
