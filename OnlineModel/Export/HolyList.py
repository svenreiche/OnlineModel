from OnlineModel.Export.ExportBase import ExportBase
import math
import xlwt


class HolyList(ExportBase):
    """
    Generates an excel file with the calculated layout of SwissFEL, defining the proto holy list
    It lists each element with its PV name, position in the tunnel, Baugruppe and other information.
    """
    def __init__(self, file='HolyList.xls'):
        ExportBase.__init__(self)

        self.w = xlwt.Workbook()
        self.file = file  # output file name

        self.phase = 'Phase Final'

        self.positioncheck = {}

        self.catalogue = {}  # dictionary with all elements
        self.magcat = {}

        self.baugruppe = {}

        self.ws = self.w.add_sheet('SwissFEL')  # name of main tab
        self.wbend = self.w.add_sheet('SwissFEL Dipoles')  # name of extra tab describing the dipoles
        self.wbbg = self.w.add_sheet('Baugruppen')  # name of extra tab describing the dipoles

        # format of the excel sheet
        font0 = xlwt.Font()
        font0.name = 'Arial'
        font0.bold = True
        style0 = xlwt.XFStyle()
        style0.font = font0

        # column width
        self.ws.col(0).width = 3300
        self.ws.col(1).width = 2500
        self.ws.col(2).width = 1800
        self.ws.col(3).width = 1800
        self.ws.col(4).width = 2200
        self.ws.col(5).width = 2200
        self.ws.col(6).width = 2200
        self.ws.col(7).width = 2200
        self.ws.col(8).width = 2200
        self.ws.col(9).width = 2200
        self.ws.col(11).width = 4400
        self.ws.col(12).width = 2200
        self.ws.col(13).width = 2200
        self.ws.col(14).width = 3300

        self.wbend.col(0).width = 5500

        self.wbbg.col(0).width = 5500
        self.wbbg.col(1).width = 35500

        title = (
        'Domain', 'Prefix', 'Suffix', 'Index', 's (m)', 'z (m)', 'x (m)', 'y (m)', 'L (m)', 'Reference', 'Group',
        'Baugruppe', 'Roll', 'PS-Ch.', 'Phase')
        i = 0
        for name in title:
            self.ws.write(0, i, name, style0)
            i = i + 1
        self.row = 1

        title = (
        'Name', 'Length', 'Path Length', 'Radius', 'Angle', 'Entrance Model', 'Heading', 'Trans. Wander', 'Shift')
        i = 0
        for name in title:
            self.wbend.write(0, i, name, style0)
            i = i + 1
        self.bendrow = 1
        self.setRef(-0.1, -0.1)

        title = ('BAUGRUPPE', 'DESCRIPTION')
        i = 0
        for name in title:
            self.wbbg.write(0, i, name, style0)
            i = i + 1
        self.bgrow = 1

        self.style = xlwt.XFStyle()
        self.pattern = xlwt.Pattern()
        self.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        self.pattern.pattern_fore_colour = 1
        self.style.pattern = self.pattern

        self.orange = xlwt.Pattern()
        self.orange.pattern = xlwt.Pattern.SOLID_PATTERN
        self.orange.pattern_fore_colour = 51

        self.yellow = xlwt.Pattern()
        self.yellow.pattern = xlwt.Pattern.SOLID_PATTERN
        self.yellow.pattern_fore_colour = 43

        self.cyan = xlwt.Pattern()
        self.cyan.pattern = xlwt.Pattern.SOLID_PATTERN
        self.cyan.pattern_fore_colour = 41

        self.green = xlwt.Pattern()
        self.green.pattern = xlwt.Pattern.SOLID_PATTERN
        self.green.pattern_fore_colour = 42

        self.purple = xlwt.Pattern()
        self.purple.pattern = xlwt.Pattern.SOLID_PATTERN
        self.purple.pattern_fore_colour = 46

        self.lila = xlwt.Pattern()
        self.lila.pattern = xlwt.Pattern.SOLID_PATTERN
        self.lila.pattern_fore_colour = 45

    def writeBG(self):
        """
        Add a tab in the excel sheet to list all involved Baugruppen
        :return: Nothing
        """
        for key in sorted(self.baugruppe.keys()):
            self.wbbg.write(self.bgrow, 0, key, self.style)
            info = self.infobg(key)
            self.wbbg.write(self.bgrow, 1, info, self.style)
            self.bgrow += 1

    def append(self, phase_in='Phase 1'):
        """
        Add an internal table to hold the facility layout. Needed to combine current, planned and future phase in one sheet.
        :param phase_in: phase name for the current instance of the facility
        :return: Nothing
        """
        if self.phase == phase_in:
            return
        self.phase = phase_in
        self.catalogue = {}

    def close(self):
        """
        Writes out the accumulated data to an excel sheet.
        :return: Nothing
        """
        self.writeBG()
        self.w.save(self.file)

    def setRef(self, sin=0, zin=0, xin=0, yin=1.2, exin=0, eyin=0, ezin=1):
        self.s = sin
        self.z = zin
        self.x = xin
        self.y = yin
        # vector of direction
        self.ex = exin
        self.ey = eyin
        self.ez = ezin

        self.vertx = 0
        self.verty = 0
        self.vertz = 0
        self.verts = 0

    def swap(self):
        xtmp = self.x
        ytmp = self.y
        ztmp = self.z
        stmp = self.s
        self.x = self.vertx
        self.y = self.verty
        self.z = self.vertz
        self.s = self.verts
        self.vertx = xtmp
        self.verty = ytmp
        self.vertz = ztmp
        self.verts = stmp

    def write(self, elements):

        name = elements[0]
        reference = elements[2]
        elelength = elements[1]
        group = elements[3]

        if (name == 'SINEG01.MSOL010'):  ############### very first element
            self.setRef(-0.085, -0.085)

        pos_s = self.s
        pos_z = self.z

        if name in self.positioncheck:
            alt_z = self.positioncheck[name]
            if (abs(alt_z - pos_z) > 1e-6):
                print('Element:', name, 'by', alt_z - pos_z)
        else:
            self.positioncheck[name] = pos_z

        if name in self.catalogue:
            return

        if name[8:9] == 'S':
            group = 'Safety'

        if name[0:12] == 'SINBC02.DCOL' or name[0:12] == 'S10BC02.DCOL' or name[0:12] == 'S10BC02.DSFH':
            reference = 'Center'
            pos_s = pos_s + 0.5 * elelength
            pos_z = pos_z + 0.5 * elelength

        if name[0:12] == 'SINBC02.DSCR' or name[0:12] == 'S10BC02.DSCR':
            elelength = 0.28
            pos_s = pos_s - 0.09
            pos_z = pos_z - 0.09

        domain = 'INJECTOR'
        if name[1:3] == '10':
            domain = 'LINAC1'
        if name[1:3] == '20':
            domain = 'LINAC2'
        if name[1:3] == '30':
            domain = 'LINAC3'
        if name[1:3] == 'AR':
            domain = 'ARAMIS-U15'
        if name[1:3] == 'AT':
            domain = 'ATHOS-U40'
        if name[1:3] == 'PO':
            domain = 'PORTHOS'

        phasetxt = self.phase

        self.style.pattern = self.orange

        if group == 'Diagnostics':
            self.style.pattern = self.yellow
        if group == 'RF':
            self.style.pattern = self.cyan
        if group == 'Vacuum' or group == 'Safety':
            self.style.pattern = self.green
        if group == 'ID':
            self.style.pattern = self.purple
        if group == 'Photonics':
            self.style.pattern = self.lila

        self.ws.write(self.row, 0, domain, self.style)
        self.ws.write(self.row, 1, name[0:7], self.style)
        self.ws.write(self.row, 2, name[8:12], self.style)
        self.style.num_format_str = '000'
        self.ws.write(self.row, 3, int(name[12:15]), self.style)
        self.style.num_format_str = '0.0000'
        self.ws.write(self.row, 4, pos_s, self.style)
        self.ws.write(self.row, 5, pos_z, self.style)
        self.ws.write(self.row, 6, self.x, self.style)
        self.ws.write(self.row, 7, self.y, self.style)
        self.style.num_format_str = 'General'
        self.ws.write(self.row, 8, elelength, self.style)
        self.ws.write(self.row, 9, reference, self.style)
        self.ws.write(self.row, 10, group, self.style)
        self.ws.write(self.row, 11, elements[5], self.style)
        self.ws.write(self.row, 12, elements[6], self.style)
        self.ws.write(self.row, 13, elements[7], self.style)
        self.ws.write(self.row, 14, phasetxt, self.style)

        self.catalogue[name] = 1
        bg = elements[5]
        if not bg in self.baugruppe.keys():
            self.baugruppe[bg] = 1

        self.row = self.row + 1

        if name[0:12] == 'SINBC02.DSCR' or name[0:12] == 'S10BC02.DSCR':
            self.ws.write(self.row, 0, domain, self.style)
            self.ws.write(self.row, 1, name[0:7], self.style)
            self.ws.write(self.row, 2, 'DALA', self.style)
            self.style.num_format_str = '000'
            self.ws.write(self.row, 3, int(name[12:15]), self.style)
            self.style.num_format_str = '0.0000'
            self.ws.write(self.row, 4, pos_s, self.style)
            self.ws.write(self.row, 5, pos_z, self.style)
            self.ws.write(self.row, 6, self.x, self.style)
            self.ws.write(self.row, 7, self.y, self.style)
            self.style.num_format_str = 'General'
            self.ws.write(self.row, 8, elelength, self.style)
            self.ws.write(self.row, 9, reference, self.style)
            self.ws.write(self.row, 10, group, self.style)
            self.ws.write(self.row, 11, 'DALA', self.style)
            self.ws.write(self.row, 12, elements[6], self.style)
            self.ws.write(self.row, 13, elements[7], self.style)
            self.ws.write(self.row, 14, phasetxt, self.style)
            self.row = self.row + 1

    def writeBendTab(self, elements):
        name = str(elements[0])

        if name in self.magcat:
            return
        off = elements[8]
        if (name.find('UN') > -1):
            off = 0
            of = 0.149
            if (name.find('SARUN') > -1):
                of = -0.008
            if (name.find('200') > -1 or name.find('300') > -1):
                off = of
        self.style.pattern = self.orange
        self.wbend.write(self.bendrow, 0, name.replace('.', '-'), self.style)
        i = 1;
        self.style.num_format_str = '0.0000'

        while (i < 8):
            self.wbend.write(self.bendrow, i, elements[i], self.style)
            i = i + 1
        self.wbend.write(self.bendrow, 8, off, self.style)
        self.bendrow = self.bendrow + 1
        self.style.num_format_str = 'General'
        self.magcat[name] = 1

    # ----------------------------------------
    # sepcific elements

    def isType(self, name):
        if (name.find('holylist') > -1):
            return 1
        else:
            return 0

    def writeLine(self, ele, seq):
        return

    def writeDrift(self, s):
        self.advance(s, 0)

    def writeAlignment(self, ele):
        # print info of the element and advances the layout position over the reserved length
        if 'dx' in ele.__dict__:
            self.x = self.x + ele.dx
        if 'dy' in ele.__dict__:
            self.y = self.y + ele.dy
        self.advance(ele.getResLength(), 0)

    def writeMarker(self, ele):
        return

    def writeVacuum(self, ele):  # all components, which have a well defined vacuum vessel.
        self.write((ele.Name, ele.LengthRes, 'Start', ele.Group, ele.Tag, ele.Baugruppe, 0, 0))
        self.advance(ele.LengthRes, 0)

    def writeRF(self, ele):
        self.writeVacuum(ele)

    def writeDiagnostic(self, ele):
        self.writeVacuum(ele)

    def writeUndulator(self, ele):
        self.writeMagnets(ele)

    def writeCorrector(self, ele):
        self.writeMagnets(ele)

    def writeQuadrupole(self, ele):
        self.writeMagnets(ele)

    def writeSextupole(self, ele):
        self.writeMagnets(ele)

    def writeSolenoid(self, ele):
        self.writeMagnets(ele)

    def writeMagnets(self, ele):
        channels = 0
        if 'k1' in ele.__dict__:
            channels = channels + 1
        if 'k2' in ele.__dict__:
            channels = channels + 1
        if 'ks' in ele.__dict__:
            channels = channels + 1
        if 'corx' in ele.__dict__:
            channels = channels + 1
        if 'cory' in ele.__dict__:
            channels = channels + 1
        if 'cor' in ele.__dict__:
            channels = channels + 1
        if ele.Baugruppe == 'QFU':
            channels = channels - 1
        if ele.Baugruppe == 'QFUE':
            channels = channels - 1
        if ele.Baugruppe == 'UE38-DELAY':
            channels = channels + 1
        # print info of the element and advances the layout position over the reserved length
        self.advance(ele.sRef + ele.Length * 0.5, 0)
        self.write(
            (ele.Name, ele.Length, 'Center', ele.Group, ele.Tag, ele.Baugruppe, ele.Tilt * 90 / math.asin(1), channels))
        self.advance(ele.LengthRes - ele.sRef - ele.Length * 0.5, 0)

    def writeBend(self, ele):
        # print info of the element and advances the layout position over the reserved length
        channels = 1
        if ele.Baugruppe[0:3] == 'AFP':
            channels = 0
        if 'cor' in ele.__dict__:
            channels = channels + 1
        self.advance(ele.sRef, 0)
        if (ele.design_angle == 0):
            self.advance(0.5 * ele.getLength(), 0)
            self.writeBendTab((ele.Name, ele.Length, ele.getLength(), '', 0, 0, 0, 0, 0))
            self.write((ele.Name, ele.getLength(), 'Vertex', ele.Group, ele.Tag, ele.Baugruppe,
                        ele.Tilt * 90 / math.asin(1), channels))
            self.advance(ele.getResLength() - ele.sRef - 0.5 * ele.getLength(), 0)
        else:
            self.advance(ele.sRef, 0)
            xtmp = self.x
            ytmp = self.y
            ztmp = self.z
            stmp = self.s
            extmp = self.ex
            eytmp = self.ey
            eztmp = self.ez
            angletmp = ele.angle
            ele.angle = ele.design_angle
            # advance according to design angle
            angrad = math.asin(1) * ele.angle / 90.
            Lpath = ele.getLength()
            self.advance(Lpath, angrad, ele.Tilt)
            self.swap()
            R = ele.getLength() / angrad;
            dR = R * (1 - math.cos(angrad))
            shift = 0.5
            if (ele.e1 == 0.5):
                dR = R * (1 - math.cos(angrad * 0.5))
                shift = -0.5
            self.writeBendTab(
                (ele.Name, ele.Length, ele.getLength(), abs(R), ele.angle, ele.e1, ele.angle * ele.e1, dR, shift * dR))
            self.write((ele.Name, ele.Length, 'Vertex', ele.Group, ele.Tag, ele.Baugruppe, ele.Tilt * 90 / math.asin(1),
                        channels))
            self.swap()

            # restore position before dipole and then advance according to given angle (this matters for branching point dipoles
            self.x = xtmp
            self.y = ytmp
            self.z = ztmp
            self.s = stmp
            self.ex = extmp
            self.ey = eytmp
            self.ez = eztmp
            ele.angle = angletmp

            angrad = math.asin(1) * ele.angle / 90.
            Lpath = ele.getLength()
            self.advance(Lpath, angrad, ele.Tilt)
            self.advance(ele.getResLength() - ele.sRef - Lpath, 0)

    def advance(self, L, angle=0, tilt=0):

        self.vertx = 0
        self.verty = 0
        self.vertz = 0
        self.verts = self.s
        self.s = self.s + L
        if angle == 0:
            self.x = self.x + L * self.ex
            self.y = self.y + L * self.ey
            self.z = self.z + L * self.ez
        else:
            # save initial coordinates
            xtmp = self.x
            ytmp = self.y
            ztmp = self.z
            # radius
            R = L / angle
            # rotation vector - default around y axis
            Rproj = self.ey  # R dot e = Ry*ey=ey
            Rx = -Rproj * self.ex
            Ry = 1 - Rproj * self.ey
            Rz = -Rproj * self.ez
            # Orthonormal vector to direction of propagation and rotation axis
            Ox = Ry * self.ez - Rz * self.ey
            Oy = Rz * self.ex - Rx * self.ez
            Oz = Rx * self.ey - Ry * self.ex
            Rnorm = math.sqrt(Rx * Rx + Ry * Ry + Rz * Rz)
            Onorm = math.sqrt(Ox * Ox + Oy * Oy + Oz * Oz)
            Rx = Rx / Rnorm
            Ry = Ry / Rnorm
            Rz = Rz / Rnorm
            Ox = Ox / Onorm
            Oy = Oy / Onorm
            Oz = Oz / Onorm
            # Rot Vector is the axis of rotation and Ort vector pointing to the origin of the rotation
            Ortx = Ox * math.cos(tilt) - Rx * math.sin(tilt)
            Orty = Oy * math.cos(tilt) - Ry * math.sin(tilt)
            Ortz = Oz * math.cos(tilt) - Rz * math.sin(tilt)
            # the origin of the rotation
            X0 = self.x + R * Ortx
            Y0 = self.y + R * Orty
            Z0 = self.z + R * Ortz
            # rotation

            self.vertx = X0 - R * (Ortx * math.cos(angle * 0.5) - self.ex * math.sin(angle * 0.5)) / math.cos(
                angle * 0.5)
            self.verty = Y0 - R * (Orty * math.cos(angle * 0.5) - self.ey * math.sin(angle * 0.5)) / math.cos(
                angle * 0.5)
            self.vertz = Z0 - R * (Ortz * math.cos(angle * 0.5) - self.ez * math.sin(angle * 0.5)) / math.cos(
                angle * 0.5)
            self.x = X0 - R * (Ortx * math.cos(angle) - self.ex * math.sin(angle))
            self.y = Y0 - R * (Orty * math.cos(angle) - self.ey * math.sin(angle))
            self.z = Z0 - R * (Ortz * math.cos(angle) - self.ez * math.sin(angle))
            self.ex = (self.ex * math.cos(angle) + Ortx * math.sin(angle))
            self.ey = (self.ey * math.cos(angle) + Orty * math.sin(angle))
            self.ez = (self.ez * math.cos(angle) + Ortz * math.sin(angle))
            # calculate vertex
            ds = (self.vertx - xtmp) * (self.vertx - xtmp) + (self.verty - ytmp) * (self.verty - ytmp) + (
                        self.vertz - ztmp) * (self.vertz - ztmp)
            self.verts = self.verts + math.sqrt(ds)

    def infobg(self, bg):
        if 'DECHIRPER' in bg:
            pol = 'horizontal'
            if '-V' in bg:
                pol = 'vertical'
            return 'Dechirper - %s gap - 1m long' % pol
        if 'AF' in bg[0:2]:
            inf = 'Dipole'
            if 'AFSC' in bg:
                return 'SC ' + inf + ' in FCC Positron Source'
            if 'BC1' in bg:
                return inf + ' Injector Bunch Compressor'
            if 'BC3' in bg:
                return inf + ' Linac Bunch Compressor'
            if 'BC4' in bg:
                return inf + ' Porthos Switchyard'
            if 'AFL' in bg:
                return inf + ' Laser Heater'
            if 'AFSS' in bg:
                return inf + ' Two-Color/Hero/Self-seeding'
            if 'AFS' in bg:
                return inf + ' Septum of Athos Switchyard'
            if 'AFDL' in bg:
                return inf + ' Injector Dump'
            if 'D1' in bg:
                return inf + ' Main Dump'
            if 'P1' in bg:
                return inf + ' Beam Stopper (permanent magnet)'
        if 'BEAM' in bg:
            inf = 'Beam'
            if 'DUMP' in bg:
                inf = inf + ' Dump -'
            else:
                inf = inf + ' Stopper -'
            if 'SIN' in bg:
                inf = inf + ' Gun'
            elif 'S10' in bg:
                inf = inf + ' Linac 1'
            elif 'SAR' in bg:
                inf = inf + ' Aramis'
            elif 'FCC' in bg:
                inf = inf + ' FCC Positron Source'
            else:
                inf = inf + ' Athos'
            return inf
        if 'BAND' in bg:
            inf = 'Accelerating RF Structure ' + bg[0:1] + '-Band'
            if 'TDS' in bg:
                inf = 'Transverse Deflecting RF Structure ' + bg[0:1] + '-Band'
            if 'FCC' in bg:
                inf = inf + ' for FCC Positron Source'
            return inf
        if 'DBPM' in bg:
            if 'FCC' in bg:
                return 'Two-Frequency Beam Position Monitor to Distinguish Electrons and Positrons'
            return 'Beam Position Monitor with ' + bg[6:] + ' mm Aperture'
        if 'DWSC' in bg:
            inf = 'Wire Scanner with ' + bg[6:] + ' mm Aperture'
            if '-AL' in bg:
                inf = 'Wire Scanner with ' + bg[6:-3] + ' mm Aperture and Aluminum Foil'
            return inf
        if 'DICT' in bg:
            inf = 'Integrating Current Transformer with ' + bg[6:] + ' mm Aperture'
            if '-GUN' in bg:
                inf = 'Integrating Current Transformer with ' + bg[6:-4] + ' mm Aperture (slow signal)'
            return inf
        if 'DSCR' in bg:
            inf = 'Screen (Profile Monitor)'
            if 'FCC' in bg:
                if 'SPEC' in bg:
                    inf = 'Spectrometer ' + inf
                return inf + ' for FCC Positron Source'
            if '-HR' in bg:
                return 'High Resolution ' + inf + ' with ' + bg[7:] + ' mm Aperture'
            if '-OV' in bg:
                return 'Overview ' + inf + ' with ' + bg[7:] + ' mm Aperture'
            if 'LH' in bg:
                return inf + ' for Overlap in Laser Heater with ' + bg[7:] + ' mm Aperture'
            if 'BC' in bg:
                return inf + ' in Bunch Compressor'
            if 'LE' in bg:
                return inf + ' in Gun Section with ' + bg[7:] + ' mm Aperture'
            return inf
        if 'RES-KICK' in bg:
            tag = 'Resonant Kicker - AC Component'
            if '-DC' in bg:
                tag = 'Resonant Kicker - AC Component'
            return tag
        if 'QF' in bg[0:2]:
            tag = 'Quadrupole ' + bg[0:3]
            if 'QFC' in bg:
                tag = 'Corrector Quadrupole'
                if 'QFCOR' in bg:
                    tag = 'Gun ' + tag
            if 'SKEW' in bg:
                tag = tag + ' (skewed)'
            if 'QFDM' in bg:
                tag = tag + ' (reduced corrector strength)'
            if 'QFUE' in bg:
                return 'Alignment Quadrupole for Athos (permanent magnet)'
            if 'QFU' in bg:
                return 'Alignment Quadrupole for Aramis (permanent magnet)'
            return tag
        if 'COL' in bg:
            tag = 'Energy Collimator (horizontal gap)'
            if 'VERT' in bg:
                tag = 'Vertical Collimator (beam spoiler)'
            return tag
        if 'U' in bg[0:1]:
            if 'UE' in bg:
                tag = 'Athos Undulator Module (Apple-X with 38 mm period)'
                if 'DELAY' in bg:
                    tag = 'Athos Delaying Chicane'
                return tag
            if 'U15' in bg:
                tag = 'Aramis Undulator Module (planar with 15 mm period)'
                if 'PS' in bg:
                    tag = 'Aramis Phase Shifter'
                return tag
            if 'U200' in bg:
                return 'Single Period Undulator (planar with 200 mm period)'
            if 'U50' in bg:
                return 'Laser Heater Modulator (planar with 50 mm period)'
            return 'Undulator'
        if 'WF' in bg[0:2]:
            if 'FCC' in bg:
                return 'Solenoid for FCC Positron Accelerating Structures'
            if 'WFAMD' in bg:
                return 'Solenoid for Adiabatic Matching of FCC Positron Source'
            return 'Solenoid ' + bg
        if 'DALA' in bg:
            return 'Input Port for Alignment Laser'
        if 'DBAM' in bg:
            return 'Beam Arrival Monitor for ' + bg[5:7].lower() + ' Bunch Length with ' + bg[7:] + ' mm Aperture'
        if 'SCRAPER' in bg:
            return 'Horizontal Scraper in Bunch Compressors'
        if 'DBCM' in bg:
            return 'Bunch Compression Monitor for ' + bg[5:] + ' Frequency Range'
        if 'DCDR' in bg:
            return 'Coherent Diffraction Monitor'
        if 'DFCP' in bg:
            return 'Faraday Cup'
        if 'DHVS' in bg:
            return 'Horizontal and Vertical Slits (emittance spoiler)'
        if 'DLAC' in bg:
            return 'Laser Acceleration on a Chip (ACHIP) Box in Injector'
        if 'LASER-ACC' in bg:
            return 'Laser Acceleration on a Chip (ACHIP) Box in Athos Switchyard'
        if 'DSRM' in bg:
            tag = 'Synchrotron Radiation Monitor in the Visible Regime'
            if 'UV' in bg:
                tag = 'Synchrotron Radiation Monitor in the UV Regime'
            return tag
        if 'DWCM' in bg:
            return 'Wall Current Monitor'
        if 'HF' in bg:
            return 'Sextupole ' + bg
        if 'LC-GUN' in bg:
            return 'Laser Port for RF Gun'
        if 'LH-LASER' in bg:
            return 'Laser Port for Laser Heater'
        if 'PSI-GUN' in bg:
            return 'PSI Photo-electron RF Gun'
        if 'SF' in bg[0:2]:
            tag = 'Corrector Magnet ' + bg
            if 'SFC' in bg:
                tag = tag + ' for QFA Quadrupole'
            if 'SFQFM' in bg:
                tag = tag + ' for QFM Quadrupole'
            if 'SFUE' in bg:
                tag = 'Undulator ' + tag + ' for Athos Undulator Module'
            elif 'SFU' in bg:
                tag = 'Undulator ' + tag + ' for Aramis Undulator Module'
            return tag
        if 'SHA' in bg:
            if 'SPEC' in bg:
                return 'Dipole Spectrometer for FCC Positron Source'
            return 'Dipole Spectrometer after Gun'
        if 'SLOT' in bg:
            tag = 'Slotted Foil with Horizontal Mover'
            if '-V' in bg:
                tag = 'Slotted Foil with Vertical Mover'
            return tag
        if 'FCC' in bg[0:4]:
            tag = 'Crystal Target for FCC Positron Source'
            if 'Target' in bg:
                tag = 'Main Target for FCC Positron Source'
            return tag
        return 'unknown'
