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


class LCC:
    
    
    def __init__(self, xx, AB, AC, AD, AE, T1A, T2A, LS, fbn, fnx, E, v, al, x, m, z, alpha, alpha_tw,
                 r, rl, ra, rb, rf, b, k, rho, cp, vr, Pin, COF, n, Tamb, HVL, HV, PAIR, GB, cofT):

        # IN VDI 2736 is RLG = 1/k3 on page 11, Part 2
        # open gearbox free entry of air:   RLG = 0
        # partially open housing:           RLG = 0.015 to 0.045
        # closed housing:                   RLG 0.06
        if self.GB == 'O':
            self.RLG = 0.0
        elif self.GB == 'C':
            self.RLG = 0.06
        else:
            self.RLG = (0.015+0.045)/2
        self.A2V = 0.03

        if self.PAIR == 'PS':
            # PLASTIC/STEEL
            self.kF = 6300
            self.kR = 895
        else:
            # PLASTIC/PLASTIC
            self.kF = 9000
            self.kR = 2148

        # MESHING POWER LOSS
        self.QFV = self.POWER*self.cof*self.HV

        # GEAR TOOTH TEMPERATURE (FLANK)
        self.TV_F = self.TO + self.QFV * \
            (self.kF/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75) + self.RLG/self.A2V)

        # GEAR TOOTH TEMPERATURE (ROOT)
        self.TV_R = self.TO + self.QFV * \
            (self.kR/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75) + self.RLG/self.A2V)

        self.FV1 = self.kR/(1000*self.b*self.z1*(self.vt*1000*self.m)**0.75)

        self.FV2 = self.RLG/self.A2V

        self.k1 = 10.159

        self.AV = self.k1*self.m*self.z1*self.b

        self.hcV = (1/20)*(self.lambda_air/self.m) * \
            (self.vt*self.m/self.dif_air)**0.75

        self.QCV = (self.TV_R-self.TO)*(self.hcV*self.AV)

        self.ECV = self.QCV*self.t1

        self.QTV = self.QCV/(self.TV_R-self.TO)

# ## PLSTIC AGAINST STEEL ###################################################
# mat = str(mat)
# if mat in 'POM' or mat in 'PA66' or mat in 'PEEK':
#     KH = KA
#     KF = KA
#     ZLUB = ZL * ZV
#     SFmin = 2
#     YdelT[0] = 1
#     YdelT[1] = 1
#     YRrelT = 1
# else:
#     KH = KA * KV * KHB * KHA
#     KF = KA * KV * KFB * KFA
#     ZLUB = ZL * ZV * ZR
#     SFmin = 1.4