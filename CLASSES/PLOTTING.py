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

    def __init__(self, GPATH, GFS, GCONTACT):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(GPATH.xf, GPATH.lxi, 'k')
        plt.xlabel('\u03B6')
        plt.ylabel(r'$L_t\left(x\right)/b$')
        plt.grid(True)
        plt.show()

        plt.figure()
        plt.plot(GPATH.xf, GFS.gs1, 'b', label='pinion')
        plt.plot(GPATH.xf, GFS.gs2, 'r', label='wheel')
        plt.ylabel(r'$v_g\left(x\right)$ / ms$^{-1}$')
        plt.title('Specific Sliding')
        plt.xlabel('\u03B6')
        plt.grid(True)
        plt.legend()
        plt.show()

        plt.figure()
        plt.plot(GPATH.xf, GFS.fnx[:, 0], 'k')
        plt.ylabel(r'$Fn\left(x\right)$ / Nmm$^{-1}$')
        plt.xlabel('\u03B6')
        plt.title('Load per face width')
        plt.grid(True)
        plt.show()
        
        plt.figure()
        plt.plot(GPATH.xf, GCONTACT.fnx_COF, 'k')
        plt.ylabel(r'$Fn\left(x\right)$ / Nmm$^{-1}$')
        plt.xlabel('\u03B6')
        plt.title('Load per face width with friction')
        plt.grid(True)
        plt.show()

        plt.figure()
        plt.plot(GPATH.xf, GFS.vg, 'k')
        plt.ylabel(r'$v_g\left(x\right)$ / ms$^{-1}$')
        plt.title('Sliding Speed')
        plt.xlabel('\u03B6')
        plt.grid(True)
        plt.show()
        
        plt.figure()
        plt.plot(GPATH.xf, GCONTACT.p0[:,0], 'k')
        plt.ylabel(r'$\sigma_H\left(x\right)$ / MPa')
        plt.title('Contact pressure')
        plt.xlabel('\u03B6')
        plt.grid(True)
        plt.show()


        cmap = plt.get_cmap('jet', 21)
        nc = 21
        import numpy as np
        import matplotlib.ticker as tick
        plt.figure()
        plt.title(r'$\sigma_{xx}$ / $p_0$')
        cmin = GCONTACT.SX.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.SX.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.SX.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))
        plt.show()

        plt.figure()
        plt.title(r'$\sigma_{yy}$ / $p_0$')
        cmin = GCONTACT.SY.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.SY.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.SY.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))
        plt.show()

        plt.figure()
        plt.title(r'$\sigma_{zz}$ / $p_0$')
        cmin = GCONTACT.SZ.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.SZ.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.SZ.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))
        plt.show()

        plt.figure()
        plt.title(r'$\tau_{xz}$ / $p_0$')
        cmin = GCONTACT.TXZ.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.TXZ.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.TXZ.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))

        plt.figure()
        plt.title(r'$\tau_{max}$ / $p_0$')
        cmin = GCONTACT.Tmax.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.Tmax.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.Tmax.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))
        plt.show()

        plt.figure()
        plt.title(r'$\tau_{oct}$ / $p_0$')
        cmin = GCONTACT.Toct.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.Toct.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.Toct.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar()
        plt.show()

        plt.figure()
        plt.title(r'$\sigma_{von~Mises}$ / $p_0$')
        cmin = GCONTACT.SMises.min()/GCONTACT.p0[GCONTACT.indS, 0]
        cmax = GCONTACT.SMises.max()/GCONTACT.p0[GCONTACT.indS, 0]
        plt.contourf(GCONTACT.xH[:, 0]/GCONTACT.aHS,
                     GCONTACT.zH[0, :]/GCONTACT.aHS,
                     GCONTACT.SMises.T/GCONTACT.p0[GCONTACT.indS, 0],
                     levels=np.linspace(cmin, cmax, nc), cmap=cmap)
        plt.xlabel('x / b')
        plt.ylabel('z / b')
        plt.grid()
        plt.colorbar(format=tick.FormatStrFormatter('%.2f'))
        plt.show()
        