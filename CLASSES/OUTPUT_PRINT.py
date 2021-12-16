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


class PRINTING:
    """Print a table with output results"""

    def __init__(self, GEAR_NAME, GTYPE, GMAT, GEO, GFS, GCONTACT):
        dash = '-' * 65
        dots = '.' * 65
        print(dash)
        print('{:^65s}'.format(GEAR_NAME + ' GEAR'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Presure angle \u03B1:', "%.1f" % GTYPE.alpha, '\u00b0'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Helix angle \u03B2:', "%.1f" % GTYPE.beta, '\u00b0'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Module m:', "%.1f" % GTYPE.m, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Number of teeth z1:', "%.1f" % GTYPE.z[0], ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Number of teeth z2:', "%.1f" % GTYPE.z[1], ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Profile shift x1:', "%.4f" % GTYPE.x[0], ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Profile shift x2:', "%.4f" % GTYPE.x[1], ''))
        print(dash)
        print('{:^65s}'.format('GEAR MATERIALS:'))
        print(dots)
        print('Pinion:')
        print('{:<35s}{:^20s}{:<10s}'.format('  Young modulus E1:', "%.0f" %
                                             (GMAT.E1/1e3), 'GPa'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Poisson ratio \u03BD1:', "%.2f" % GMAT.v1, ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal capacity cp1:', "%.2f" % GMAT.cp1, 'J/kg.K'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal conductivity k1:', "%.2f" % GMAT.k1, 'W/m.K'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Density \u03C11:', "%.2f" % GMAT.rho1, 'kg/m3'))
        print('Wheel:')
        print('{:<35s}{:^20s}{:<10s}'.format('  Young modulus E2:', "%.0f" %
                                             (GMAT.E2/1e3), 'GPa'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Poisson ratio \u03BD2:', "%.2f" % GMAT.v2, ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal capacity cp2:', "%.2f" % GMAT.cp2, 'J/kg.K'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal conductivity k2:', "%.2f" % GMAT.k2, 'W/m.K'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Density \u03C12:', "%.2f" % GMAT.rho2, 'kg/m3'))
        print(dash)
        print('{:^65s}'.format('GEAR GEOMETRY:'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Axis distance:', "%.1f" % GEO.al, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base pitch n:', "%.3f" % GEO.pb, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base pitch t:', "%.3f" % GEO.pbt, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('Root radius:', "%.3f" %
                                             GEO.rf1 + ' / ' +
                                             "%.3f" % GEO.rf2, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('Reference radius:', "%.3f" %
                                             GEO.r1 + ' / ' +
                                             "%.3f" % GEO.r2, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('Pitch radius:', "%.3f" %
                                             GEO.rl1 + ' / ' +
                                             "%.3f" % GEO.rl2, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('Tip radius:', "%.3f" %
                                             GEO.ra1 + ' / ' +
                                             "%.3f" % GEO.ra2, 'mm'))
        print(dash)
        print('{:^65s}'.format('CONTACT RATIO:'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Transverse \u03B5\u03B1:', "%.2f" % GEO.epslon_alpha, ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Overlap \u03B5\u03B2:', "%.2f" % GEO.epslon_beta, ''))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Total \u03B5\u03B3:', "%.2f" % GEO.epslon_gama, ''))
        print(dash)
        print('{:^65s}'.format('PATH OF CONTACT:'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format('T1T2:', "%.2f" % GEO.T1T2, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('AB:', "%.2f" % GEO.AB, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('AC:', "%.2f" % GEO.AC, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('AD:', "%.2f" % GEO.AD, 'mm'))
        print('{:<35s}{:^20s}{:<10s}'.format('AE:', "%.2f" % GEO.AE, 'mm'))
        print(dash)
        print('{:^65s}'.format('OPERATING CONDITIONS:'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format('Pin:', "%.1f" % GFS.Pin, 'W'))
        print('{:<35s}{:^20s}{:<10s}'.format('Torque T:', "%.1f" %
                                             GFS.torque1 + ' / ' +
                                             "%.1f" % GFS.torque2, 'N.m'))
        print('{:<35s}{:^20s}{:<10s}'.format('Speed n:', "%.1f" %
                                             GFS.speed1 + ' / ' +
                                             "%.1f" % GFS.speed2, 'rpm'))
        print('{:<35s}{:^20s}{:<10s}'.format('Angular speed \u03C9:', "%.1f" %
                                             GFS.omega1 + ' / ' +
                                             "%.1f" % GFS.omega2, 'rad/s'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Tangential load F_t:', "%.1f" % GFS.ft, 'N'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Radial load F_r:', "%.1f" % GFS.fr, 'N'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Normal load F_n:', "%.1f" % GFS.fn, 'N'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Axial load F_a:', "%.1f" % GFS.fa, 'N'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base circle load F_bt:', "%.1f" % GFS.fbt, 'N'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base circle load F_bn:', "%.1f" % GFS.fbn, 'N'))
        print(dash)
        print('{:^65s}'.format('CONTACT RESULTS:'))
        print(dots)
        print('Maximum pressure p0:')
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  At pitch point:', "%.2f" % GCONTACT.p0I, 'MPa'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:', "%.2f" %
                                             GCONTACT.p0.max(), 'MPa'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:', "%.2f" %
                                             GCONTACT.p0.min(), 'MPa'))
        print('Mean pressure pm:')
        print('{:<35s}{:^20s}{:<10s}'.format('  At pitch point:', "%.2f" %
                                             GCONTACT.pmI, 'MPa'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:', "%.2f" %
                                             GCONTACT.pm.max(), 'MPa'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:', "%.2f" %
                                             GCONTACT.pm.min(), 'MPa'))
        print('Contact half-width aH:')
        print('{:<35s}{:^20s}{:<10s}'.format('  At pitch point:', "%.3f" %
                                             (GCONTACT.aHI*1e3), '\u03BCm'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:', "%.3f" %
                                             (GCONTACT.aH.max()*1e3),
                                             '\u03BCm'))
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:', "%.3f" %
                                             (GCONTACT.aH.min()*1e3),
                                             '\u03BCm'))
        print(dash)
        print('{:^65s}'.format('POWER LOSS:'))
        print(dots)
        print('{:<35s}{:^20s}{:<10s}'.format('Gear Loss Factor HVL:', "%.4f" %
                                             GCONTACT.HVL, 'Wimmer'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Gear Loss Factor HV:', "%.4f" % GEO.HV, 'Ohlendorf'))
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Coefficient of Friction \u03BCmZ:', "%.4f" % GCONTACT.CoF,
            'Schlenk'))
        print('{:<35s}{:^20s}{:<10s}'.format('Average Power Loss Pvzp:',
                                             "%.2f" % GCONTACT.Pvzp, 'W'))
        print('{:<35s}{:^20s}{:<10s}'.format('Maximum Local Power Loss:',
                                             "%.2f" % GCONTACT.PvzpL.max(),
                                             'W'))
        print('{:<35s}{:^20s}{:<10s}'.format('Minimum Local Power Loss:',
                                             "%.2f" % GCONTACT.PvzpL.min(),
                                             'W'))
        print(dash)
        # print('Hertzian Contact Pressure Pitch Point p_0 [GPa]:\n', p0p/1e6)
        # print('Maximum shear stress [MPa]:\n',
        #       np.array([0.3*p0[i, :, :].max()/1e6 for i in range(len(fbn))]))
        # print('Maximum octaedric shear stress [MPa]:\n',
        #       np.array([0.272*p0[i, :, :].max()/1e6 for i in range(len(fbn))]))
        # print('Location of maximum equivalent stress [\u03BCm]:\n',
        #       np.array([0.7861*a[i, :, :].min()*1e6 for i in range(len(fbn))]))
        # print('Oil temperature Tlub [\u00b0C]:', "%.1f" % Tlub)
        # print('Dynamic Viscosity \u03B7 [mPas]:', "%.2f" % miu)
        # print('Kinematic Viscosity \u03BD [cSt]:', "%.2f" % niu)
        # print('Piezoviscosity \u03B1 [1/Pa]:', "%.3f" % piezo)

        #       sigmaHlim[0], '/', sigmaHlim[1])
        # print('Flank Strength \u03C3_{Flim} [MPa]:',
        #       sigmaFlim[0], '/', sigmaFlim[1])
        # np.set_printoptions(precision=1)
