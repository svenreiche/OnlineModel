import math


def Types(TM):
    """
    Defines Baugruppen for the layout, common elements without the explicit position or index
    :param TM: TypeManager class
    :return: Nothing
    """

    # define common Undulator
    indict = {'Type': 'Undulator', 'Length': 4, 'K': 1.2, 'ku': 4 * math.asin(1) / 0.015, 'cor': 0,
              'Baugruppe': 'U15'}
    TM.define('U15', indict)
    indict = {'Type': 'Undulator', 'Length': 2, 'K': 1.5, 'ku': 4 * math.asin(1) / 0.04, 'corx': 0, 'cory': 0,
              'Baugruppe': 'UE38'}
    TM.define('UE38', indict)
    indict = {'Type': 'Undulator', 'Length': 0.06, 'Tag': 'UPHS', 'Baugruppe': 'U15-PS'}
    TM.define('PSU15', indict)
    indict = {'Type': 'Undulator', 'Length': 0.20, 'Tag': 'UDLY', 'Baugruppe': 'UE38-DELAY'}
    TM.define('PSUE38', indict)
    indict = {'Type': 'Undulator', 'Length': 0.20, 'K': 25, 'ku': 4 * math.asin(1) / 0.2, 'Tag': 'UMOD',
              'Baugruppe': 'U200'}
    TM.define('UMOD', indict)
    indict = {'Type': 'Undulator', 'Length': 0.4, 'K': 2.27, 'ku': 4 * math.asin(1) / 0.05, 'Baugruppe': 'U50',
              'Power': 20e3, 'Waist': 400e-6}
    TM.define('U50', indict)

    # define common quadrupole38
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'corx': 0, 'cory': 0, 'Baugruppe': 'QFD'}
    TM.define('QFD', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'corx': 0, 'cory': 0, 'Baugruppe': 'QFDM'}
    TM.define('QFDM', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.15, 'corx': 0, 'cory': 0, 'Baugruppe': 'QFDM'}
    TM.define('QFDM-short', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'Baugruppe': 'QFD'}
    TM.define('QFD-noCor', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'Baugruppe': 'QFDM'}
    TM.define('QFDM-noCor', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'Tilt': math.asin(1) / 2, 'Tag': 'MQSK',
              'Baugruppe': 'QFD-SKEW'}
    TM.define('QFS', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'Baugruppe': 'QFA'}
    TM.define('QFA', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.3, 'LengthRes': 0.7, 'Baugruppe': 'QFM'}
    TM.define('QFM', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.3, 'LengthRes': 0.5, 'Baugruppe': 'QFM'}
    TM.define('QFM-short', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.3, 'LengthRes': 0.3, 'Baugruppe': 'QFM'}
    TM.define('QFM-veryshort', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.15, 'LengthRes': 0.25, 'Tilt': math.asin(1) / 2, 'Tag': 'MQSK',
              'Baugruppe': 'QFA-SKEW'}
    TM.define('QFAS', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.08, 'LengthRes': 0.08, 'corx': 0, 'cory': 0, 'Baugruppe': 'QFF'}
    TM.define('QFF', indict)
    #        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.08,'corx':0,'cory':0,'Baugruppe':'QFG'}
    #        TM.define('QFG',indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.04, 'LengthRes': 0.04, 'Tag': 'MQUP', 'Baugruppe': 'QFU',
              'Overlap': 1}
    TM.define('QFU', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.015, 'LengthRes': 0.03, 'Tag': 'MQUP', 'Baugruppe': 'QFUE'}
    TM.define('QFUE', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.08, 'LengthRes': 0.10, 'Baugruppe': 'QFC'}
    TM.define('QFC', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.08, 'LengthRes': 0.10, 'Tilt': math.asin(1) / 2, 'Tag': 'MQSK',
              'Baugruppe': 'QFC-SKEW'}
    TM.define('QFCS', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.08, 'LengthRes': 0.10, 'Baugruppe': 'QFB'}
    TM.define('QFB', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.08, 'LengthRes': 0.10, 'Tilt': math.asin(1) / 2, 'Tag': 'MQSK',
              'Baugruppe': 'QFB-SKEW'}
    TM.define('QFBS', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.16, 'LengthRes': 0.16, 'Baugruppe': 'QFCOR'}
    TM.define('QFCOR', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.16, 'LengthRes': 0.16, 'Tilt': math.asin(1) / 2, 'Tag': 'MQSK',
              'Baugruppe': 'QFCOR-SKEW'}
    TM.define('QFCORS', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.1, 'LengthRes': 0.1, 'Baugruppe': 'QPM1'}
    TM.define('QPM1', indict)
    indict = {'Type': 'Quadrupole', 'Length': 0.1, 'LengthRes': 0.1, 'Baugruppe': 'QPM2'}
    TM.define('QPM2', indict)

    indict = {'Type': 'Sextupole', 'Length': 0.08, 'LengthRes': 0.10, 'Baugruppe': 'HFA'}
    TM.define('HFA', indict)
    indict = {'Type': 'Sextupole', 'Length': 0.08, 'LengthRes': 0.10, 'Baugruppe': 'HFB'}
    TM.define('HFB', indict)

    indict = {'Type': 'Solenoid', 'Length': 0.75, 'Baugruppe': 'WFS'}
    TM.define('WFS', indict)
    indict = {'Type': 'Solenoid', 'Length': 0.03, 'Baugruppe': 'WFB'}
    TM.define('WFB', indict)
    indict = {'Type': 'Solenoid', 'Length': 0.26, 'Baugruppe': 'WFG'}
    TM.define('WFG', indict)

    # define common dipoles
    indict = {'Type': 'Dipole', 'Length': 0.25, 'Baugruppe': 'SHA'}
    TM.define('SHA', indict)
    indict = {'Type': 'Dipole', 'Length': 0.12, 'cor': 0, 'Baugruppe': 'AFL'}
    TM.define('AFL', indict)
    indict = {'Type': 'Dipole', 'Length': 0.25, 'cor': 0, 'Baugruppe': 'AFBC1'}
    TM.define('AFBC1', indict)
    indict = {'Type': 'Dipole', 'Length': 0.5, 'cor': 0, 'Baugruppe': 'AFBC3'}
    TM.define('AFBC3', indict)
    indict = {'Type': 'Dipole', 'Length': 0.5, 'Baugruppe': 'AFBC3'}
    TM.define('AFBC3-noCor', indict)
    indict = {'Type': 'Dipole', 'Length': 0.76, 'Baugruppe': 'AFS'}
    TM.define('AFS', indict)
    indict = {'Type': 'Dipole', 'Length': 0.3, 'cor': 0, 'Baugruppe': 'AFSS'}
    TM.define('AFSS', indict)
    indict = {'Type': 'Dipole', 'Length': 2, 'Tilt': math.asin(1), 'Baugruppe': 'AFD1'}
    TM.define('AFD1', indict)
    indict = {'Type': 'Dipole', 'Length': 1.1, 'Tilt': math.asin(1), 'Baugruppe': 'AFD2'}
    TM.define('AFD2', indict)
    indict = {'Type': 'Dipole', 'Length': 0.3, 'Tag': 'MBNP', 'Baugruppe': 'AFP1'}
    TM.define('AFP1', indict)
    indict = {'Type': 'Dipole', 'Length': 1.0, 'cor': 0, 'Baugruppe': 'AFDL'}
    TM.define('AFDL', indict)
    # new dipole for Porthos
    indict = {'Type': 'Dipole', 'Length': 1., 'cor': 0, 'Baugruppe': 'AFBC4'}
    TM.define('AFBC4', indict)

    # define common correctors
    indict = {'Type': 'Corrector', 'Length': 1, 'Tag': 'MKAC', 'cory': 0, 'Baugruppe': 'RES-KICKER-AC'}
    TM.define('RESKICKAC', indict)
    indict = {'Type': 'Corrector', 'Length': 0.21, 'Tag': 'MKDC', 'cory': 0, 'Baugruppe': 'RES-KICKER-DC'}
    TM.define('RESKICKDC', indict)
    indict = {'Type': 'Corrector', 'Length': 0.05, 'LengthRes': 0.1, 'Tag': 'MCOR', 'corx': 0, 'cory': 0,
              'Baugruppe': 'SFC'}
    TM.define('SFC', indict)
    indict = {'Type': 'Corrector', 'Length': 0.2, 'LengthRes': 0.3, 'Tag': 'MCOR', 'corx': 0, 'cory': 0,
              'Baugruppe': 'SFQFM'}
    TM.define('SFQFM', indict)
    indict = {'Type': 'Corrector', 'Length': 0.2, 'LengthRes': 0.2, 'Tag': 'MCOR', 'corx': 0, 'cory': 0,
              'Baugruppe': 'SFQFM'}
    TM.define('SFQFM-short', indict)
    indict = {'Type': 'Corrector', 'Length': 0.015, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFDD'}
    TM.define('SFDD', indict)
    indict = {'Type': 'Corrector', 'Length': 0.015, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFD1'}
    TM.define('SFD1', indict)
    indict = {'Type': 'Corrector', 'Length': 0.05, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFC'}
    TM.define('SFC', indict)
    indict = {'Type': 'Corrector', 'Length': 0.005, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFB'}
    TM.define('SFB', indict)
    indict = {'Type': 'Corrector', 'Length': 0.06, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFU'}
    TM.define('SFU', indict)
    indict = {'Type': 'Corrector', 'Length': 0.01, 'Tag': 'MCOR', 'corx': 0, 'cory': 0, 'Baugruppe': 'SFUE'}
    TM.define('SFUE', indict)

    # define common RF structure
    indict = {'Type': 'RF', 'Length': 0.2, 'LengthRes': 0.25, 'Band': 'S', 'Tag': 'RGUN', 'Baugruppe': 'PSI-GUN'}
    TM.define('GUN', indict)
    indict = {'Type': 'RF', 'Length': 1.978045, 'LengthRes': 2.05, 'Band': 'C', 'Baugruppe': 'C-BAND-ACC'}
    TM.define('TW Cav C-Band', indict)
    indict = {'Type': 'RF', 'Length': 4.0830, 'LengthRes': 4.15, 'Band': 'S', 'Baugruppe': 'S-BAND-ACC'}
    TM.define('TW Cav S-Band', indict)
    indict = {'Type': 'RF', 'Length': 0.75, 'LengthRes': 0.965, 'Band': 'X', 'Baugruppe': 'X-BAND-ACC'}
    TM.define('TW Cav X-Band', indict)
    indict = {'Type': 'RF', 'Length': 0.240, 'LengthRes': 0.441, 'Band': 'S', 'Tag': 'RTDS',
              'Baugruppe': 'S-BAND-TDS'}
    TM.define('TDS S-Band', indict)
    indict = {'Type': 'RF', 'Length': 1.9, 'LengthRes': 2.0, 'Band': 'C', 'Tag': 'RTDS', 'Baugruppe': 'C-BAND-TDS'}
    TM.define('TDS C-Band', indict)
    indict = {'Type': 'RF', 'Length': 1.20, 'LengthRes': 1.2, 'Band': 'X', 'Tag': 'RTDS', 'Baugruppe': 'X-BAND-TDS'}
    TM.define('TDS X-Band', indict)

    # define diagnostics template
    indict = {'Type': 'Diagnostic', 'Length': 0.10, 'Baugruppe': 'DBPM-C16'}
    TM.define('DBPM-C16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.10, 'Baugruppe': 'DBPM-C8'}
    TM.define('DBPM-C8', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.08, 'Baugruppe': 'DBPM-C5'}
    TM.define('DBPM-C5', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.255, 'Baugruppe': 'DBPM-C38'}
    TM.define('DBPM-C38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-OV16'}
    TM.define('DSCR-OV16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-OV38'}
    TM.define('DSCR-OV38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-HR16'}
    TM.define('DSCR-HR16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-HR16-VO'}
    TM.define('DSCR-HR16-VACONLY', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-HR8'}
    TM.define('DSCR-HR8', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-HR8-TEMP'}
    TM.define('DSCR-HR8-P1-OV16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-HR38'}
    TM.define('DSCR-HR38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Seval': 0.0685, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR',
              'Baugruppe': 'DSCR-LH16'}
    TM.define('DSCR-LH16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-LE16'}
    TM.define('DSCR-LE16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-BC120'}
    TM.define('DSCR-BC120', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-LE38R'}
    TM.define('DSCR-LE38R', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.126, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-LE38'}
    TM.define('DSCR-LE38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.085, 'Tag': 'DHVS', 'Baugruppe': 'DHVS-SLIT'}
    TM.define('DHVS', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DCDR', 'Baugruppe': 'DCDR'}
    TM.define('DCDR', indict)

    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DSRM', 'Baugruppe': 'DSRM-VIS'}
    TM.define('DSRM-VIS', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DSRM', 'Baugruppe': 'DSRM-UV'}
    TM.define('DSRM-UV', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DBCM', 'Baugruppe': 'DBCM-THZ'}
    TM.define('DBCM-THZ', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DBCM', 'Baugruppe': 'DBCM-IR'}
    TM.define('DBCM-IR', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DALA', 'Baugruppe': 'DALA'}
    TM.define('DALA', indict)

    indict = {'Type': 'Diagnostic', 'Length': 0.02, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-LA'}
    TM.define('DSCR-LA', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.02, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DLAC-TARGET'}
    TM.define('DLAC-TARGET', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.02, 'Sx': 1, 'Sy': 1, 'Tag': 'DSCR', 'Baugruppe': 'DCDR-LA'}
    TM.define('DCDR-LA', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DLAC', 'Baugruppe': 'DLAC-LL16'}
    TM.define('DLAC-LL16', indict)

    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DWSC', 'Baugruppe': 'DWSC-C16'}
    TM.define('DWSC-C16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DWSC', 'Baugruppe': 'DWSC-C16-AL'}
    TM.define('DWSC-C16-AL', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.15, 'Sx': 1, 'Sy': 1, 'Tag': 'DWSC', 'Baugruppe': 'DWSC-C38'}
    TM.define('DWSC-C38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Sx': 1, 'Sy': 1, 'Tag': 'DWSC', 'Baugruppe': 'DWSC-C8'}
    TM.define('DWSC-C8', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Sx': 1, 'Sy': 1, 'Tag': 'DWSC', 'Apery': 0,
              'Baugruppe': 'DWSC-C16-COL'}
    TM.define('DWSC-C16-COL', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.075, 'Cx': 0, 'Cy': 0, 'Cz': 1, 'Tag': 'DBAM',
              'Baugruppe': 'DBAM-PS16'}
    TM.define('DBAM-PS16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.075, 'Cx': 0, 'Cy': 0, 'Cz': 1, 'Tag': 'DBAM',
              'Baugruppe': 'DBAM-FS16'}
    TM.define('DBAM-FS16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Cx': 0, 'Cy': 0, 'Cz': 1, 'Tag': 'DBAM',
              'Baugruppe': 'DBAM-FS8'}
    TM.define('DBAM-FS8', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.04, 'Cx': 0, 'Cy': 0, 'Cz': 0, 'Tag': 'DICT',
              'Baugruppe': 'DICT-C16'}
    TM.define('DICT-C16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.04, 'Cx': 0, 'Cy': 0, 'Cz': 0, 'Tag': 'DICT',
              'Baugruppe': 'DICT-C38'}
    TM.define('DICT-C38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.06, 'Cx': 0, 'Cy': 0, 'Cz': 0, 'Tag': 'DICT',
              'Baugruppe': 'DICT-C38-GUN'}
    TM.define('DICT-C38-GUN', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.1, 'Cx': 0, 'Cy': 0, 'Cz': 0, 'Tag': 'DWCM',
              'Baugruppe': 'DWCM-C38'}
    TM.define('DWCM-C38', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.15, 'Cx': 0, 'Cy': 0, 'Sz': 1, 'Tag': 'DTAU', 'Baugruppe': 'DTAU'}
    TM.define('DTAU', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.15, 'Cx': 0, 'Cy': 0, 'Sz': 1, 'Tag': 'DEOM', 'Baugruppe': 'DEOM'}
    TM.define('DEOM', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.126, 'Cx': 0, 'Cy': 0, 'Sz': 1, 'Tag': 'DFCP',
              'Baugruppe': 'DFCP-GUN'}
    TM.define('DFCP', indict)

    # define x-ray diagnostic
    indict = {'Type': 'Photonics', 'Length': 0.15, 'Sx': 1, 'Sy': 1, 'Tag': 'PPRM', 'Baugruppe': 'PPRM'}
    TM.define('PPRM-C38', indict)
    indict = {'Type': 'Photonics', 'Length': 0.15, 'Tag': 'PCRY', 'Baugruppe': 'BRAGG-CRYSTAL'}
    TM.define('PCRY-C38', indict)

    # define aperture templates (moving apertures are part of diagnostics and diagnostics)
    indict = {'Type': 'Diagnostic', 'Length': 0.137, 'Tag': 'DCOL', 'Apery': 0, 'Baugruppe': 'VERT-COL'}
    TM.define('COL-TR-16', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.5, 'Tag': 'VCOL', 'Aperx': 0, 'Baugruppe': 'E-COL'}
    TM.define('COL-Energy', indict)
    indict = {'Type': 'Undulator', 'Length': 1, 'Tag': 'UDCP', 'gap': 20e-3, 'offset': 0, 'Aperx': 0,
              'Baugruppe': 'DECHIRPER-V'}
    TM.define('COL-Dechirper-V', indict)
    indict = {'Type': 'Undulator', 'Length': 1, 'Tag': 'UDCP', 'gap': 20e-3, 'offset': 0, 'Aperx': 0,
              'Baugruppe': 'DECHIRPER-H'}
    TM.define('COL-Dechirper-H', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.01, 'Tag': 'DCOL', 'Aperx': 0, 'Baugruppe': 'BC-SCRAPER'}
    TM.define('COL-BC-Scraper', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.01, 'Tag': 'DSFH', 'Baugruppe': 'SLOT-FOIL-H'}
    TM.define('BC-SlotFoil-H', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.15, 'Tag': 'DSFV', 'Baugruppe': 'SLOT-FOIL-V'}
    TM.define('BC-SlotFoil-V', indict)
    indict = {'Type': 'Vacuum', 'Length': 0.085, 'Tag': 'VLAP', 'Baugruppe': 'LH-LASER-PORT'}
    TM.define('LH-Laserport', indict)
    indict = {'Type': 'Vacuum', 'Length': 0.1, 'Tag': 'VLAP', 'Baugruppe': 'LC-GUN-IN'}
    TM.define('GUN-Laserport', indict)

    # Beam Stopper and Dumps
    indict = {'Type': 'Vacuum', 'Length': 1, 'Tag': 'SDMP', 'Baugruppe': 'BEAM-DUMP-SIN'}
    TM.define('Beam-Dump-Sin', indict)
    indict = {'Type': 'Vacuum', 'Length': 1, 'Tag': 'SDMP', 'Baugruppe': 'BEAM-DUMP-S10'}
    TM.define('Beam-Dump-S10', indict)
    indict = {'Type': 'Vacuum', 'Length': 1, 'Tag': 'SDMP', 'Baugruppe': 'BEAM-DUMP-SAR'}
    TM.define('Beam-Dump-Sar', indict)
    indict = {'Type': 'Vacuum', 'Length': 1, 'Tag': 'SDMP', 'Baugruppe': 'BEAM-DUMP-SAT'}
    TM.define('Beam-Dump-Sat', indict)
    indict = {'Type': 'Vacuum', 'Length': 2.5, 'Tag': 'SSTP', 'Baugruppe': 'BEAM-STOP-SAR'}
    TM.define('Beam-Stopper-Sar', indict)
    indict = {'Type': 'Vacuum', 'Length': 2.5, 'Tag': 'SSTP', 'Baugruppe': 'BEAM-STOP-SAT'}
    TM.define('Beam-Stopper-Sat', indict)
    indict = {'Type': 'Vacuum', 'Length': 1.6, 'Tag': 'SSTP', 'Baugruppe': 'BEAM-STOP-S10'}
    TM.define('Beam-Stopper-S10', indict)
    indict = {'Type': 'Vacuum', 'Length': 1.5, 'Tag': 'SLOS', 'Baugruppe': 'SHIELD-FE'}
    TM.define('FE-Shielding', indict)

    # Laser Acceleration
    indict = {'Type': 'Diagnostic', 'Length': 2.13, 'Tag': 'DLAC', 'Aperx': 0, 'Baugruppe': 'LASER-ACC-BOX'}
    TM.define('Laser-Acceleration', indict)

    # define branching point
    indict = {'Type': 'Marker', 'Length': 0.0, 'Tag': 'MKBR', 'Baugruppe': 'BRANCHING-POINT'}
    TM.define('MKBR', indict)

    # FCC experiment
    indict = {'Type': 'Vacuum', 'Length': 0.1, 'Tag': 'FCRY', 'Baugruppe': 'FCC-Crystal'}
    TM.define('FCC-Crystal', indict)
    indict = {'Type': 'Vacuum', 'Length': 0.1, 'Tag': 'FTAR', 'Baugruppe': 'FCC-Target'}
    TM.define('FCC-Target', indict)
    indict = {'Type': 'Dipole', 'Length': 0.8, 'cor': 0, 'Baugruppe': 'AFSC'}
    TM.define('AFSC', indict)
    indict = {'Type': 'RF', 'Length': 1.2, 'LengthRes': 1.4, 'Band': 'S', 'Baugruppe': 'S-BAND-ACC-FCC'}
    TM.define('FCC-RF-ACC', indict)
    indict = {'Type': 'Solenoid', 'Length': 0.5, 'Baugruppe': 'WFFCC'}
    TM.define('WFFCC', indict)
    indict = {'Type': 'Solenoid', 'Length': 0.02, 'Baugruppe': 'WFAMD'}
    TM.define('WFAMD', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.20, 'Baugruppe': 'DBPM-FCC'}
    TM.define('DBPM-FCC', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.20, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-FCC'}
    TM.define('DSCR-FCC', indict)
    indict = {'Type': 'Diagnostic', 'Length': 0.20, 'Tag': 'DSCR', 'Baugruppe': 'DSCR-SPEC-FCC'}
    TM.define('DSCR-SPEC-FCC', indict)
    indict = {'Type': 'Dipole', 'Length': 0.5, 'Baugruppe': 'SHA-SPEC'}
    TM.define('SHA-FCC', indict)
    indict = {'Type': 'Vacuum', 'Length': 1, 'Tag': 'SDMP', 'Baugruppe': 'BEAM-DUMP-FCC'}
    TM.define('Beam-Dump-FCC', indict)


def Lines(TM):
    """
    Defines common lines for the layout which can be called several times, e.g. a Fodo cell
    :param TM: TypeManager class
    :return: Nothing
    """

    # Aramis
    a0 = {'Length': 4.75}
    a1cor = {'Element': 'SFU', 'sRef': 0.105 + 0.026, 'Ref': 'absolute', 'index': 10,
             'Option': {'MADthin': 1, 'MADshift': -0.02}}
    a1 = {'Element': 'QFU', 'sRef': 0.115, 'Ref': 'absolute', 'index': 20}
    a2 = {'Element': 'U15', 'sRef': 0.0575, 'Ref': 'relative', 'index': 30}
    a3cor = {'Element': 'SFU', 'sRef': 0.0475 - 0.026, 'Ref': 'relative', 'index': 40,
             'Option': {'MADthin': 1, 'MADshift': -0.02}}
    a3 = {'Element': 'QFU', 'sRef': 4.27, 'Ref': 'absolute', 'index': 50}
    a4 = {'Element': 'PSU15', 'sRef': 0.035, 'Ref': 'relative', 'index': 60}
    a5 = {'Element': 'DBPM-C8', 'sRef': 0.078, 'Ref': 'relative', 'index': 70}
    a6 = {'Element': 'QFF', 'sRef': 0.06, 'Ref': 'relative', 'index': 80}
    seq = [a0, a1cor, a1, a2, a3cor, a3, a4, a5, a6]
    TM.define('U15-Cell', seq)
    a5alt = {'Element': 'DBPM-C8', 'sRef': 0.173, 'Ref': 'relative', 'index': 70}
    seq = [a0, a1cor, a1, a2, a3cor, a3, a5alt, a6]
    TM.define('U15-Cell-Last', seq)
    a5alt = {'Element': 'DBPM-C8', 'sRef': 4.483, 'Ref': 'relative', 'index': 70}
    seq = [a0, a5alt, a6]
    TM.define('U15-Cell-Empty', seq)

    # Athos

    a0 = {'Length': 2.8}
    a1 = {'Element': 'QFUE', 'sRef': 0.035, 'Ref': 'relative', 'index': 10}
    a2 = {'Element': 'SFUE', 'sRef': 0.0095, 'Ref': 'relative', 'index': 20}
    a3 = {'Element': 'UE38', 'sRef': 0.038, 'Ref': 'relative', 'index': 30}
    a4 = {'Element': 'SFUE', 'sRef': 0.038, 'Ref': 'relative', 'index': 40}
    a5 = {'Element': 'QFUE', 'sRef': 0.0095, 'Ref': 'relative', 'index': 50}
    a6 = {'Element': 'PSUE38', 'sRef': 0.035 + 0.01, 'Ref': 'relative', 'index': 60}
    a7 = {'Element': 'DBPM-C5', 'sRef': 0.035 - 0.01 + 0.00775, 'Ref': 'relative', 'index': 70}
    a8 = {'Element': 'QFF', 'sRef': 0.06025 - 0.00775 + 0.005, 'Ref': 'relative', 'index': 80}

    seq = [a0, a1, a2, a3, a4, a5, a6, a7, a8]
    TM.define('UE38-Cell', seq)  # normal line
    a7alt = {'Element': 'DBPM-C5', 'sRef': 0.27 + 0.00775, 'Ref': 'relative', 'index': 70}
    seq = [a0, a1, a2, a3, a4, a5, a7alt, a8]
    TM.define('UE38-Cell-Last', seq)  # line without phase shifter
    a6alt = {'Element': 'PSUE38', 'sRef': 2.21 + 0.035 + 0.01, 'Ref': 'relative', 'index': 60}
    seq = [a0, a6alt, a7, a8]
    TM.define('UE38-Cell-PS', seq)  # empty cell with only phase shifter
    a7alt = {'Element': 'DBPM-C5', 'sRef': 2.48 + 0.00775, 'Ref': 'relative', 'index': 70}
    seq = [a0, a7alt, a8]
    TM.define('UE38-Cell-Empty', seq)  # fully empty cell

    a7_400 = {'Element': 'DBPM-C5', 'sRef': 2.48 + 0.00775, 'Ref': 'relative', 'index': 410}
    a8_400 = {'Element': 'QFF', 'sRef': 0.06025 - 0.00775 + 0.005, 'Ref': 'relative', 'index': 420}
    seq = [a0, a7_400, a8_400]
    TM.define('UE38-Cell-Empty-400', seq)  # fully empty cell

    # C-banLinac

    a0 = {'Length': 9.8}
    a1 = {'Element': 'TW Cav C-Band', 'sRef': 0.035, 'Ref': 'relative', 'index': 100}
    a2 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 200}
    a3 = {'Element': 'DBPM-C16', 'sRef': 0.080613, 'Ref': 'relative', 'index': 220}
    a4 = {'Element': 'QFDM', 'sRef': 0.049, 'Ref': 'relative', 'index': 230}
    a5 = {'Element': 'TW Cav C-Band', 'sRef': 0.252075, 'Ref': 'relative', 'index': 300}
    a6 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 400}
    a7 = {'Element': 'DBPM-C16', 'sRef': 0.099538, 'Ref': 'relative', 'index': 420}
    a8 = {'Element': 'QFDM', 'sRef': 0.049, 'Ref': 'relative', 'index': 430}
    a9 = {'Element': 'DWSC-C16', 'sRef': 0.019, 'Ref': 'relative', 'index': 440}
    seq = [a0, a1, a2, a3, a4, a5, a6, a7, a8]
    TM.define('CB-Lin1-Cell', seq)
    seq = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
    TM.define('CB-Lin1-Cell-WSC', seq)
    a0alt = {'Length': 9.135}
    seq = [a0alt, a1, a2, a3, a4, a5, a6]
    TM.define('CB-Lin1-Cell-Last', seq)

    a0 = {'Length': 9.8}
    a1 = {'Element': 'TW Cav C-Band', 'sRef': 0.035, 'Ref': 'relative', 'index': 100}
    a2 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 200}
    a3 = {'Element': 'DBPM-C16', 'sRef': 0.080613, 'Ref': 'relative', 'index': 220}

    a3empty = {'Element': 'DBPM-C16', 'sRef': 4.265, 'Ref': 'relative', 'index': 220}
    a4 = {'Element': 'QFD', 'sRef': 0.049, 'Ref': 'relative', 'index': 230}
    a5 = {'Element': 'COL-TR-16', 'sRef': 0.019, 'Ref': 'relative', 'index': 240}
    a6 = {'Element': 'TW Cav C-Band', 'sRef': 0.096075, 'Ref': 'relative', 'index': 300}
    a7 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 400}
    a8 = {'Element': 'DBPM-C16', 'sRef': 0.099538, 'Ref': 'relative', 'index': 420}
    a8empty = {'Element': 'DBPM-C16', 'sRef': 4.501, 'Ref': 'relative', 'index': 420}
    a9 = {'Element': 'QFD', 'sRef': 0.049, 'Ref': 'relative', 'index': 430}
    a10 = {'Element': 'COL-TR-16', 'sRef': 0.019, 'Ref': 'relative', 'index': 440}
    seq = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]
    TM.define('CB-Athos-Cell', seq)
    seq = [a0, a3empty, a4, a8empty, a9]
    TM.define('CB-Athos-Cell-empty', seq)

    a0 = {'Length': 9.1}
    a1 = {'Element': 'TW Cav C-Band', 'sRef': 0.035, 'Ref': 'relative', 'index': 100}
    a2 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 200}
    a3 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 300}
    a4 = {'Element': 'TW Cav C-Band', 'sRef': 0.049387, 'Ref': 'relative', 'index': 400}
    a5 = {'Element': 'DBPM-C16', 'sRef': 0.081839, 'Ref': 'relative', 'index': 420}
    a6 = {'Element': 'QFD', 'sRef': 0.049, 'Ref': 'relative', 'index': 430}
    a7 = {'Element': 'DWSC-C16', 'sRef': 0.019, 'Ref': 'relative', 'index': 440}

    seq = [a0, a1, a2, a3, a4, a5, a6]
    TM.define('CB-Lin2-Cell', seq)
    seq = [{'Length': 8.435}, a1, a2, a3, a4]
    TM.define('CB-Lin2-Cell-Last', seq)
    seq = [a0, a1, a2, a3, a4, a5, a6, a7]
    TM.define('CB-Lin2-Cell-WSC', seq)

    seq = [a0, a1, a2, a3, a4, a5, a6]
    TM.define('CB-Lin3-Cell-incomplete', seq)

    # s-Band
    a0 = {'Length': 11.0}
    a1 = {'Element': 'TW Cav S-Band', 'sRef': 0.155, 'Ref': 'relative', 'index': 100}
    a2 = {'Element': 'DBPM-C16', 'sRef': 0.835, 'Ref': 'relative', 'index': 120}
    a3 = {'Element': 'QFDM', 'sRef': 0.03, 'Ref': 'relative', 'index': 130}
    a4 = {'Element': 'TW Cav S-Band', 'sRef': 0.135 - 0.0016, 'Ref': 'relative', 'index': 200}
    a5 = {'Element': 'DBPM-C16', 'sRef': 0.835 + 0.0016, 'Ref': 'relative', 'index': 220}
    a6 = {'Element': 'QFDM', 'sRef': 0.03, 'Ref': 'relative', 'index': 230}

    # replaces a3
    a3alt1 = {'Element': 'DSCR-HR16', 'sRef': 0.235, 'Ref': 'relative', 'index': 110}
    a3alt2 = {'Element': 'DBPM-C16', 'sRef': 0.463, 'Ref': 'relative', 'index': 120}
    a3alt3 = {'Element': 'QFDM', 'sRef': 0.03, 'Ref': 'relative', 'index': 130}

    #
    a2alt1 = {'Element': 'DBPM-C16', 'sRef': 0.837 + 4.15 + 0.153, 'Ref': 'relative', 'index': 120}
    a2alt2 = {'Element': 'DBPM-C16', 'sRef': 0.837 + 4.15 + 0.133, 'Ref': 'relative', 'index': 220}

    a0alt = {'Length': 11.6}
    a5alt1 = {'Element': 'DBPM-C16', 'sRef': 0.835 + 0.0016 + 0.57450, 'Ref': 'relative', 'index': 220}

    seq = [a0, a1, a2, a3, a4, a5, a6]
    TM.define('SB-Lin-Cell-Mid', seq)
    seq = [a0, a1, a3alt1, a3alt2, a3alt3, a4, a5, a6]
    TM.define('SB-Lin-Cell-First', seq)
    seq = [a0, a2alt1, a3, a2alt2, a6]
    TM.define('SB-Lin-Cell-Empty', seq)

    seq = [a0alt, a1, a2, a3, a4, a5alt1, a6]
    TM.define('SB-Lin-TMP-DECHIRPER', seq)



