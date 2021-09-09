import math

import src.OnlineModel.Layout.Macro as Macro

from src.OnlineModel.Core.Type import TypeManager, LineContainer, VariableContainer, Alignment


class Build:
    """
    Class to define the layout of SwissFEL. This class will only be called from the facility container
    """
    def __init__(self, alt=0):
        """
        initialization of the class
        :param alt: integer number to switch between versions of the lattice
                    0 = current
                    1 = planned (near term future)
                    2 = future (long term future)
        """
        self.alt = alt
        self.Version = '10.4.7'


    def build(self):
        """
        function to construct the layout of all branches, first defining commen types and line and then
        assigning position and index numbers. The end is the branching array for the various beamline
        :return: array with all beamlines and branching points
        """
        # initiate the TypeManage
        TM = TypeManager()
        Macro.Types(TM)
        Macro.Lines(TM)

        # -----------------------------------------------
        # define actual layout

        # ---------- short branch for gun dump
        BD01 = LineContainer('BD01', 0)
        BD01.append(TM.generate('DSCR-LE38R', 10), 0.489 + 0.097811, 'relative')
        BD01.append(TM.generate('Beam-Dump-Sin', 15), 0.165 + 0.165 - 0.017, 'relative')

        InjectorDump = LineContainer('IN')
        InjectorDump.append(BD01, 0, 'relative')

        # ---------- elements of injector

        Lsec = 3.6039
        angle = 0  # default angle
        EG01 = LineContainer('EG01', Lsec)
        EG01.append(TM.generate('WFB', 10), 0, 'absolute')
        EG01.append(TM.generate('GUN', 100), 0.1, 'absolute')
        EG01.append(TM.generate('SFB', 120, {'Overlap': 1}), 0.265, 'absolute')
        EG01.append(TM.generate('WFG', 130, {'Overlap': 1}), 0.27, 'absolute')
        EG01.append(TM.generate('QFCOR', 140, {'Overlap': 1}), 0.32, 'absolute')
        EG01.append(TM.generate('QFCORS', 150, {'Overlap': 1}), 0.32, 'absolute')
        EG01.append(TM.generate('SFB', 160, {'Overlap': 1}), 0.054, 'relative')
        EG01.append(TM.generate('DWCM-C38', 170), 0.143, 'relative')
        EG01.append(TM.generate('SFDD', 180), 0.07 - 0.0002, 'relative')
        EG01.append(TM.generate('GUN-Laserport', 185), 0.2397, 'relative')
        EG01.append(TM.generate('DFCP', 185), 0.0, 'relative')
        EG01.append(TM.generate('DSCR-LE38', 190), 0.1445 - 0.126, 'relative')
        EG01.append(TM.generate('SFDD', 200), 1.3725 + 0.0615 - 0.06 + 0.1445, 'absolute')
        EG01.append(TM.generate('DICT-C38-GUN', 210), 0.07 + 0.0375 - 0.064, 'relative')
        EG01.append(TM.generate('QFC', 212), 0.123 - 0.0547, 'relative')
        EG01.append(TM.generate('DICT-C38', 215), 0.4 - 0.055 + 0.062 - 0.0845 - 0.223 + 0.0547, 'relative')
        EG01.append(TM.generate('SFD1', 220), 0.6894 - 0.45 - 0.0425 - 0.0795, 'relative')
        EG01.append(TM.generate('SHA', 300, {'angle': angle, 'design_angle': 30, 'e1': 0.5, 'e2': 0.5, 'branch': True}),
                    0.035, 'relative')
        EG01.append(TM.generate('MKBR', 301), 0.0, 'relative')  # Marker to indicate a branching to Injector beam dump
        #        EG01.append(TM.generate('QFC',310),0.123,'relative')
        EG01.append(TM.generate('QFCS', 320), 0.05 + 0.223, 'relative')
        EG01.append(TM.generate('DHVS', 330), 0.06, 'relative')
        EG01.append(TM.generate('DBPM-C16', 340), 0.2275 - 0.0885 + 0.041, 'relative')
        EG01.append(TM.generate('DSCR-LE16', 350), 0.0455 + 0.013 + 0.0885 - 0.067, 'relative')

        SB01 = LineContainer('SB01', 5 - 0.022)
        SB01.append(TM.generate('SFDD', 10), 0.02, 'relative')
        SB01.append(TM.generate('TW Cav S-Band', 100), 0.025, 'relative')
        SB01.append(TM.generate('WFS', 110, {'Overlap': 1}), 0.41, 'absolute')
        SB01.append(TM.generate('WFS', 120, {'Overlap': 1}), 0.15, 'relative')
        SB01.append(TM.generate('WFS', 130, {'Overlap': 1}), 0.15, 'relative')
        SB01.append(TM.generate('WFS', 140, {'Overlap': 1}), 0.15, 'relative')
        SB01.append(TM.generate('DBPM-C16', 150), 0.582, 'relative')

        SB02 = LineContainer('SB02', 4.59 + 0.032 - 0.0039)
        SB02.append(TM.generate('SFC', 10), 0., 'relative')
        SB02.append(TM.generate('TW Cav S-Band', 100), 0.032, 'relative')
        SB02.append(TM.generate('WFS', 110, {'Overlap': 1}), 0.432, 'absolute')
        SB02.append(TM.generate('WFS', 120, {'Overlap': 1}), 0.15, 'relative')
        SB02.append(TM.generate('WFS', 130, {'Overlap': 1}), 0.15, 'relative')
        SB02.append(TM.generate('WFS', 140, {'Overlap': 1}), 0.15, 'relative')
        SB02.append(TM.generate('DBPM-C16', 150), 0.585, 'relative')

        LH01 = LineContainer('LH01', 2.19)
        LH01.append(TM.generate('DBAM-PS16', 10), 0.099, 'relative')
        LH01.append(TM.generate('QFDM-short', 20), 0.04 + 0.026, 'relative')
        LH01.append(TM.generate('QFCS', 30), 0.1, 'relative')
        LH01.append(TM.generate('QFDM-noCor', 40), 0.05, 'relative')
        LH01.append(TM.generate('QFDM', 50), 0.2, 'relative')
        LH01.append(TM.generate('DBPM-C16', 60), 0.18 - 0.008 - 0.056, 'relative')
        LH01.append(TM.generate('QFDM-noCor', 70), 0.02 + 0.008 + 0.056, 'relative')
        LH01.append(TM.generate('DSCR-OV16', 80), 0.066, 'relative')

        LH02 = LineContainer('LH02', -0.412)
        LH02.append(TM.generate('QFDM', 10), 0.09, 'relative')
        LH02.append(TM.generate('LH-Laserport', 15), 0.033, 'relative')
        varC = VariableContainer(0.16, 0)
        LH02.append(
            TM.generate('AFL', 100, {'angle': -4.1, 'design_angle': -4.1, 'e1': 0, 'e2': 1, 'BC': 'Laser Heater'}),
            0.142, 'relative')
        LH02.append(
            TM.generate('AFL', 200, {'angle': 4.1, 'design_angle': 4.1, 'e1': 1, 'e2': 0, 'BC': 'Laser Heater'}), 2,
            varC)
        LH02.append(TM.generate('DBPM-C16', 210), 0.19, 'relative')
        LH02.append(TM.generate('DSCR-LH16', 220), 0.08, 'relative')
        LH02.append(TM.generate('U50', 230), 0.14 - 0.007, 'relative')
        LH02.append(TM.generate('DBPM-C16', 240), 0.21 - 0.058, 'relative')
        LH02.append(TM.generate('DSCR-LH16', 250), 0.08, 'relative')
        LH02.append(
            TM.generate('AFL', 300, {'angle': 4.1, 'design_angle': 4.1, 'e1': 0, 'e2': 1, 'BC': 'Laser Heater'}), 0.191,
            'relative')
        LH02.append(
            TM.generate('AFL', 400, {'angle': -4.1, 'design_angle': -4.1, 'e1': 1, 'e2': 0, 'BC': 'Laser Heater'}), 2,
            varC)
        LH02.append(TM.generate('LH-Laserport', 405), 0.141, 'relative')
        LH02.append(TM.generate('QFDM', 410), 0.038, 'relative')

        LH03 = LineContainer('LH03', 2.563)
        LH03.append(TM.generate('DBPM-C16', 10), 0., 'relative')
        LH03.append(TM.generate('QFDM', 30), 0.298, 'relative')
        LH03.append(TM.generate('QFDM-noCor', 40), 0.255, 'relative')
        LH03.append(TM.generate('DBPM-C16', 50), 0.155 - 0.062, 'relative')
        LH03.append(TM.generate('QFDM', 60), 0.062, 'relative')
        LH03.append(TM.generate('QFDM-noCor', 80), 0.15 - 0.035 + 0.137 + 0.088, 'relative')
        LH03.append(TM.generate('DBPM-C16', 90), 0.135, 'relative')

        SB03 = TM.generate('SB-Lin-Cell-First', 0, {'Name': 'SB03'})
        SB04 = TM.generate('SB-Lin-Cell-Mid', 0, {'Name': 'SB04'})
        SB05 = TM.generate('SB-Lin-Cell-Empty', 0, {'Name': 'SB05'})

        XB01 = LineContainer('XB01', 5.311)
        XB01.append(TM.generate('TW Cav X-Band', 100), 0.305 - 0.013, 'relative')
        XB01.append(TM.generate('DBPM-C16', 120), 0.2048, 'relative')
        XB01.append(TM.generate('TW Cav X-Band', 200), 0.2048, 'relative')

        BC01 = LineContainer('BC01', 6.615)
        BC01.append(TM.generate('DBPM-C16', 10), 0.12 + 0.08, 'relative')
        BC01.append(TM.generate('QFDM', 20), 0.105 - 0.08, 'relative')
        BC01.append(TM.generate('DBPM-C16', 30), 0.425, 'relative')
        BC01.append(TM.generate('DSCR-OV16', 40), 0.15, 'relative')
        BC01.append(TM.generate('QFDM', 50), 0.240 - 0.027, 'relative')
        BC01.append(TM.generate('DBAM-PS16', 60), 0.749 - 0.075 + 0.175, 'relative')
        BC01.append(TM.generate('QFDM', 70), 0.466 - 0.175, 'relative')
        BC01.append(TM.generate('DBPM-C16', 80), 1.011, 'relative')
        BC01.append(TM.generate('QFDM', 90), 0.189, 'relative')
        BC01.append(TM.generate('DBPM-C16', 100), 0.987, 'relative')
        BC01.append(TM.generate('QFDM', 110), 0.098, 'relative')

        BC02 = LineContainer('BC02', -0.8226)
        varC = VariableContainer(6, 2.655 + 0.0175)
        varD = VariableContainer(6, 3.601 + 0.0175 + 0.306)
        BC02.append(TM.generate('AFBC1', 100,
                                {'angle': -3.82, 'design_angle': -3.82, 'e1': 0, 'e2': 1, 'BC': 'Bunch Compressor 1'}),
                    0., 'relative')
        BC02.append(TM.generate('QFBS', 110), 1.8, 'relative')
        BC02.append(TM.generate('QFB', 120), 0.1, 'relative')
        BC02.append(TM.generate('HFA', 130), 0.1, 'relative')
        BC02.append(TM.generate('DBPM-C38', 140), 0.1 + 0.0175, 'relative')
        BC02.append(TM.generate('AFBC1', 200,
                                {'angle': 3.82, 'design_angle': 3.82, 'e1': 1, 'e2': 0, 'BC': 'Bunch Compressor 1'}), 0,
                    varC)
        BC02.append(TM.generate('COL-BC-Scraper', 210), 0.29, 'relative')
        BC02.append(TM.generate('DSCR-BC120', 220), 0.025, 'relative')
        BC02.append(TM.generate('AFBC1', 300,
                                {'angle': 3.82, 'design_angle': 3.82, 'e1': 0, 'e2': 1, 'BC': 'Bunch Compressor 1'}),
                    0.325, 'relative')
        BC02.append(TM.generate('DSRM-VIS', 310), 0.846 + 0.306, 'relative')
        BC02.append(TM.generate('DBPM-C38', 320), 0, varD)
        BC02.append(TM.generate('HFA', 330), 0.1 + 0.0175, 'relative')
        BC02.append(TM.generate('QFB', 340), 0.1, 'relative')
        BC02.append(TM.generate('QFAS', 350), 0.09, 'relative')
        BC02.append(TM.generate('DALA', 360), 1.214 - 0.0385, 'relative')
        BC02.append(TM.generate('AFBC1', 400,
                                {'angle': -3.82, 'design_angle': -3.82, 'e1': 1, 'e2': 0, 'BC': 'Bunch Compressor 1'}),
                    1.56 - 1.214 + 0.0385 - 0.037, 'relative')
        BC02.append(TM.generate('DBCM-THZ', 410), 0.4274, 'relative')

        DI01 = LineContainer('DI01', 3.84)
        DI01.append(TM.generate('DBPM-C16', 10), 0.263, 'relative')
        DI01.append(TM.generate('QFDM', 20), 0.037, 'relative')
        DI01.append(TM.generate('QFBS', 30), 0.27, 'relative')
        DI01.append(TM.generate('DBPM-C16', 60), 0.109 + 0.012 + 0.4 + 0.137, 'relative')
        DI01.append(TM.generate('QFDM', 70), 0.03 - 0.008, 'relative')
        DI01.append(TM.generate('DWSC-C16-AL', 90), 0.167 - 0.022 + 0.005 + 0.137 + 0.022 + 0.061, 'relative')
        DI01.append(TM.generate('TDS S-Band', 100), 0.346, 'relative')

        DI02 = LineContainer('DI02', 5.456)
        DI02.append(TM.generate('DBPM-C16', 10), 0.366 + 0.037, 'relative')
        DI02.append(TM.generate('QFDM', 20), 0.09 - 0.037, 'relative')
        DI02.append(TM.generate('QFDM', 30), 0.9, 'relative')
        DI02.append(TM.generate('DBPM-C16', 40), 0.756, 'relative')
        DI02.append(TM.generate('QFDM', 50), 0.044, 'relative')
        DI02.append(TM.generate('DLAC-LL16', 55), 0.363 - 0.091, 'relative')
        DI02.append(TM.generate('QFDM', 60), 0.4 + 0.091, 'relative')
        DI02.append(TM.generate('DCDR', 65), 0.263, 'relative')
        DI02.append(TM.generate('DSCR-OV16', 75), 0.09 - 0.137 + 0.1 + 0.047, 'relative')
        DI02.append(TM.generate('DBPM-C16', 80), 0.11 - 0.047 + 0.037, 'relative')
        DI02.append(TM.generate('QFDM', 90), 0.11 - 0.037, 'relative')

        InjLine = [EG01, SB01, SB02, LH01, LH02, LH03, SB03, SB04, SB05, XB01, BC01, BC02, DI01, DI02]
        Injector = LineContainer('IN')
        Injector.append(InjLine)

        # ------------------------------------------------------
        # ----- Insertion of short Linac beam dump
        BD01 = LineContainer('BD01', 0)
        BD01.append(TM.generate('QFA', 10), 1.1, 'relative')
        BD01.append(TM.generate('DBPM-C38', 20), 0.4, 'relative')
        BD01.append(TM.generate('DSCR-HR38', 30), 0.15, 'relative')
        BD01.append(TM.generate('Beam-Dump-S10', 35), 3.8115, 'relative')
        Linac1Dump = LineContainer('10')
        Linac1Dump.append(BD01, 0, 'relative')

        # -----------------------------------------------------
        # Linac 1

        CB01 = TM.generate('CB-Lin1-Cell', 0, {'Name': 'CB01'})
        CB02 = TM.generate('CB-Lin1-Cell', 0, {'Name': 'CB02'})

        angle = 0
        Lcell = 4.9
        DI01 = LineContainer('DI01', Lcell)
        DI01.append(TM.generate('DWSC-C16', 10), 0.094, 'relative')
        DI01.append(TM.generate('DSCR-HR16', 20), 0.12, 'relative')
        DI01.append(TM.generate('DICT-C16', 25), 0.0675, 'relative')
        DI01.append(TM.generate('QFDM-noCor', 30), 0.03 - 0.0005, 'relative')
        DI01.append(
            TM.generate('AFDL', 100, {'angle': angle, 'design_angle': -20, 'e1': 0.5, 'e2': 0.5, 'branch': True}),
            0.303, 'relative')
        DI01.append(TM.generate('MKBR', 101), 0.0, 'relative')
        DI01.append(TM.generate('DBPM-C16', 110), 2.09 - 0.003, 'relative')
        DI01.append(TM.generate('QFDM', 120), 0.049, 'relative')

        CB03 = TM.generate('CB-Lin1-Cell-WSC', 0, {'Name': 'CB03'})
        CB04 = TM.generate('CB-Lin1-Cell', 0, {'Name': 'CB04'})
        CB05 = TM.generate('CB-Lin1-Cell-WSC', 0, {'Name': 'CB05'})
        CB06 = TM.generate('CB-Lin1-Cell', 0, {'Name': 'CB06'})
        CB07 = TM.generate('CB-Lin1-Cell-WSC', 0, {'Name': 'CB07'})
        CB08 = TM.generate('CB-Lin1-Cell', 0, {'Name': 'CB08'})
        CB09 = TM.generate('CB-Lin1-Cell-Last', 0, {'Name': 'CB09'})

        BC01 = LineContainer('BC01', 9.665)
        BC01.append(TM.generate('DBPM-C16', 10), 0.03, 'relative')
        BC01.append(TM.generate('QFDM', 20), 0.049, 'relative')
        BC01.append(TM.generate('DWSC-C16-AL', 30), 0.019, 'relative')
        BC01.append(TM.generate('QFDM', 40), 1.08, 'relative')
        BC01.append(TM.generate('DBPM-C16', 50), 2.351, 'relative')
        BC01.append(TM.generate('QFDM', 60), 0.049, 'relative')
        BC01.append(TM.generate('DBAM-FS16', 70), 0.839, 'relative')
        BC01.append(TM.generate('QFDM', 80), 1.586, 'relative')
        BC01.append(TM.generate('DBPM-C16', 90), 1.305, 'relative')
        BC01.append(TM.generate('QFDM', 100), 0.095, 'relative')

        BC02 = LineContainer('BC02', -0.521)
        #        varC=VariableContainer(7,3.15+0.1+0.72+0.037)
        varC = VariableContainer(7, 3.15)
        varD = VariableContainer(7, 4.2761 + 0.357 - 0.661)
        BC02.append(TM.generate('AFBC3', 100,
                                {'angle': -2.15, 'design_angle': -2.15, 'e1': 0, 'e2': 1, 'BC': 'Bunch Compressor 2'}),
                    0., 'relative')
        BC02.append(TM.generate('QFBS', 110), 2.45, 'relative')
        BC02.append(TM.generate('QFB', 120), 0.1, 'relative')
        BC02.append(TM.generate('HFB', 130), 0.09, 'relative')
        BC02.append(TM.generate('DBPM-C16', 140), 0.11, 'relative')
        #        BC02.append(TM.generate('DALA',150),0,varC)
        #        BC02.append(TM.generate('AFBC3',200,{'angle':2.15,'design_angle':2.15,'e1':1,'e2':0,'BC':'Bunch Compressor 2'}),0.720,'relative')
        #        BC02.append(TM.generate('DALA',150),0,varC)
        BC02.append(TM.generate('AFBC3', 200,
                                {'angle': 2.15, 'design_angle': 2.15, 'e1': 1, 'e2': 0, 'BC': 'Bunch Compressor 2'}), 0,
                    varC)
        BC02.append(TM.generate('COL-BC-Scraper', 210), 0.3005, 'relative')
        BC02.append(TM.generate('DSCR-BC120', 220), 0.0395, 'relative')
        BC02.append(TM.generate('BC-SlotFoil-H', 230), 0.0395, 'relative')
        BC02.append(TM.generate('BC-SlotFoil-V', 240), 0.0405, 'relative')
        BC02.append(TM.generate('AFBC3', 300,
                                {'angle': 2.15, 'design_angle': 2.15, 'e1': 0, 'e2': 1, 'BC': 'Bunch Compressor 2'}),
                    0.26, 'relative')
        BC02.append(TM.generate('DSRM-VIS', 310), 1.0261 + 0.357 - 0.661, 'relative')
        BC02.append(TM.generate('DBPM-C16', 320), 0, varD)
        BC02.append(TM.generate('HFB', 330), 0.11, 'relative')
        BC02.append(TM.generate('QFB', 340), 0.09, 'relative')
        BC02.append(TM.generate('QFS', 350), 0.05, 'relative')
        BC02.append(TM.generate('DALA', 360), 1.922 - 0.019, 'relative')
        BC02.append(TM.generate('AFBC3', 400,
                                {'angle': -2.15, 'design_angle': -2.15, 'e1': 1, 'e2': 0, 'BC': 'Bunch Compressor 2'}),
                    2.25 - 1.922 + 0.019 - 0.037, 'relative')
        BC02.append(TM.generate('DBCM-IR', 410), 0.4 - 0.021, 'relative')

        Lsec = 9.43
        angle = 0
        MA01 = LineContainer('MA01', Lsec)
        MA01.append(TM.generate('DBPM-C16', 10), 0.104, 'relative')
        MA01.append(TM.generate('QFDM', 20), 0.1 - 0.004, 'relative')
        #        MA01.append(TM.generate('DCDR-VACONLY',25),1.38-0.137,'relative')
        MA01.append(TM.generate('QFDM', 50), 0.05 + 0.15 + 0.12 + 1.480 + 0.05, 'relative')
        MA01.append(TM.generate('DBPM-C16', 60), 1.82, 'relative')
        MA01.append(TM.generate('QFDM', 70), 0.08, 'relative')
        MA01.append(TM.generate('DCDR', 80), 1.008 - 0.312 - 0.037, 'relative')
        MA01.append(TM.generate('DSCR-HR16', 90), 0.2, 'relative')
        MA01.append(TM.generate('AFBC1', 100, {'angle': 0, 'design_angle': 0, 'e1': 0, 'e2': 1}),
                    0.16 + 0.025 + 0.05 + 0.3 - 0.043, 'relative')
        MA01.append(TM.generate('QFDM', 110), 0.10 - 0.025, 'relative')
        MA01.append(TM.generate('Beam-Stopper-S10', 115), 0.15, 'relative')
        MA01.append(TM.generate('DBPM-C16', 120), 0.13 - 0.05, 'relative')
        MA01.append(TM.generate('QFDM', 130), 0.07, 'relative')

        L1Line = [CB01, CB02, DI01, CB03, CB04, CB05, CB06, CB07, CB08, CB09, BC01, BC02, MA01]
        Linac10 = LineContainer('10')
        Linac10.append(L1Line)

        # --------------------------------
        # Linac 2

        CB01 = TM.generate('CB-Lin2-Cell-WSC', 0, {'Name': 'CB01'})
        #        CB01=TM.generate('CB-Lin2-Cell',0,{'Name':'CB01'})
        CB02 = TM.generate('CB-Lin2-Cell', 0, {'Name': 'CB02'})
        CB03 = TM.generate('CB-Lin2-Cell', 0, {'Name': 'CB03'})
        CB04 = TM.generate('CB-Lin2-Cell-Last', 0, {'Name': 'CB04'})

        SY01 = LineContainer('SY01', 8.165)
        SY01.append(TM.generate('DBPM-C16', 10), 0.03, 'relative')
        SY01.append(TM.generate('QFD', 20), 0.049, 'relative')
        SY01.append(TM.generate('QFD', 30), 1.536 + 0.8, 'relative')
        SY01.append(TM.generate('DBPM-C16', 40), 3.9 - 0.8 + 0.032, 'relative')
        SY01.append(TM.generate('QFD', 50), 0.1 - 0.032, 'relative')
        SY01.append(TM.generate('DBPM-C16', 60), 0.75 - 0.042, 'relative')
        SY01.append(TM.generate('DWSC-C16', 70), 0.1, 'relative')
        SY01.append(TM.generate('QFD', 80), 0.063 + 0.042, 'relative')

        SY02 = LineContainer('SY02', -0.7502)
        SY02.append(TM.generate('RESKICKDC', 10, {'design_kick': 0}), 0.285, 'relative')
        SY02.append(TM.generate('RESKICKAC', 20, {'design_kick': 0}), 0.0, 'relative')
        SY02.append(TM.generate('RESKICKDC', 30, {'design_kick': 0}), 0.0, 'relative')
        SY02.append(TM.generate('RESKICKAC', 40, {'design_kick': 0}), 0.0, 'relative')
        SY02.append(TM.generate('RESKICKDC', 50, {'design_kick': 0}), 0.0, 'relative')
        SY02.append(TM.generate('SFC', 60), 0.080, 'relative')
        SY02.append(TM.generate('QFA', 70), 0.105, 'relative')
        SY02.append(TM.generate('DBPM-C38', 80), 1.33 - 0.12, 'relative')
        SY02.append(TM.generate('SFC', 90), 0.08, 'relative')
        SY02.append(TM.generate('QFA', 100), 0.105, 'relative')
        SY02.append(TM.generate('DBPM-C38', 120), 1.33 - 0.12, 'relative')
        SY02.append(TM.generate('SFC', 130), 0.08, 'relative')
        SY02.append(TM.generate('QFA', 140), 0.105, 'relative')
        SY02.append(TM.generate('DBPM-C38', 150), 1.18 - 0.24, 'relative')
        SY02.append(TM.generate('DWSC-C38', 160), 0.12, 'relative')
        SY02.append(TM.generate('SFC', 170), 0.08, 'relative')
        SY02.append(TM.generate('QFA', 180), 0.105, 'relative')
        angle = 0
        SY02.append(TM.generate('AFS', 200, {'angle': angle, 'design_angle': 2, 'e1': 0, 'e2': 0, 'branch': True,
                                             'BC': 'Switch Yard 1'}), 0.30 - 0.0002 + 0.12, 'relative')
        SY02.append(TM.generate('MKBR', 201), 0., 'relative')

        SY03 = LineContainer('SY03', 19.53 + 0.12)
        SY03.append(TM.generate('DBPM-C16', 10), 4.8 + 0.12, 'relative')
        SY03.append(TM.generate('QFD', 20), 0.1, 'relative')
        SY03.append(TM.generate('QFD', 30), 3, 'relative')
        SY03.append(TM.generate('DBPM-C16', 40), 2.6, 'relative')
        SY03.append(TM.generate('QFD', 50), 0.1, 'relative')
        SY03.append(TM.generate('QFD', 60), 4.2, 'relative')
        SY03.append(TM.generate('DBPM-C16', 80), 0.2 + 2.31 + 0.05 - 0.257, 'relative')
        SY03.append(TM.generate('DSCR-HR16', 85), 0.12, 'relative')
        SY03.append(TM.generate('DWSC-C16-AL', 90), 0.1 + 0.257 - 0.12 - 0.137, 'relative')
        SY03.append(TM.generate('QFD', 100), 0.053, 'relative')

        L2Line = [CB01, CB02, CB03, CB04, SY01, SY02, SY03]
        Linac20 = LineContainer('20')
        Linac20.append(L2Line)

        # --------------------------------------
        # Linac 3

        CB01 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB01'})
        CB01.append(TM.generate('DWSC-C16', 440), 0.019, 'relative')
        CB02 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB02'})
        CB03 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB03'})
        CB04 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB04'})
        CB05 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB05'})
        CB05.append(TM.generate('DWSC-C16-AL', 440), 0.019, 'relative')
        CB06 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB06'})
        CB07 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB07'})
        CB08 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB08'})
        CB08.append(TM.generate('COL-TR-16', 440), 0.019, 'relative')
        CB09 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB09'})
        CB09.append(TM.generate('DWSC-C16', 440), 0.019, 'relative')
        CB10 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB10'})
        CB10.append(TM.generate('COL-TR-16', 440), 0.019, 'relative')
        CB11 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB11'})
        CB12 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB12'})
        CB12.append(TM.generate('COL-TR-16', 440), 0.019, 'relative')
        CB13 = TM.generate('CB-Lin3-Cell-incomplete', 0, {'Name': 'CB13'})
        CB13.append(TM.generate('DWSC-C16', 440), 0.019, 'relative')
        CB14 = LineContainer('CB14', 9.1)
        CB14.append(TM.generate('TDS C-Band', 100), 0.035, 'relative')
        CB14.append(TM.generate('TDS C-Band', 200), 0.1, 'relative')
        CB14.append(TM.generate('DBPM-C16', 420), 4.33, 'relative')
        CB14.append(TM.generate('QFD', 430), 0.049, 'relative')
        CB14.append(TM.generate('COL-TR-16', 440), 0.019, 'relative')
        if self.alt < 2:
            CB15 = LineContainer('CB15', 9.1)
            CB15.append(TM.generate('COL-Dechirper-H', 100), 1 - 0.315, 'relative')
            CB15.append(TM.generate('COL-Dechirper-V', 200), 1 + 0.315 - 0.465, 'relative')
            CB15.append(TM.generate('DBPM-C16', 420), 4.465 + 0.465, 'relative')
            CB15.append(TM.generate('QFD', 430), 0.049, 'relative')
            CB16 = LineContainer('CB16', 9.1 - 0.665)
        else:
            FC01 = LineContainer('FC01', 9.1 - 0.665)
            FC01.append(TM.generate('FCC-Crystal', 10), 0.1, 'relative')
            FC01.append(TM.generate('AFSC', 100, {'angle': 0, 'design_angle': 0, 'e1': 0.5, 'e2': 0.5}), 0.1,
                        'relative')
            FC01.append(TM.generate('FCC-Target', 110), 1.2, 'absolute')
            FC01.append(TM.generate('WFAMD', 120), 1.3, 'absolute')
            FC01.append(TM.generate('FCC-RF-ACC', 200), 1.35, 'absolute')
            FC01.append(TM.generate('WFFCC', 210), 1.45, 'absolute')
            FC01.append(TM.generate('WFFCC', 220), 2.15, 'absolute')
            FC01.append(TM.generate('FCC-RF-ACC', 300), 2.75, 'absolute')
            FC01.append(TM.generate('WFFCC', 310), 2.85, 'absolute')
            FC01.append(TM.generate('WFFCC', 320), 3.55, 'absolute')
            FC01.append(TM.generate('DBPM-FCC', 330), 4.25, 'absolute')
            FC01.append(TM.generate('DSCR-FCC', 340), 0.1, 'relative')
            FC01.append(TM.generate('SHA-FCC', 400, {'angle': 0, 'design_angle': 0, 'e1': 0.5, 'e2': 0.5}), 0.1,
                        'relative')
            FC01.append(TM.generate('DSCR-SPEC-FCC', 410), 0.7, 'relative')
            FC01.append(TM.generate('Beam-Dump-FCC', 420), 0.2, 'relative')
            CB15 = LineContainer('CB15', 0.665)
            CB15.append(TM.generate('DBPM-C16', 420), 0.03, 'relative')
            CB15.append(TM.generate('QFD', 430), 0.049, 'relative')
            CB16 = LineContainer('CB16', 9.1 - 0.665)
            CB16.append(TM.generate('COL-Dechirper-H', 100), 1 - 0.315, 'relative')
            CB16.append(TM.generate('COL-Dechirper-V', 200), 1 + 0.315 - 0.465, 'relative')

        #        if self.alt > 1:
        #            CB16.append(TM.generate('AFBC4',100,{'angle':0,'design_angle':-3,'e1':0.5,'e2':0.5,'branch':True}),0.300,'relative')
        #            CB16.append(TM.generate('MKBR',101),0.,'relative')
        #        else:
        #            CB15=LineContainer('CB15', 9.3)
        #            CB15.append(TM.generate('RESKICKDC',10,{'design_kick':0}),0.285,'relative')
        #            CB15.append(TM.generate('RESKICKAC',20,{'design_kick':0}),0.0,'relative')
        #            CB15.append(TM.generate('RESKICKDC',30,{'design_kick':0}),0.0,'relative')
        #            CB15.append(TM.generate('RESKICKAC',40,{'design_kick':0}),0.0,'relative')
        #            CB15.append(TM.generate('RESKICKDC',50,{'design_kick':0}),0.0,'relative')
        #            CB15.append(TM.generate('SFC',60),0.080,'relative')
        #            CB15.append(TM.generate('QFA',70),0.105,'relative')
        #            CB15.append(TM.generate('DBPM-C38',80),1.33-0.12,'relative')
        #            CB15.append(TM.generate('SFC',90),0.08,'relative')
        #            CB15.append(TM.generate('QFA',100),0.105,'relative')
        #            CB15.append(TM.generate('DBPM-C38',120),1.33-0.12,'relative')
        #            CB15.append(TM.generate('SFC',130),0.08,'relative')
        #            CB15.append(TM.generate('QFA',140),0.105,'relative')
        #            CB15.append(TM.generate('DBPM-C38',150),1.18-0.24,'relative')
        #            CB15.append(TM.generate('DWSC-C38',160),0.12,'relative')
        #            CB15.append(TM.generate('SFC',170),0.08,'relative')
        #            CB15.append(TM.generate('QFA',180),0.105,'relative')
        #            CB16=LineContainer('CB16', 1.3)

        if self.alt > 1:
            L3Line = [CB01, CB02, CB03, CB04, CB05, CB06, CB07, CB08, CB09, CB10, CB11, CB12, CB13, CB14, FC01, CB15,
                      CB16]
        else:
            L3Line = [CB01, CB02, CB03, CB04, CB05, CB06, CB07, CB08, CB09, CB10, CB11, CB12, CB13, CB14, CB15, CB16]

        Linac30 = LineContainer('30')
        Linac30.append(L3Line)

        # ----------------------------
        # Aramis

        dx = 8.435 - 1.3
        CL01 = LineContainer('CL01', 13.54)
        CL01.append(TM.generate('DBPM-C16', 10), 0.03, 'relative')
        CL01.append(TM.generate('QFD', 20), 0.049, 'relative')
        CL01.append(TM.generate('COL-TR-16', 30), 0.019, 'relative')
        CL01.append(TM.generate('SFQFM', 40), 0.855, 'relative')
        CL01.append(TM.generate('QFM', 50), 0, 'relative')
        CL01.append(TM.generate('DBPM-C16', 60), 1.95, 'relative')
        CL01.append(TM.generate('SFQFM', 70), 0.0, 'relative')
        CL01.append(TM.generate('QFM', 80), 0, 'relative')
        CL01.append(TM.generate('SFQFM', 90), 2.05, 'relative')
        CL01.append(TM.generate('QFM', 100), 0, 'relative')
        CL01.append(TM.generate('DCDR', 105), 0.5 + 0.649 - 0.039, 'relative')  # 0.137 length
        CL01.append(TM.generate('DBAM-FS16', 110), 1.775 - 0.637 - 0.649 + 0.039, 'relative')
        CL01.append(TM.generate('DBPM-C16', 120), 0.1, 'relative')
        CL01.append(TM.generate('SFQFM', 130), 0.0, 'relative')
        CL01.append(TM.generate('QFM', 140), 0, 'relative')
        CL01.append(TM.generate('DBPM-C16', 150), 0.276, 'relative')
        CL01.append(TM.generate('DWSC-C16-AL', 160), 0.1, 'relative')
        CL01.append(TM.generate('DSCR-HR16', 170), 0.1, 'relative')
        CL01.append(TM.generate('SFQFM', 180), 0.0, 'relative')
        CL01.append(TM.generate('QFM', 190), 0, 'relative')

        CL02 = LineContainer('CL02', 0)
        CL02.append(
            TM.generate('AFBC3', 100, {'angle': -1, 'design_angle': -1, 'e1': 0, 'e2': 1, 'BC': 'Aramis Collimator'}),
            0., 'relative')
        CL02.append(TM.generate('DBPM-C16', 110), 2.55 + 0.035, 'relative')
        CL02.append(TM.generate('SFQFM', 120), 0.0, 'relative')
        CL02.append(TM.generate('QFM-short', 130), 0.1 - 0.035, 'relative')
        #        CL02.append(TM.generate('HFB',140),0.35+0.035,'relative')
        CL02.append(TM.generate('QFB', 150), 0.1 + 0.45 + 0.035, 'relative')
        CL02.append(TM.generate('QFBS', 160), 0.1, 'relative')
        dl = 5.25 / math.cos(math.asin(1) / 90) - 4.4 - 0.035
        CL02.append(
            TM.generate('AFBC3', 200, {'angle': 1, 'design_angle': 1, 'e1': 1, 'e2': 0, 'BC': 'Aramis Collimator'}), dl,
            'relative')
        CL02.append(TM.generate('QFM-short', 210), 0.35, 'relative')
        CL02.append(TM.generate('DBPM-C16', 220), 0.1 - 0.065, 'relative')
        CL02.append(TM.generate('SFQFM', 230), 0.065, 'relative')
        CL02.append(TM.generate('DWSC-C16', 235), 0.1 + 0.141, 'relative')
        CL02.append(TM.generate('SFQFM', 240), 0.4 - 0.237 - 0.141, 'relative')
        CL02.append(TM.generate('QFM-short', 250), 0.1, 'relative')
        CL02.append(TM.generate('HFB', 255), 0.02, 'relative')
        CL02.append(TM.generate('DBPM-C16', 260), 0.1 - 0.089 + 0.157, 'relative')
        CL02.append(TM.generate('DSCR-HR16', 280), 0.12, 'relative')
        CL02.append(TM.generate('BC-SlotFoil-V', 282), 0.57, 'relative')
        CL02.append(TM.generate('COL-Energy', 290), 0.8 - 0.15 - 0.57, 'relative')
        CL02.append(TM.generate('QFS', 300), 0.274 - 0.073 + 0.104, 'relative')
        CL02.append(TM.generate('HFB', 305), 0.08, 'relative')
        CL02.append(TM.generate('QFM-short', 310), 0.02, 'relative')
        CL02.append(TM.generate('SFQFM', 320), 0.1, 'relative')
        CL02.append(TM.generate('DALA', 325), 0.119 - 0.011, 'relative')
        CL02.append(TM.generate('DBPM-C16', 330), 0.35 + 0.015 - 0.137 - 0.119 + 0.011, 'relative')
        CL02.append(TM.generate('SFQFM', 340), 0.035, 'relative')
        CL02.append(TM.generate('QFM', 350), 0, 'relative')
        CL02.append(
            TM.generate('AFBC3', 400, {'angle': 1, 'design_angle': 1, 'e1': 0, 'e2': 1, 'BC': 'Aramis Collimator'}),
            0.25, 'relative')
        dl = 5.25 / math.cos(math.asin(1) / 90) - 5.0 + 0.03 - 0.1
        CL02.append(TM.generate('DSRM-UV', 410), 0.5, 'relative')
        CL02.append(TM.generate('QFBS', 420), dl, 'relative')
        CL02.append(TM.generate('QFB', 430), 0.1, 'relative')
        #        CL02.append(TM.generate('HFB',440),0.1,'relative')
        CL02.append(TM.generate('SFQFM', 450), 0.05 + 0.2, 'relative')
        CL02.append(TM.generate('QFM-short', 460), 0.1 - 0.03, 'relative')
        CL02.append(TM.generate('DBPM-C16', 470), 0.3 + 0.03, 'relative')
        CL02.append(TM.generate('SFQFM', 480), 0.00, 'relative')
        CL02.append(TM.generate('DALA', 485), 1.875 - 0.012, 'relative')
        CL02.append(
            TM.generate('AFBC3', 500, {'angle': -1, 'design_angle': -1, 'e1': 1, 'e2': 0, 'BC': 'Aramis Collimator'}),
            2.35 - 0.03 - 0.137 - 1.875 + 0.012, 'relative')

        MA01 = LineContainer('MA01', 13.25)
        MA01.append(TM.generate('QFM-veryshort', 10), 0.3, 'relative')
        MA01.append(TM.generate('DBCM-IR', 15), 0.125, 'relative')
        MA01.append(TM.generate('SFQFM-short', 20), 0.05 - 0.025, 'relative')
        MA01.append(TM.generate('DBPM-C16', 40), 0.25 + 0.7 + 0.1, 'relative')
        MA01.append(TM.generate('SFQFM', 50), 0.00, 'relative')
        MA01.append(TM.generate('QFM', 60), 0.0, 'relative')
        MA01.append(TM.generate('SFQFM', 70), 2.55, 'relative')
        MA01.append(TM.generate('QFM', 80), 0.0, 'relative')
        MA01.append(TM.generate('DICT-C16', 90), 1.95 - 0.075 - 0.09 + 0.1575 - 0.05, 'relative')
        MA01.append(TM.generate('DBPM-C16', 100), 0.2 + 0.175 - 0.1575 + 0.05, 'relative')
        MA01.append(TM.generate('SFQFM', 110), 0.00, 'relative')
        MA01.append(TM.generate('QFM', 120), 0.0, 'relative')
        MA01.append(TM.generate('SFQFM', 130), 2.0, 'relative')
        MA01.append(TM.generate('QFM', 140), 0.0, 'relative')

        Lsec = 9.5
        angle = 0
        MA02 = LineContainer('MA02', Lsec)
        MA02.append(TM.generate('DBPM-C8', 10), 0.385, 'relative')
        MA02.append(TM.generate('DBPM-C8', 20), 0.85 + 0.05 + 1 - 0.002 + 0.051, 'relative')
        MA02.append(TM.generate('DSCR-HR8', 30), 1.78 - 0.037 + 0.009 - 0.06, 'relative')
        MA02.append(TM.generate('DBPM-C8', 40), 0.12, 'relative')
        MA02.append(TM.generate('QFF', 50), 0.06, 'relative')
        MA02.append(TM.generate('DWSC-C8', 60), 0.077, 'relative')
        MA02.append(TM.generate('AFP1', 100, {'angle': angle, 'design_angle': 0, 'e1': 0, 'e2': 1}), 0.175, 'relative')
        MA02.append(TM.generate('Beam-Stopper-Sar', 105), 0.881, 'relative')
        MA02.append(TM.generate('DBPM-C8', 110), 0.477, 'relative')
        MA02.append(TM.generate('QFF', 120), 0.06, 'relative')

        UN01 = TM.generate('U15-Cell-Empty', 0, {'Name': 'UN01'})

        if (self.alt == 2):
            UN02 = TM.generate('U15-Cell', 0, {'Name': 'UN02'})
        else:
            UN02 = TM.generate('U15-Cell-Empty', 0, {'Name': 'UN02'})

        UN03 = TM.generate('U15-Cell', 0, {'Name': 'UN03'})
        UN04 = TM.generate('U15-Cell', 0, {'Name': 'UN04'})
        UN05 = TM.generate('U15-Cell', 0, {'Name': 'UN05'})
        UN06 = TM.generate('U15-Cell', 0, {'Name': 'UN06'})
        UN07 = TM.generate('U15-Cell', 0, {'Name': 'UN07'})
        UN08 = TM.generate('U15-Cell', 0, {'Name': 'UN08'})

        if (self.alt == 2):
            UN09 = LineContainer('UN09', -0.027)
            varC = VariableContainer(1.200, 0)
            UN09.append(TM.generate('DWSC-C8', 10), 0.05 + 0.175, 'relative')
            UN09.append(TM.generate('AFSS', 100, {'angle': -0, 'design_angle': -0.22, 'e1': 0, 'e2': 1,
                                                  'BC': 'Aramis Self-Seeding'}), 0.199, 'relative')
            UN09.append(TM.generate('AFSS', 200,
                                    {'angle': 0, 'design_angle': 0.22, 'e1': 1, 'e2': 0, 'BC': 'Aramis Self-Seeding'}),
                        1, varC)
            UN09.append(TM.generate('AFSS', 300,
                                    {'angle': 0, 'design_angle': 0.22, 'e1': 0, 'e2': 1, 'BC': 'Aramis Self-Seeding'}),
                        0.16, 'relative')
            UN09.append(TM.generate('AFSS', 400, {'angle': -0, 'design_angle': -0.22, 'e1': 1, 'e2': 0,
                                                  'BC': 'Aramis Self-Seeding'}), 1, varC)
            UN09.append(TM.generate('DBPM-C8', 410), 0.374 - 0.175, 'relative')
            UN09.append(TM.generate('QFF', 420), 0.06, 'relative')
        else:
            UN09 = TM.generate('U15-Cell', 0, {'Name': 'UN09'})

        UN10 = TM.generate('U15-Cell', 0, {'Name': 'UN10'})
        UN11 = TM.generate('U15-Cell', 0, {'Name': 'UN11'})
        UN12 = TM.generate('U15-Cell', 0, {'Name': 'UN12'})
        UN13 = TM.generate('U15-Cell', 0, {'Name': 'UN13'})
        UN14 = TM.generate('U15-Cell', 0, {'Name': 'UN14'})
        UN15 = TM.generate('U15-Cell-Last', 0, {'Name': 'UN15'})
        UN16 = TM.generate('U15-Cell-Empty', 0, {'Name': 'UN16'})
        UN17 = TM.generate('U15-Cell-Empty', 0, {'Name': 'UN17'})
        UN18 = LineContainer('UN18', 4.75)
        UN18.append(TM.generate('COL-Dechirper-H', 10), 0.85 - 0.0625, 'relative')
        UN18.append(TM.generate('COL-Dechirper-H', 20), 0.85, 'relative')
        UN18.append(TM.generate('DBPM-C8', 70), 4.483 - 3.7 + 0.0625, 'relative')
        UN18.append(TM.generate('QFF', 80), 0.06, 'relative')
        UN19 = TM.generate('U15-Cell-Empty', 0, {'Name': 'UN19'})
        UN20 = LineContainer('UN20', 4.75)
        UN20.append(TM.generate('DWSC-C8', 10), 0.05, 'relative')
        UN20.append(TM.generate('DBAM-FS8', 20), 0.025 + 2.133 - 0.0005, 'relative')
        UN20.append(TM.generate('DBPM-C8', 70), 2.1 + 0.0005 + 0.025 - 0.05, 'relative')
        UN20.append(TM.generate('QFF', 80), 0.06, 'relative')

        Lsec = 0
        angle = 0
        BD01 = LineContainer('BD01', Lsec)
        BD01.append(TM.generate('QFF', 20), 0.2265 - 0.116 + 0.29 + 0.125 + 0.075 + 1.05 - 0.29, 'relative')
        BD01.append(TM.generate('DICT-C16', 30), 0.06 + 0.3235 - 0.125 + 0.03, 'relative')
        BD01.append(TM.generate('DBPM-C16', 40), 0.25 + 0.106 - 0.1 - 0.1885, 'relative')
        BD01.append(TM.generate('DSCR-HR16', 50), 0.12, 'relative')
        BD01.append(TM.generate('AFD1', 100, {'angle': angle, 'design_angle': 8, 'e1': 0.5, 'e2': 0.5, 'branch': True}),
                    0.279 - 0.0125, 'relative')
        BD01.append(TM.generate('MKBR', 101), 0.0, 'relative')
        BD01.append(TM.generate('DSCR-OV38', 110), 5.55 - 2.2665, 'relative')
        BD01.append(TM.generate('AFP1', 200, {'angle': 0, 'design_angle': 0, 'e1': 0, 'e2': 1, 'Tilt': math.asin(1)}),
                    0.363, 'relative')
        BD01.append(TM.generate('FE-Shielding', 205), 2.967, 'relative')

        ArLine = [CL01, CL02, MA01, MA02, UN01, UN02, UN03, UN04, UN05, UN06, UN07, UN08, UN09, UN10, UN11, UN12, UN13,
                  UN14, UN15, UN16, UN17, UN18, UN19, UN20, BD01]
        Aramis = LineContainer('AR')
        Aramis.append(ArLine)

        # Aramis Dump
        BD02 = LineContainer('BD02', 0)
        BD02.append(TM.generate('DBPM-C16', 10), 0.42, 'relative')
        dlict = 0.0
        dlict = 0.1575
        LD = 1.1 / math.cos(8 * math.asin(1) / 90) - 0.92 - 0.1 + dlict - 0.0075
        BD02.append(TM.generate('QFM', 30), LD, 'relative')
        LD = LD + 0.3015 - dlict
        BD02.append(TM.generate('DBPM-C16', 40), LD - 0.022 + 0.03235, 'relative')
        BD02.append(TM.generate('DSCR-HR16', 50), 0.12, 'relative')
        LD = 19.478 / math.cos(8 * math.asin(1) / 90) - 0.0685 + 0.2 + 0.002 - 0.0249
        BD02.append(TM.generate('Beam-Dump-Sar', 55), LD, 'relative')

        AramisDump = LineContainer('AR')
        AramisDump.append(BD02, 0, 'relative')

        # -----------------------------
        # Athos Beamline

        ddx = 0.7502
        SY01 = LineContainer('SY01', 29.100107 + ddx + 0.12 + 0.000049)
        SY01.append(Alignment({'dy': 0.01, 'Tag': 'ALIG', 'index': 1}))
        SY01.append(TM.generate('DBPM-C16', 10), 3.3 + ddx + 0.12 + 0.000048, 'relative')
        SY01.append(TM.generate('QFM', 20), 0.35 - 0.183 - 0.035, 'relative')
        SY01.append(TM.generate('SFQFM', 22), 0.183 + 0.925 + 0.035, 'relative')
        SY01.append(TM.generate('BC-SlotFoil-V', 25), 1.65 - 0.626 - 0.925, 'relative')
        SY01.append(TM.generate('QFBS', 30), 0.15 + 0.026, 'relative')

        SY01.append(TM.generate('QFD', 40), 0.05, 'relative')
        SY01.append(TM.generate('HFB', 50), 0.1, 'relative')
        SY01.append(TM.generate('DBPM-C16', 60), 2.1, 'relative')
        SY01.append(TM.generate('QFD', 70), 0.1, 'relative')
        SY01.append(TM.generate('HFB', 80), 0.1, 'relative')
        SY01.append(TM.generate('QFD', 90), 2.3, 'relative')
        SY01.append(TM.generate('DBPM-C16', 100), 1.25 - 0.135, 'relative')
        SY01.append(TM.generate('AFBC3-noCor', 200,
                                {'angle': 1, 'design_angle': 1, 'e1': 0.5, 'e2': 0.5, 'BC': 'Switch Yard 1'}),
                    0.15 + 0.135, 'relative')
        # used for matching        SY01.append(TM.generate('AFBC3',200,{'angle':1,'e1':0.5,'e2':0.5}),0.15,'relative')
        SY01.append(TM.generate('QFD', 210), 1.5, 'relative')
        SY01.append(TM.generate('HFB', 220), 2.3, 'relative')
        SY01.append(TM.generate('QFD', 230), 0.1, 'relative')
        SY01.append(TM.generate('DBPM-C16', 240), 1.8, 'relative')
        SY01.append(TM.generate('HFB', 250), 0.4, 'relative')
        SY01.append(TM.generate('QFD', 260), 0.1, 'relative')
        SY01.append(TM.generate('QFS', 270), 0.05, 'relative')
        SY01.append(TM.generate('QFM', 280), 1.912, 'relative')
        SY01.append(TM.generate('SFQFM', 282), 0., 'relative')
        SY01.append(TM.generate('DBPM-C16', 290), 3.0 - 0.45 - 0.012, 'relative')
        SY01.append(TM.generate('QFD', 300), 0.1, 'relative')
        SY01.append(
            TM.generate('AFBC3-noCor', 400, {'angle': 2, 'design_angle': 2, 'e1': 1, 'e2': 0., 'BC': 'Switch Yard 1'}),
            1.15, 'relative')

        SY02 = LineContainer('SY02', 9.13)
        SY02.append(TM.generate('QFD', 10), 1.0, 'relative')
        SY02.append(TM.generate('DBPM-C16', 20), 0.7 - 0.004, 'relative')
        SY02.append(
            TM.generate('AFL', 100, {'angle': 0.108, 'design_angle': 0.108, 'e1': 0, 'e2': 1., 'Tilt': math.asin(1)}),
            0.194, 'relative')
        SY02.append(TM.generate('QFD', 110), 1.29, 'relative')
        SY02.append(TM.generate('QFD', 120), 2.1, 'relative')
        SY02.append(
            TM.generate('AFL', 200, {'angle': -0.108, 'design_angle': -0.108, 'e1': 1, 'e2': 0., 'Tilt': math.asin(1)}),
            1.29, 'relative')
        SY02.append(TM.generate('DBPM-C16', 210), 0.103, 'relative')
        SY02.append(TM.generate('QFD', 230), 0.03 + 0.137 + 0.12, 'relative')

        SY03 = LineContainer('SY03', 12.65)
        SY03.append(TM.generate('QFD', 10), 0.45, 'relative')
        SY03.append(TM.generate('DBPM-C16', 30), 0.1 + 2.35, 'relative')
        SY03.append(TM.generate('QFD', 40), 0.1, 'relative')
        if self.alt < 1:
            SY03.append(TM.generate('DBPM-C16', 60), 0.1 + 2.25, 'relative')
        else:
            SY03.append(TM.generate('DCDR', 50), 0.876, 'relative')
            SY03.append(TM.generate('DBPM-C16', 60), 0.1 + 2.25 - 0.876 - 0.137, 'relative')

        SY03.append(TM.generate('QFD', 70), 0.1, 'relative')
        SY03.append(TM.generate('Laser-Acceleration', 80), 0.13 - 0.106, 'relative')
        SY03.append(TM.generate('DBPM-C16', 90), 0.1 - 0.01 + 0.106, 'relative')
        SY03.append(TM.generate('QFD', 100), 0.1, 'relative')
        SY03.append(TM.generate('DWSC-C16', 110), 2. - 0.02 - 0.064, 'relative')
        SY03.append(TM.generate('DALA', 115), 0.08, 'relative')
        SY03.append(TM.generate('DBPM-C16', 120), 0.08, 'relative')
        SY03.append(TM.generate('QFD', 130), 0.1, 'relative')
        SY03.append(TM.generate('DSCR-HR16', 140), 0.08 + 0.153, 'relative')

        CL01 = LineContainer('CL01', 12.050318)
        CL01.append(
            TM.generate('AFBC3', 100, {'angle': -2.5, 'design_angle': -2.5, 'e1': 0, 'e2': 1., 'BC': 'Switch Yard 2'}),
            0.0, 'relative')
        if self.alt > 1:
            CL01.append(TM.generate('DSRM-UV', 105), 0.6, 'relative')
            CL01.append(TM.generate('HFB', 110), 0.15, 'relative')
            CL01.append(TM.generate('QFD', 120), 0.05, 'relative')
            CL01.append(TM.generate('QFD', 130), 2.5, 'relative')
            CL01.append(TM.generate('DBPM-C16', 140), 0.718, 'relative')
            CL01.append(TM.generate('DSCR-HR16', 150), 0.12, 'relative')
            CL01.append(TM.generate('HFB', 160), 0.45, 'relative')
            CL01.append(TM.generate('DALA', 165), 0.5 - 0.05 - 0.137 - 0.1 + 0.0197938, 'relative')
            CL01.append(TM.generate('COL-Energy', 170), 0.1 - 0.0197938, 'relative')
            CL01.append(TM.generate('QFD', 180), 0.475, 'relative')
            CL01.append(TM.generate('QFD', 190), 2.5, 'relative')
            CL01.append(TM.generate('AFBC3', 300,
                                    {'angle': -2.5, 'design_angle': -2.5, 'e1': 1, 'e2': 0., 'BC': 'Switch Yard 2'}),
                        0.85 - 0.137 - 0.26 + 0.001 + 0.546, 'relative')
        else:
            CL01.append(TM.generate('HFB', 110), 0.15 + 0.7, 'relative')
            CL01.append(TM.generate('QFD', 120), 0.05, 'relative')
            CL01.append(TM.generate('QFD', 130), 2.5, 'relative')
            CL01.append(TM.generate('DBPM-C16', 140), 0.718, 'relative')
            CL01.append(TM.generate('DSCR-HR16', 150), 0.12, 'relative')
            CL01.append(TM.generate('HFB', 160), 0.45, 'relative')
            CL01.append(TM.generate('COL-Energy', 170), 0.5 - 0.05, 'relative')
            CL01.append(TM.generate('QFD', 180), 0.475, 'relative')
            CL01.append(TM.generate('QFD', 190), 2.5, 'relative')
            CL01.append(TM.generate('HFB', 200), 0.05, 'relative')
            CL01.append(TM.generate('DALA', 205), 0.2600 - 0.001, 'relative')
            CL01.append(TM.generate('AFBC3', 300,
                                    {'angle': -2.5, 'design_angle': -2.5, 'e1': 1, 'e2': 0., 'BC': 'Switch Yard 2'}),
                        0.85 - 0.137 - 0.26 + 0.001, 'relative')

        DI01 = LineContainer('DI01', 18.52)
        # Girder 1
        if self.alt > 1:  # temporarily changing this to planned, was before self.alt>1
            DI01.append(TM.generate('DBCM-IR', 10), 0.4, 'relative')
            DI01.append(TM.generate('DICT-C16', 20), 0.46 - 0.1, 'relative')
            DI01.append(TM.generate('QFD', 25), 0.15, 'relative')
            DI01.append(TM.generate('DBPM-C16', 30), 0.2 + 0.226 - 0.326, 'relative')
            DI01.append(TM.generate('DSCR-OV16', 40), 0.1, 'relative')
            DI01.append(TM.generate('UMOD', 50), 0.4 - 0.226 + 0.326 - 0.1, 'relative')
            DI01.append(TM.generate('UMOD', 51), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 52), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 53), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 54), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 55), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 56), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 57), 0.001, 'relative')
            DI01.append(TM.generate('UMOD', 58), 0.001, 'relative')
            DI01.append(TM.generate('DBPM-C16', 60), 0.286 - 0.008 - 0.06, 'relative')
            DI01.append(TM.generate('DSCR-OV16', 65), 0.1, 'relative')
            DI01.append(TM.generate('DBAM-FS16', 70), 0.1 + 0.06 + 0.02 - 0.02 + 0.1, 'relative')
        else:
            DI01.append(TM.generate('DICT-C16', 20), 1.4 + 0.043 - 0.0075 + 0.5, 'relative')
            DI01.append(TM.generate('DBPM-C16', 30), 0.15 - 0.043 + 0.013 + 0.175 - 0.1575, 'relative')
            DI01.append(TM.generate('QFD', 40), 0.1 - 0.013, 'relative')
            DI01.append(TM.generate('QFD', 50), 1.15, 'relative')
            DI01.append(TM.generate('DBPM-C16', 60), 0.063, 'relative')
            DI01.append(TM.generate('DBAM-FS16', 70), 0.1 + 0.06 + 0.02 + 0.23 + 0.12 + 0.137 - 0.02, 'relative')
        # girder 2
        if self.alt > 0:
            DI01.append(TM.generate('QFD', 80), 2.15 - 1.563 - 0.397 - 0.02 + 0.02, 'relative')
            DI01.append(TM.generate('DBPM-C16', 90), 0.063, 'relative')
            DI01.append(TM.generate('COL-Dechirper-H', 100, {'gap': 2e-3}), 0.5 + 0.087, 'relative')
        else:
            DI01.append(TM.generate('COL-Dechirper-H', 100, {'gap': 2e-3}), 0.7 + 0.087 + 0.2186 + 0.1644 + 0.02,
                        'relative')

        DI01.append(TM.generate('COL-Dechirper-V', 200, {'gap': 2e-3}), 0.5 + 0.35, 'relative')
        DI01.append(TM.generate('DBPM-C16', 210), 0.5 + 0.019 + 0.115 + 0.327 - 0.437, 'relative')
        DI01.append(TM.generate('QFD', 220), 0.081, 'relative')
        #        DI01.append(TM.generate('DBPM-C16',222),0.5+0.019+2+3.58-0.23-0.255-4.975,'relative')
        #        DI01.append(TM.generate('QFD',225),0.1-0.019,'relative')
        DI01.append(TM.generate('QFD', 230), 1.25 + 0.7 + 0.37, 'relative')
        DI01.append(TM.generate('DBPM-C16', 240), 1.05 - 0.001, 'relative')
        DI01.append(TM.generate('QFD', 250), 0.101, 'relative')
        DI01.append(TM.generate('QFD', 260), 1.25, 'relative')
        DI01.append(TM.generate('DBPM-C16', 270), 1.05 - 0.021, 'relative')
        DI01.append(TM.generate('QFD', 280), 0.121, 'relative')
        DI01.append(TM.generate('DWSC-C16', 290), 0.1 + 0.729, 'relative')
        DI01.append(TM.generate('QFD', 300), 0.163 + 0.137 + 0.85 - 0.237 - 0.729, 'relative')
        DI01.append(TM.generate('DBPM-C16', 310), 0.04, 'relative')
        # needs a wire scanner here

        CB01 = LineContainer('CB01', 9.8)
        CB02 = LineContainer('CL02', 9.8)
        CB01.append(TM.generate('TW Cav C-Band', 100), 0.035, 'relative')
        CB01.append(TM.generate('TW Cav C-Band', 200), 0.049387, 'relative')
        CB01.append(TM.generate('DBPM-C16', 220), 0.080613, 'relative')
        CB01.append(TM.generate('QFD', 230), 0.049, 'relative')
        CB01.append(TM.generate('TW Cav C-Band', 300), 0.096075 + 0.137 + 0.019, 'relative')
        CB01.append(TM.generate('TW Cav C-Band', 400), 0.049387, 'relative')
        CB01.append(TM.generate('DBPM-C16', 420), 0.099538, 'relative')
        CB01.append(TM.generate('QFD', 430), 0.049, 'relative')
        CB02.append(TM.generate('COL-Dechirper-V', 100, {'gap': 2e-3}), 0.5 + 0.528 - 0.003, 'relative')
        CB02.append(TM.generate('COL-Dechirper-H', 200, {'gap': 2e-3}), 0.5 - 0.528 + 0.875 + 0.003, 'relative')
        CB02.append(TM.generate('DBPM-C16', 220), 0.080613 + 0.035 + 0.049387 + 0.085 + 1.015 - 0.875, 'relative')
        CB02.append(TM.generate('QFD', 230), 0.049, 'relative')
        CB02.append(TM.generate('COL-Dechirper-V', 300, {'gap': 2e-3}), 0.5 + 0.74208, 'relative')
        CB02.append(TM.generate('COL-Dechirper-H', 400, {'gap': 2e-3}), 0.5 - 0.74208 + 1.09208, 'relative')
        CB02.append(TM.generate('DBPM-C16', 420), 0.099538 + 1.40146 - 1.09208, 'relative')
        CB02.append(TM.generate('QFD', 430), 0.049, 'relative')

        # here the missing part of the Athos comes only in the later phase (planned and final)

        Lsec = 9.51 + 18.0 + 1.1245 + 0.0275 + 20 - 11.6247 - 0.2 - 0.0027
        if self.alt > 1:
            MA01 = LineContainer('MA01', Lsec - 0.1925)
        else:
            MA01 = LineContainer('MA01', Lsec - 8.1726)

        angle = 0
        MA01.append(TM.generate('DBPM-C8', 10), 0.293 + 0.102 - 0.257, 'relative')
        MA01.append(TM.generate('COL-Dechirper-V', 15, {'gap': 2e-3}), 0.5 + 0.257 - 0.202, 'relative')
        MA01.append(TM.generate('DBPM-C8', 20), 0.5 - 0.051 - 0.1285 + 0.202, 'relative')
        if self.alt > 1:
            MA01.append(TM.generate('COL-Dechirper-H', 25, {'gap': 2e-3}), 0.5 + 0.1285 - 0.2155, 'relative')
            MA01.append(TM.generate('DSCR-HR8', 30), 0.28 - 0.037 - 0.051 + 0.2155, 'relative')
        else:
            MA01.append(TM.generate('DSCR-HR8', 30), 0.28 - 0.037 - 0.051 + 0.2155 + 0.5 + 0.1285 - 0.2155 + 1,
                        'relative')

        MA01.append(TM.generate('DBPM-C8', 40), 0.12, 'relative')
        MA01.append(TM.generate('QFF', 50), 0.06, 'relative')
        MA01.append(TM.generate('AFP1', 100, {'angle': 0, 'e1': 0, 'e2': 1}), 0.175 + 0.177, 'relative')
        MA01.append(TM.generate('Beam-Stopper-Sat', 105), 0.881, 'relative')

        angcal = 0.1

        if self.alt < 2:
            MA01.append(TM.generate('DBPM-C8', 110), 1.477, 'relative')
            MA01.append(TM.generate('QFF', 120), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 130), 4, 'relative')
            MA01.append(TM.generate('QFF', 140), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 150), 4., 'relative')
            MA01.append(TM.generate('QFF', 160), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 170), 4., 'relative')
            MA01.append(TM.generate('QFF', 180), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 190), 4, 'relative')
            MA01.append(TM.generate('QFF', 200), 0.06, 'relative')
            UN01 = TM.generate('UE38-Cell-Empty', 0, {'Name': 'UN01'})
            UN02 = TM.generate('UE38-Cell-Empty', 0, {'Name': 'UN02'})
            UN03 = TM.generate('UE38-Cell-Empty', 0, {'Name': 'UN03'})
            UN04 = TM.generate('UE38-Cell-Empty', 0, {'Name': 'UN04'})  # modulator goes in here.....
            if self.alt < 1:
                UN05 = TM.generate('UE38-Cell-Empty-400', 0, {'Name': 'UN05'})
            else:
                UN05 = LineContainer('UN05', -0.027 - 0.07275 + 0.005)
                varC = VariableContainer(0.38, 0)
                UN05.append(TM.generate('AFSS', 100, {'angle': 0.0, 'design_angle': angcal, 'e1': 0, 'e2': 1,
                                                      'BC': 'Athos Self-Seeding'}), 0.18, 'relative')
                UN05.append(TM.generate('AFSS', 200, {'angle': 0.0, 'design_angle': -angcal, 'e1': 1, 'e2': 0,
                                                      'BC': 'Athos Self-Seeding'}), 1, varC)
                UN05.append(TM.generate('AFSS', 300, {'angle': 0.0, 'design_angle': -angcal, 'e1': 0, 'e2': 1,
                                                      'BC': 'Athos Self-Seeding'}), 0.16, 'relative')
                UN05.append(TM.generate('AFSS', 400, {'angle': 0.0, 'design_angle': angcal, 'e1': 1, 'e2': 0,
                                                      'BC': 'Athos Self-Seeding'}), 1, varC)
                UN05.append(TM.generate('DBPM-C5', 410), 0.18 + 0.00775, 'relative')
                UN05.append(TM.generate('QFF', 420), 0.06025 - 0.00775 + 0.005, 'relative')
        else:
            MA01.append(TM.generate('DBPM-C8', 110), 0.6013, 'relative')
            MA01.append(TM.generate('QFF', 120), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 130), 2.8 - 0.24, 'relative')
            MA01.append(TM.generate('QFF', 140), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 150), 2.8 - 0.24, 'relative')
            MA01.append(TM.generate('QFF', 160), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 170), 2.8 - 0.24, 'relative')
            MA01.append(TM.generate('QFF', 180), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 190), 2.8 - 0.24, 'relative')
            MA01.append(TM.generate('QFF', 200), 0.06, 'relative')
            MA01.append(TM.generate('DBPM-C8', 210), 2.8 - 0.24, 'relative')
            MA01.append(TM.generate('QFF', 220), 0.06, 'relative')
            MA01.append(TM.generate('QFF', 230), 1 - 0.18, 'relative')
            MA01.append(TM.generate('DBPM-C8', 240), 0.06 + 0.6, 'relative')
            MA01.append(TM.generate('QFF', 250), 1 - 0.18 - 0.16 - 0.6, 'relative')
            MA01.append(TM.generate('AFBC3', 300,
                                    {'angle': -0, 'design_angle': -2.3, 'e1': 0, 'e2': 1, 'BC': 'Athos EEHG first BC'}),
                        0.26, 'relative')
            MA01.append(TM.generate('AFBC3', 400,
                                    {'angle': 0, 'design_angle': 2.3, 'e1': 1, 'e2': 0, 'BC': 'Athos EEHG first BC'}),
                        3.47, 'relative')
            MA01.append(TM.generate('AFBC3', 500,
                                    {'angle': 0, 'design_angle': 2.3, 'e1': 0, 'e2': 1, 'BC': 'Athos EEHG first BC'}),
                        0.2, 'relative')
            MA01.append(TM.generate('AFBC3', 600,
                                    {'angle': 0, 'design_angle': -2.3, 'e1': 1, 'e2': 0, 'BC': 'Athos EEHG first BC'}),
                        3.47, 'relative')
            MA01.append(TM.generate('QFD', 610), 0.06 + 0.22,
                        'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            MA01.append(TM.generate('DBPM-C16', 620), 0.2 + 0.0438, 'relative')

            MA01.append(TM.generate('QFD', 630), 1 - 0.18 - 0.17 - 0.3 - 0.25 - 0.0438,
                        'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            MA01.append(TM.generate('QFD', 640), 1 - 0.18 - 0.17 - 0.25,
                        'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            UN04 = LineContainer('UN04', 3.0247 + 0.0027 + 0.1925)  # modulator
            UN04.append(TM.generate('DBPM-C16', 10), 0., 'relative')
            UN04.append(TM.generate('DSCR-HR16', 20), 0.05 + 0.0293 + 0.1925 - 0.2218, 'relative')
            UN04.append(TM.generate('UMOD', 30), 0.03 + 0.3491 + 0.2218 - 0.301, 'relative')
            UN04.append(TM.generate('UMOD', 31), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 32), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 33), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 34), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 35), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 36), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 37), 0.001, 'relative')
            UN04.append(TM.generate('UMOD', 38), 0.001, 'relative')
            UN04.append(TM.generate('DBPM-C16', 40), 0.03 - 0.0381 + 0.301 - 0.17614, 'relative')
            UN04.append(TM.generate('DSCR-HR16', 50), 0.05, 'relative')
            UN04.append(TM.generate('QFF', 60),
                        0.06025 - 0.00775 + 0.005 + 0.0338 + 0.0381 - 0.00004 - 0.059 + 0.17614 + 0.0095, 'relative')
            UN05 = LineContainer('UN05', -0.027 - 0.07275 + 0.005)
            varC = VariableContainer(0.38, 0)
            UN05.append(TM.generate('AFSS', 100, {'angle': 0.0, 'design_angle': angcal, 'e1': 0, 'e2': 1,
                                                  'BC': 'Athos Self-Seeding'}), 0.18, 'relative')
            UN05.append(TM.generate('AFSS', 200, {'angle': 0.0, 'design_angle': -angcal, 'e1': 1, 'e2': 0,
                                                  'BC': 'Athos Self-Seeding'}), 1, varC)
            UN05.append(TM.generate('AFSS', 300, {'angle': 0.0, 'design_angle': -angcal, 'e1': 0, 'e2': 1,
                                                  'BC': 'Athos Self-Seeding'}), 0.16, 'relative')
            UN05.append(TM.generate('AFSS', 400, {'angle': 0.0, 'design_angle': angcal, 'e1': 1, 'e2': 0,
                                                  'BC': 'Athos Self-Seeding'}), 1, varC)
            UN05.append(TM.generate('DBPM-C5', 410), 0.18 + 0.00775, 'relative')
            UN05.append(TM.generate('QFF', 420), 0.06025 - 0.00775 + 0.005, 'relative')

        UN06 = TM.generate('UE38-Cell', 0, {'Name': 'UN06'})
        UN07 = TM.generate('UE38-Cell', 0, {'Name': 'UN07'})
        UN08 = TM.generate('UE38-Cell', 0, {'Name': 'UN08'})
        UN09 = TM.generate('UE38-Cell', 0, {'Name': 'UN09'})
        UN10 = TM.generate('UE38-Cell', 0, {'Name': 'UN10'})
        UN11 = TM.generate('UE38-Cell', 0, {'Name': 'UN11'})
        UN12 = TM.generate('UE38-Cell', 0, {'Name': 'UN12'})
        UN13 = TM.generate('UE38-Cell', 0, {'Name': 'UN13'})

        SS = LineContainer('UN14', -0.027 - 0.07275 + 0.005)
        varC = VariableContainer(0.38, 0)
        SS.append(TM.generate('AFSS', 100,
                              {'angle': 0.0, 'design_angle': angcal, 'e1': 0, 'e2': 1, 'BC': 'Athos Self-Seeding'}),
                  0.18, 'relative')
        SS.append(TM.generate('AFSS', 200,
                              {'angle': 0.0, 'design_angle': -angcal, 'e1': 1, 'e2': 0, 'BC': 'Athos Self-Seeding'}), 1,
                  varC)
        SS.append(TM.generate('AFSS', 300,
                              {'angle': 0.0, 'design_angle': -angcal, 'e1': 0, 'e2': 1, 'BC': 'Athos Self-Seeding'}),
                  0.16, 'relative')
        SS.append(TM.generate('AFSS', 400,
                              {'angle': 0.0, 'design_angle': angcal, 'e1': 1, 'e2': 0, 'BC': 'Athos Self-Seeding'}), 1,
                  varC)
        SS.append(TM.generate('DBPM-C5', 410), 0.18 + 0.00775, 'relative')
        SS.append(TM.generate('QFF', 420), 0.06025 - 0.00775 + 0.005, 'relative')

        UN14 = TM.generate('UE38-Cell', 0, {'Name': 'UN15'})
        UN15 = TM.generate('UE38-Cell', 0, {'Name': 'UN16'})
        UN16 = TM.generate('UE38-Cell', 0, {'Name': 'UN17'})
        UN17 = TM.generate('UE38-Cell', 0, {'Name': 'UN18'})
        UN18 = TM.generate('UE38-Cell', 0, {'Name': 'UN19'})
        UN19 = TM.generate('UE38-Cell', 0, {'Name': 'UN20'})
        UN20 = TM.generate('UE38-Cell', 0, {'Name': 'UN21'})
        UN21 = TM.generate('UE38-Cell-Last', 0, {'Name': 'UN22'})

        MA02 = LineContainer('MA02', 15 - 1.2591 + 1.3)
        MA02.append(TM.generate('QFF', 10), 1.51534, 'relative')
        MA02.append(TM.generate('QFF', 20), 2.183, 'relative')
        MA02.append(TM.generate('DBPM-C8', 30), 2.183 - 0.2, 'relative')
        MA02.append(TM.generate('QFF', 40), 0.1, 'relative')
        MA02.append(TM.generate('COL-Dechirper-H', 45), 0.1 + 0.6015 - 0.03, 'relative')
        MA02.append(TM.generate('QFF', 50), 2.183 - 1.1 - 0.6015 + 0.03, 'relative')
        MA02.append(TM.generate('DBPM-C8', 60), 2.183 - 0.2, 'relative')
        MA02.append(TM.generate('QFF', 70), 0.1, 'relative')
        if self.alt > 0:
            MA02.append(TM.generate('TDS X-Band', 100), 2.0535 - 0.22 + 0.06, 'relative')
            MA02.append(TM.generate('TDS X-Band', 200), 0.1, 'relative')  # currently disable the second cavity

        BD01 = LineContainer('BD01', 0)

        BD01.append(TM.generate('QFM', 10), 0.15 + 0.12 - 0.06, 'relative')
        BD01.append(TM.generate('DBPM-C16', 20), 1.1 - 0.3, 'relative')
        BD01.append(TM.generate('QFM', 30), 0.2, 'relative')
        BD01.append(TM.generate('SFQFM', 40), 0.1, 'relative')
        BD01.append(TM.generate('QFM', 50), 1.1 - 0.4, 'relative')
        BD01.append(TM.generate('DBPM-C16', 60), 1.1 - 0.3, 'relative')
        BD01.append(TM.generate('QFM', 70), 0.2, 'relative')
        BD01.append(TM.generate('SFQFM', 80), 0.1, 'relative')
        BD01.append(TM.generate('QFM', 90), 1.1 - 0.4, 'relative')
        BD01.append(TM.generate('DBAM-FS8', 95), 0.025 + 0.4735 + 0.0018 + 1 - 0.002998 + 0.0026, 'relative')
        BD01.append(TM.generate('DBPM-C16', 100),
                    3.1 - 0.0685 - 0.2 - 0.237 - 0.1 - 0.4753 - 0.025 - 1 + 0.002998 - 0.0026, 'relative')
        BD01.append(TM.generate('DWSC-C16', 110), 0.1, 'relative')
        BD01.append(TM.generate('DSCR-HR16', 120), 0.1, 'relative')
        BD01.append(TM.generate('AFD1', 200, {'angle': angle, 'design_angle': 8, 'e1': 0.5, 'e2': 0.5, 'branch': True}),
                    0.2165 + 0.05, 'relative')
        BD01.append(TM.generate('MKBR', 201), 0.0, 'relative')
        BD01.append(TM.generate('DSCR-OV38', 210), 5.5 - 1.2683 - 0.0044 - 0.94425, 'relative')
        BD01.append(TM.generate('AFP1', 300, {'angle': 0, 'design_angle': 0, 'e1': 0, 'e2': 1, 'Tilt': math.asin(1)}),
                    0.363 + 0.0064, 'relative')
        BD01.append(TM.generate('FE-Shielding', 305), 2.967 + 0.94425, 'relative')

        if (self.alt < 2):
            AtLine = [SY01, SY02, SY03, CL01, DI01, CB01, CB02, MA01, UN01, UN02, UN03, UN04, UN05, UN06, UN07, UN08,
                      UN09, UN10, UN11, UN12, UN13, SS, UN14, UN15, UN16, UN17, UN18, UN19, UN20, UN21, MA02, BD01]
        else:
            AtLine = [SY01, SY02, SY03, CL01, DI01, CB01, CB02, MA01, UN04, UN05, UN06, UN07, UN08, UN09, UN10, UN11,
                      UN12, UN13, SS, UN14, UN15, UN16, UN17, UN18, UN19, UN20, UN21, MA02, BD01]

        Athos = LineContainer('AT')
        Athos.append(AtLine)

        BD02 = LineContainer('BD02', 0)
        BD02.append(TM.generate('DBPM-C16', 10), 0.4 + 0.02072, 'relative')
        BD02.append(TM.generate('DICT-C16', 20), 0.12 - 0.0035, 'relative')
        LD = 1.1 / math.cos(8 * math.asin(1) / 90) - 0.92 - 0.1
        BD02.append(TM.generate('QFM', 30), LD + 0.01 - 0.02072 + 0.0035, 'relative')
        LD = LD + 0.3015
        BD02.append(TM.generate('DBPM-C16', 40), LD + 0.00317, 'relative')
        BD02.append(TM.generate('DSCR-HR16', 50), 0.1 + 0.01913, 'relative')
        LD = 19.478 / math.cos(8 * math.asin(1) / 90) - 0.0685 + 0.44 + 0.21 - 0.45
        BD02.append(TM.generate('Beam-Dump-Sat', 55), LD - 0.00317 - 0.01913, 'relative')
        AthosDump = LineContainer('AT')
        AthosDump.append(BD02, 0, 'relative')

        #
        # Porthos Branch for FCC experiment
        #
        # currntly not used so there will be no Porthos branch in the moment

        if self.alt > 10:
            SY01 = LineContainer('SY01', 0)
            #            SY01.append(Alignment({'dy':0.01,'Tag':'ALIG','index':1}))
            SY01.append(TM.generate('DBPM-C16', 10), 3.6, 'relative')
            SY01.append(TM.generate('QFM', 20), 0.1, 'relative')
            SY01.append(TM.generate('SFQFM', 30), 0.1, 'relative')
            SY01.append(TM.generate('QFM', 40), 3.4, 'relative')
            SY01.append(TM.generate('SFQFM', 50), 0.1, 'relative')
            SY01.append(TM.generate('DBPM-C16', 60), 0.2, 'relative')
            SY01.append(TM.generate('QFM', 70), 0.5, 'relative')
            SY01.append(TM.generate('SFQFM', 80), 0.1, 'relative')
            SY01.append(TM.generate('QFM', 90), 3.4, 'relative')
            SY01.append(TM.generate('SFQFM', 100), 0.1, 'relative')
            SY01.append(TM.generate('AFBC4', 200, {'angle': -3, 'design_angle': -2, 'e1': 0.5, 'e2': 0.5}), 3.4,
                        'relative')

            SY02 = LineContainer('SY02', 8.6 + 0.237)
            SY02.append(TM.generate('QFM', 10), 0.2, 'relative')
            SY02.append(TM.generate('SFQFM', 20), 0.1, 'relative')
            SY02.append(TM.generate('DBPM-C16', 30), 0.9, 'relative')
            SY02.append(TM.generate('QFM', 40), 0.1, 'relative')
            SY02.append(TM.generate('SFQFM', 50), 0.1, 'relative')
            SY02.append(TM.generate('QFM', 60), 1.1, 'relative')
            SY02.append(TM.generate('DBPM-C16', 70), 1.3, 'relative')
            SY02.append(TM.generate('QFM', 80), 0.1, 'relative')
            SY02.append(TM.generate('SFQFM', 90), 0.1, 'relative')
            SY02.append(TM.generate('DBPM-C16', 100), 0.6, 'relative')
            SY02.append(TM.generate('DSCR-OV16', 170), 0.1, 'relative')

            FC01 = LineContainer('FC01', 10.)
            FC01.append(TM.generate('FCC-Crystal', 10), 0.1, 'relative')
            FC01.append(TM.generate('AFSC', 100, {'angle': 0, 'design_angle': 0, 'e1': 0.5, 'e2': 0.5}), 0.1,
                        'relative')
            FC01.append(TM.generate('FCC-Target', 110), 1.2, 'absolute')
            FC01.append(TM.generate('WFAMD', 120), 1.3, 'absolute')
            FC01.append(TM.generate('FCC-RF-ACC', 200), 1.35, 'absolute')
            FC01.append(TM.generate('WFFCC', 210), 1.45, 'absolute')
            FC01.append(TM.generate('WFFCC', 220), 2.15, 'absolute')
            FC01.append(TM.generate('FCC-RF-ACC', 300), 2.75, 'absolute')
            FC01.append(TM.generate('WFFCC', 310), 2.85, 'absolute')
            FC01.append(TM.generate('WFFCC', 320), 3.55, 'absolute')
            FC01.append(TM.generate('DBPM-FCC', 330), 4.25, 'absolute')
            FC01.append(TM.generate('DSCR-FCC', 340), 0.1, 'relative')
            FC01.append(TM.generate('SHA-FCC', 400, {'angle': 0, 'design_angle': 0, 'e1': 0.5, 'e2': 0.5}), 0.1,
                        'relative')
            FC01.append(TM.generate('DSCR-SPEC-FCC', 410), 0.7, 'relative')
            FC01.append(TM.generate('Beam-Dump-FCC', 420), 0.2, 'relative')

        if self.alt > 10:
            dx = 0
            SY01 = LineContainer('SY01', 0)
            SY01.append(Alignment({'dy': 0.01, 'Tag': 'ALIG', 'index': 1}))
            SY01.append(TM.generate('QFM', 10), 4, 'relative')
            SY01.append(TM.generate('QFM', 20), 5, 'relative')
            SY01.append(TM.generate('QFM', 21), 1, 'relative')
            SY01.append(TM.generate('DBPM-C16', 25), 0.1, 'relative')
            SY01.append(TM.generate('QFM', 29), 0, 'relative')
            SY01.append(TM.generate('QFM', 30), 1, 'relative')
            SY01.append(TM.generate('QFM', 40), 5, 'relative')
            SY01.append(TM.generate('AFBC4', 100, {'angle': -2, 'design_angle': -2, 'e1': 0.5, 'e2': 0.5}), 4,
                        'relative')

            SY02 = LineContainer('SY02', 6.9)
            SY02.append(TM.generate('QFM', 10), 0.2, 'relative')
            SY02.append(TM.generate('AFL', 100, {'angle': 0.10800, 'design_angle': 0.10800, 'e1': 0, 'e2': 1.,
                                                 'Tilt': math.asin(1)}), 0.2, 'relative')
            SY02.append(TM.generate('QFM', 110), 1.29 - 0.45, 'relative')
            SY02.append(TM.generate('QFM', 120), 2.1, 'relative')
            SY02.append(TM.generate('AFL', 200, {'angle': -0.10800, 'design_angle': -0.10800, 'e1': 1, 'e2': 0.,
                                                 'Tilt': math.asin(1)}), 1.29 - 0.45, 'relative')

            SY03 = LineContainer('SY03', 22.044)
            dx = 3.5388
            SY03.append(TM.generate('QFM', 10), 0.1, 'relative')
            SY03.append(TM.generate('QFM', 20), dx, 'relative')
            SY03.append(TM.generate('QFM', 30), dx, 'relative')
            SY03.append(TM.generate('QFM', 40), dx, 'relative')
            SY03.append(TM.generate('QFM', 50), dx, 'relative')
            SY03.append(TM.generate('QFM', 60), dx, 'relative')

            SY04 = LineContainer('SY04', 24.9)
            SY04.append(TM.generate('AFBC4', 100, {'angle': 2, 'design_angle': 2, 'e1': 0.5, 'e2': 0.5}), 0.2,
                        'relative')
            SY04.append(TM.generate('QFM', 110), 4, 'relative')
            SY04.append(TM.generate('QFM', 120), 4, 'relative')
            SY04.append(TM.generate('DBPM-C16', 125), 1, 'relative')
            SY04.append(TM.generate('QFM', 130), 0.9, 'relative')
            SY04.append(TM.generate('QFM', 140), 4, 'relative')
            SY04.append(TM.generate('AFBC4', 200, {'angle': 2, 'design_angle': 2, 'e1': 0.5, 'e2': 0.5}), 4, 'relative')

            # straight layout constraints:
            # total length frm straight ahead to dump dipole: 160 m
            # distance between end of undulator to dump dipole: 25 m

            SY05 = LineContainer('SY05', 22.4)
            SY05.append(TM.generate('QFM', 10), 0.5, 'relative')
            SY05.append(TM.generate('QFM', 20), 10, 'relative')
            SY05.append(TM.generate('QFM', 30), 10, 'relative')

        PoLine = []
        if self.alt > 10:
            PoLine = [SY01, SY02, FC01]
        #            PoLine=[SY01,SY02]
        Porthos = LineContainer('PO')
        Porthos.append(PoLine)

        # construct final layout

        Linac = LineContainer('')
        Linac.append(Linac10, 0, 'relative')
        Linac.append(Linac20, 0, 'relative')
        Linac.append(Linac30, 0, 'relative')

        SwissFEL = LineContainer('S')

        # [BeamlineInstance, ParentIndex, BranchIndex, Remark]
        # BranchIndex=-1 -> added to the end of the parent line
        # BranchIndex=0  -> Beamline is the root element

        if self.alt < 10:
            PartsList = [[Injector, -1, 0, 'SwissFEL Injector'],  # 0
                         [Linac, 0, -1, 'SwissFEL Linac'],  # 1
                         [Aramis, 1, -1, 'Aramis beamline'],  # 2
                         [Athos, 1, 2, 'Athos beamline'],  # 3
                         [InjectorDump, 0, 1, 'SwissFEL Injector beam dump'],  # 4
                         [Linac1Dump, 1, 1, 'Linac1 beam dump'],  # 5
                         [AramisDump, 2, 1, 'Aramis beam dump'],  # 6
                         [AthosDump, 3, 1, 'Athos beam dump']]  # 7
        #                   [Porthos,     1, 3,'Porthos beamline']]             #8
        else:
            PartsList = [[Injector, -1, 0, 'SwissFEL Injector'],  # 0
                         [Linac, 0, -1, 'SwissFEL Linac'],  # 1
                         [Aramis, 1, -1, 'Aramis beamline'],  # 2
                         [Athos, 1, 2, 'Athos beamline'],  # 3
                         [InjectorDump, 0, 1, 'SwissFEL Injector beam dump'],  # 4
                         [Linac1Dump, 1, 1, 'Linac1 beam dump'],  # 5
                         [AramisDump, 2, 1, 'Aramis beam dump'],  # 6
                         [AthosDump, 3, 1, 'Athos beam dump'],  # 7
                         [Porthos, 1, 3, 'Porthos beamline']]  # 8

        return PartsList

