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
    """Create a text report with output results"""

    def __init__(self, GEAR_NAME, GTYPE, GMAT, GLUB, GEO, GFS, GCONTACT, GLCC):

        file = 'REPORT/' + GEAR_NAME + '.txt'
        dash = '-' * 65
        dots = '.' * 65
        # import sys 
        # stdoutOrigin=sys.stdout 
        f = open(file, "w", encoding="utf-8")
        print(dash, file=f)
        # gear type
        print('{:^65s}'.format(GEAR_NAME + ' GEAR'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Presure angle \u03B1:', "%.1f" % GTYPE.alpha, '\u00b0'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Helix angle \u03B2:', "%.1f" % GTYPE.beta, '\u00b0'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Module m:', "%.1f" % GTYPE.m, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Number of teeth z1:', "%.1f" % GTYPE.z[0], ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Number of teeth z2:', "%.1f" % GTYPE.z[1], ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Profile shift x1:', "%.4f" % GTYPE.x[0], ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Profile shift x2:', "%.4f" % GTYPE.x[1], ''), file=f)
        print(dash, file=f)
        # gear materials
        print('{:^65s}'.format('GEAR MATERIALS'), file=f)
        print(dots, file=f)
        print('Pinion:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Young modulus E1:',
                                             "%.0f" % (GMAT.E1/1e3),
                                             'GPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Poisson ratio \u03BD1:', "%.2f" % GMAT.v1, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal capacity cp1:', "%.2f" % GMAT.cp1, 'J/kg.K'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal conductivity k1:', "%.2f" % GMAT.k1, 'W/m.K'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Density \u03C11:', "%.2f" % GMAT.rho1, 'kg/m3'), file=f)
        print('Wheel:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Young modulus E2:',
                                             "%.0f" % (GMAT.E2/1e3),
                                             'GPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Poisson ratio \u03BD2:', "%.2f" % GMAT.v2, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal capacity cp2:', "%.2f" % GMAT.cp2, 'J/kg.K'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Thermal conductivity k2:', "%.2f" % GMAT.k2, 'W/m.K'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Density \u03C12:', "%.2f" % GMAT.rho2, 'kg/m3'), file=f)
        print(dash, file=f)
        # lubricant
        print('{:^65s}'.format(GLUB.NAME+' LUBRICANT'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Lubricant temperature',
                                             "%.0f" % (GLUB.TL),
                                             '\u00b0C'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Kinematic viscosity \u03BD:', "%.2f" % GLUB.niu, 'cSt'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Dynamic viscosity \u03B7:', "%.2f" % GLUB.miu, 'mPa.s'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Piezo-viscosity coefficient \u03B1:', "%.2f" % (GLUB.piezo/1e-9),
            '1/GPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Thermo-viscosity \u03B2:', "%.3f" % GLUB.beta,
            '1/\u00b0C'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Lubricant parameter XL:', "%.2f" % GLUB.xl,
            ''), file=f)
        print(dash, file=f)
        # gear geometry
        print('{:^65s}'.format('GEAR GEOMETRY:'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Axis distance:', "%.1f" % GEO.al, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base pitch n:', "%.3f" % GEO.pb, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base pitch t:', "%.3f" % GEO.pbt, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Root radius:', "%.3f" %
                                             GEO.rf1 + ' / ' +
                                             "%.3f" % GEO.rf2, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Reference radius:', "%.3f" %
                                             GEO.r1 + ' / ' +
                                             "%.3f" % GEO.r2, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Pitch radius:', "%.3f" %
                                             GEO.rl1 + ' / ' +
                                             "%.3f" % GEO.rl2, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Tip radius:', "%.3f" %
                                             GEO.ra1 + ' / ' +
                                             "%.3f" % GEO.ra2, 'mm'), file=f)
        print(dash, file=f)
        # contact ratio
        print('{:^65s}'.format('CONTACT RATIO'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Transverse \u03B5\u03B1:', "%.2f" % GEO.epslon_alpha, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Overlap \u03B5\u03B2:', "%.2f" % GEO.epslon_beta, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Total \u03B5\u03B3:', "%.2f" % GEO.epslon_gama, ''), file=f)
        print(dash, file=f)
        print('{:^65s}'.format('PATH OF CONTACT DIMENSIONS'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'T1T2:', "%.2f" % GEO.T1T2, 'mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('AB:', "%.2f" % GEO.AB, 'mm'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('AC:', "%.2f" % GEO.AC, 'mm'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('AD:', "%.2f" % GEO.AD, 'mm'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('AE:', "%.2f" % GEO.AE, 'mm'), 
              file=f)
        print(dash, file=f)
        # operating conditions
        print('{:^65s}'.format('OPERATING CONDITIONS'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Pin:', "%.1f" % GFS.Pin, 'W'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Torque T:', "%.1f" %
                                             GFS.torque1 + ' / ' +
                                             "%.1f" % GFS.torque2, 'N.m'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Speed n:', "%.1f" %
                                             GFS.speed1 + ' / ' +
                                             "%.1f" % GFS.speed2, 'rpm'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Angular speed \u03C9:',
                                             "%.1f" % GFS.omega1 + ' / ' +
                                             "%.1f" % GFS.omega2, 'rad/s'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Maximum specific sliding gs:', "%.1f" %
                                             GFS.gs1.max() + ' / ' +
                                             "%.1f" % GFS.gs2.max(), ''), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Tangential load F_t:', "%.1f" % GFS.ft, 'N'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Radial load F_r:', "%.1f" % GFS.fr, 'N'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Normal load F_n:', "%.1f" % GFS.fn, 'N'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Axial load F_a:', "%.1f" % GFS.fa, 'N'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base circle load F_bt:', "%.1f" % GFS.fbt, 'N'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Base circle load F_bn:', "%.1f" % GFS.fbn, 'N'), file=f)
        print(dash, file=f)
        # contact results
        print('{:^65s}'.format('CONTACT RESULTS'), file=f)
        print(dots, file=f)
        print('Maximum pressure p0:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  At pitch point:', "%.1f" % GCONTACT.p0I, 'MPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:',
                                             "%.1f" % GCONTACT.p0.max(),
                                             'MPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:',
                                             "%.1f" % GCONTACT.p0.min(),
                                             'MPa'), file=f)
        print('Mean pressure pm:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  At pitch point:', "%.1f" %
                                             GCONTACT.pmI, 'MPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:',
                                             "%.1f" % GCONTACT.pm.max(),
                                             'MPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:',
                                             "%.1f" % GCONTACT.pm.min(),
                                             'MPa'), file=f)
        print('Contact half-width aH:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  At pitch point:',
                                             "%.3f" % (GCONTACT.aHI*1e3),
                                             '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:',
                                             "%.3f" %
                                             (GCONTACT.aH.max()*1e3),
                                             '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:',
                                             "%.3f" %
                                             (GCONTACT.aH.min()*1e3),
                                             '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Maximum von Mises Stress:', "%.1f" % GCONTACT.SMises.max(), 
            'MPa'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Maximum Shear Stress:', "%.1f" % GCONTACT.Tmax.max(), 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Maximum Octahedric Shear Stress:', "%.1f" % GCONTACT.Toct.max(), 
            'MPa'), file=f)
        print(dash, file=f)
        # film thickness
        print('{:^65s}'.format('FILM THICKNESS'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Average Inlet Shear Heating:',
                                             "%.3f" % GCONTACT.phiT.mean(),
                                             ''), file=f)
        print('Central Film Thickness h0C:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:',
                                             "%.2f" % GCONTACT.h0C.max(),
                                             '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:',
                                             "%.2f" % GCONTACT.h0C.min(),
                                             '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Average along AE:',
                                             "%.2f" % GCONTACT.h0C.mean(),
                                             '\u03BCm'), file=f)
        print('Minimum Film Thickness hmC:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Maximum along AE:',
                                     "%.2f" % GCONTACT.hmC.max(),
                                     '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Minimum along AE:',
                                     "%.2f" % GCONTACT.hmC.min(),
                                     '\u03BCm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Average along AE:',
                                     "%.2f" % GCONTACT.hmC.mean(),
                                     '\u03BCm'), file=f)
        print(dash, file=f)
        # power loss
        print('{:^65s}'.format('POWER LOSS'), file=f)
        print(dots, file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Gear Loss Factor HVL:',
                                             "%.4f" %
                                             GCONTACT.HVL, 'Wimmer'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Gear Loss Factor HV:', "%.4f" % GEO.HV, 'Ohlendorf'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Coefficient of Friction \u03BCmZ:', "%.4f" % GCONTACT.CoF,
            'Schlenk'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Coefficient of Friction \u03BCmZ:', "%.4f" % GCONTACT.CoFF,
            'Fernandes'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Coefficient of Friction \u03BCmZ:', "%.4f" % GCONTACT.CoFM.mean(),
            'Matsumoto'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Average Power Loss Pvzp:',
                                             "%.2f" % GCONTACT.Pvzp, 'W'), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Maximum Local Power Loss:',
                                             "%.2f" % GCONTACT.PvzpL.max(),
                                             'W/mm'), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('Minimum Local Power Loss:',
                                             "%.2f" % GCONTACT.PvzpL.min(),
                                             'W/mm'), file=f)
        print(dash, file=f)
        # load carrying capacity
        print('{:^65s}'.format('LOAD CARRYING CAPACITY'), file=f)
        print(dots, file=f)
        print('Influence factors:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Application factor KA: ',
                                             ' %.2f' % GLCC.KA, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Dynamic factor KV: ',
                                             ' %.2f' % GLCC.KV, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Face load factor contact KH\u03B2: ', ' %.2f' % GLCC.KHB,
            ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Face load factor bending KF\u03B2: ', ' %.2f' % GLCC.KFB,
            ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Transverse factor contact KH\u03B1: ', ' %.2f' % GLCC.KHA,
            ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Transverse factor bending KF\u03B1: ', ' %.2f' % GLCC.KFA,
            ''), file=f)
        print('Contact factors:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Elasticity factor ZE: ',
                                             ' %.2f' % GLCC.ZE, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Zone factor ZH: ', 
                                             ' %.2f' % GLCC.ZH, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Contact ratio factor Z\u03b5: '
                                             ,' %.2f' % GLCC.ZEPS, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Helix angle factor Z\u03b2: '
                                             ,' %.2f' % GLCC.ZBETA, ''), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Lubrication factor ZL: '
                                             ,' %.2f' % GLCC.ZL, ''), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Speed factor ZV: '
                                             ,' %.2f' % GLCC.ZV, ''), 
              file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Nominal contact stress: ', ' %.2f' % GLCC.SigmaH0, 'MPa'),
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Contact stress: ', 
            ' %.2f' % GLCC.SigmaH1 + ' / ' + ' %.2f' % GLCC.SigmaH2, 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Permissible contact stress: ', ' %.2f' % GLCC.SigmaHP, 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Contact stress safety factor SH: ', 
            ' %.2f' % GLCC.SH1 + ' / ' + ' %.2f' % GLCC.SH2, ''), 
            file=f)
        print('Bending factors:', file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Form factor YF: ',
                                             ' %.2f' % GLCC.YF1 + ' / ' +
                                             ' %.2f' % GLCC.YF2, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Stress correction factor YS: ',
                                             ' %.2f' % GLCC.YS1 + ' / ' +
                                             ' %.2f' % GLCC.YS2, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format('  Helix angle factor Y\u03b2: '
                                             ,' %.2f' % GLCC.YB, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Notch sensitivity factor Y\u03b4T: ', 
            ' %.2f' % GLCC.YdelT1 + ' / ' + ' %.2f' % GLCC.YdelT2, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            '  Surface factor YRT: ', 
            ' %.2f' % GLCC.YRrelT1 + ' / ' + ' %.2f' % GLCC.YRrelT2, ''), file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Nominal root stress: ', 
            ' %.2f' % GLCC.SigmaF01 + ' / ' + ' %.2f' % GLCC.SigmaF02, 'MPa'),
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Tooth root stress: ', 
            ' %.2f' % GLCC.SigmaF1 + ' / ' + ' %.2f' % GLCC.SigmaF2, 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Limit tooth root stress: ', 
            ' %.2f' % GLCC.SigmaFG1 + ' / ' + ' %.2f' % GLCC.SigmaFG2, 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Permissible tooth root stress: ', 
            ' %.2f' % GLCC.SigmaFP1 + ' / ' + ' %.2f' % GLCC.SigmaFP2, 'MPa'), 
            file=f)
        print('{:<35s}{:^20s}{:<10s}'.format(
            'Tooth root stress safety factor SF: ', 
            ' %.2f' % GLCC.SF1 + ' / ' + ' %.2f' % GLCC.SF2, ''), 
            file=f)
        print(dash, file=f)
        f.close()