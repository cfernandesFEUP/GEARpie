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


class OPERATION:
    """Calculation of forces and speeds along the path of contact"""

    def __init__(self, element, torque, speed, GEO, GPATH, ANSWER_LS):
        import numpy as np
        self.element = element
        if element == 'P':
            self.torque1 = torque
            self.torque2 = self.torque1*GEO.u
            self.speed1 = speed
            self.speed2 = self.speed1/GEO.u
            self.omega1 = self.speed1*2*np.pi/60
            self.omega2 = self.speed2*2*np.pi/60

        elif element == 'W':
            self.torque2 = torque
            self.torque1 = self.torque2/GEO.u
            self.speed2 = speed
            self.speed1 = self.speed2*GEO.u
            self.omega1 = self.speed1*2*np.pi/60
            self.omega2 = self.speed2*2*np.pi/60

        elif element == 'F':
            self.torque1 = torque
            self.torque2 = self.torque1*GEO.u
            self.speed2 = speed
            self.speed1 = self.speed2*GEO.u
            self.omega1 = self.speed1*2*np.pi/60
            self.omega2 = self.speed2*2*np.pi/60
            
        # input power
        self.Pin = self.omega1*self.torque1
        # tangential force to pitch circle
        self.ft = 1000*self.torque1/GEO.rl1
        # tangent force to base circle (tranverse plane)
        self.fbt = 1000*self.torque1/GEO.rb1
        # tangent force to base circle (normal plane)
        self.fbn = self.fbt/np.cos(GEO.betab)
        # radial force
        self.fr = self.fbt*np.sin(GEO.alphatw)
        # tangential force (normal plane)
        self.fn = self.ft/np.cos(GEO.betab)
        # axial force
        self.fa = self.fbt*np.tan(GEO.betab)
        # normal force along path of contact
        if ANSWER_LS == 'Y':
            self.fnx = GPATH.LS3D*self.fbn/min(GEO.b1,GEO.b2)
        else:
            self.fnx = self.fbn/GPATH.lsum
        # sum velocity on the pitch circle
        self.vsumc = 2*self.omega1*GEO.rl1/1000*np.sin(GEO.alphatw)
        # tangent speed (base circle)
        self.vtb = self.omega1*GEO.rb1/1000
        # tangential speed
        self.vt = self.omega1*GEO.rl1/1000
        # rolling speed
        self.vr1 = self.omega1*GPATH.R1/(1000*np.cos(GEO.betab))
        self.vr2 = self.omega2*GPATH.R2/(1000*np.cos(GEO.betab))
        # mean rolling speed (contact)
        self.vr = (self.vr1 + self.vr2)/2
        # sliding speed
        self.vg = abs(self.vr1 - self.vr2)
        # specific sliding
        self.gs1 = self.vg/self.vr1
        self.gs2 = self.vg/self.vr2
        # slide-to-roll ratio
        self.SRR = self.vg/self.vr
