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


class FZG:
    """Selection of FZG load stages"""

    def __init__(self):
        default = 'No defined load stage'
        LOAD_STAGE = str(input('Select load stage (K1, K2, etc): ')).upper()
        ARM = input('Arm lever (0.35 or 0.5): ')
        getattr(self, LOAD_STAGE+'_'+ARM.replace('.',''), lambda: default)()

    # 0.35 m arm
    def K1_035(self):
        self.torque = 3.3
    def K2_035(self):
        self.torque = 13.7
    def K3_035(self):
        self.torque = 28.875
    def K4_035(self):
        self.torque = 46.635
    def K5_035(self):
        self.torque = 69.98
    def K6_035(self):
        self.torque = 98.82
    def K7_035(self):
        self.torque = 132.455
    def K8_035(self):
        self.torque = 171.585
    def K9_035(self):
        self.torque = 215.513
    def K10_035(self):
        self.torque = 265
    def K11_035(self):
        self.torque = 319.18
    def K12_035(self):
        self.torque = 378.26
    def K13_035(self):
        self.torque = 438.8533
    def K14_035(self):
        self.torque = 499.94


   # 0.5 m arm 
    def K1_05(self):
        self.torque = 3.3
    def K2_05(self):
        self.torque = 13.7
    def K3_05(self):
        self.torque = 35.25
    def K4_05(self):
        self.torque = 60.75
    def K5_05(self):
        self.torque = 94.1
    def K6_05(self):
        self.torque = 135.3
    def K7_05(self):
        self.torque = 183.35
    def K8_05(self):
        self.torque = 239.25
    def K9_05(self):
        self.torque = 302
    def K10_05(self):
        self.torque = 372.6
    def K11_05(self):
        self.torque = 450.1
    def K12_05(self):
        self.torque = 534.5
    def K13_05(self):
        self.torque = 626.9333
    def K14_05(self):
        self.torque = 714.2
