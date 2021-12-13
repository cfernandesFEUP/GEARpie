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
class GRAPHICS:
    """Creation of graphic output"""
    # from numba import jit
    # @jit(nopython=True)
    def __init__(self, GPATH, GFORCESPEED):
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('GTKAgg')
        plt.figure()
        plt.plot(GPATH.xf, GPATH.lxi, 'k-')
        plt.xlabel('\u03B6')
        plt.ylabel(r'$L_t\left(x\right)/b$')
        plt.grid(True)
        plt.figure()
        plt.plot(GPATH.xf, GFORCESPEED.gs1,'b',label='pinion')
        plt.plot(GPATH.xf, GFORCESPEED.gs2,'r',label='wheel')
        plt.ylabel(r'$v_g\left(x\right)$ / ms$^{-1}$')
        plt.title('Specific Sliding')
        plt.xlabel('\u03B6')
        plt.grid(True)
        plt.legend()
        plt.figure()
        plt.plot(GPATH.xf, GFORCESPEED.fnx/GFORCESPEED.fnx.max(), 'k-')
        plt.xlabel('\u03B6')
        plt.ylabel(r'$\overline{F_N}~\left(x\right)$')
        plt.title('Dimensionless normal load')
        plt.grid(True)
        plt.title('Total contact length over face width')
        plt.figure()
        plt.plot(GPATH.xf, 1e-3*GFORCESPEED.fnx,'k')
        plt.ylabel(r'$Fn\left(x\right)$ / Nmm$^{-1}$')
        plt.xlabel('\u03B6')
        plt.title('Load per face width')
        plt.grid(True)
        plt.figure()
        plt.plot(GPATH.xf, GFORCESPEED.vg,'k')
        plt.ylabel(r'$v_g\left(x\right)$ / ms$^{-1}$')
        plt.title('Sliding Speed')
        plt.xlabel('\u03B6')
        plt.grid(True)
        

        