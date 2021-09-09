import math
from OnlineModel.Export.ExportBase import ExportBase

class MadXLattice(ExportBase):

    def __init__(self, switch=1):
        ExportBase.__init__(self)
        self.cc = []  # this holds the lattice in form
        self.invertMatrix = False

    def demandMapID(self):
        return 1

    def write(self, line):
        if isinstance(line, list):
            for l in line:
                self.write(l)
        else:
            self.cc.append(line)

    def clear(self):
        self.cc = []

    # ----------------
    #  the element specific format

    def isType(self, name):
        if (name.find('madx') > -1):
            return 1
        else:
            return 0

    def writeLine(self, line, seq):

        if (len(line.Name) == 7):
            SecName = line.Name
            self.write("%s.START: MARKER;\n" % (SecName))
            self.write("%s.END: MARKER;\n" % (SecName))
            self.write("\n%s: SEQUENCE, REFER=centre, L=%14.10f;\n" % (SecName, line.getResLength()))
            self.write("   %s, AT=%14.10f;\n" % (SecName + '.START', 0))
            for ele in seq:
                if 'MADshift' in ele.__dict__:
                    spos = line.position(ele) + ele.sRef + ele.getLength() * 0.5 + ele.MADshift
                else:
                    spos = line.position(ele) + ele.sRef + ele.getLength() * 0.5
                if 'Overlap' in ele.__dict__:
                    if ele.Overlap == 0:
                        self.write("   %s, AT=%f;\n" % (ele.Name, spos))
                else:
                    if ('MQUA' in ele.Name) and ('corx' not in ele.__dict__):
                        self.write("   %s$START, AT=%f;\n" % (ele.Name, spos - ele.getLength() / 2.0))
                        self.write("   %s, AT=%f;\n" % (ele.Name, spos))
                        self.write("   %s$END, AT=%f;\n" % (ele.Name, spos + ele.getLength() / 2.0))
                    else:
                        # The case applies for most elements.
                        self.write("   %s, AT=%f;\n" % (ele.Name, spos))
            self.write("   %s, AT=%f;\n" % (SecName + '.END', line.getResLength()))
            self.write("ENDSEQUENCE;\n\n")
            return
        else:
            # self.MapIndx=None ##################################3 where is self.MapIndex defined???
            # It is defined in OMType... It is not a good implementation, I know... Masa 21.11.2014
            length = 0
            for subline in seq:
                length = length + subline['L']
            if not self.MapIndx:  # had to add this to make it work for me
                if self.MapIndx == 0:
                    '0 is not None'
                else:
                    self.MapIndx = None
            if self.MapIndx != None:  # Writing out Facility
                SecName = 'SEQ' + str(abs(self.MapIndx))
                if self.switch:
                    self.write("  %s.START: Marker;\n" % (SecName))
                    self.write("  %s.END: Marker;\n" % (SecName))
                self.write("\n%s: SEQUENCE, REFER=centre, L=%f;\n" % (SecName, length))
            else:
                self.write("\nSWISSFEL: SEQUENCE, REFER=centre, L=%f;\n" % (length))
            tlength = length
            if self.MapIndx and self.switch:
                self.write("  SEQ%s.START, AT=0.0;\n" % (str(abs(self.MapIndx))))
            length = 0
            for subline in seq:
                SecName = subline['Name']
                self.write("   %s, AT=%f;\n" % (SecName, length + subline['L'] * 0.5))
                length = length + subline['L']
            if self.MapIndx != None and self.switch:
                self.write("  SEQ%s.END, AT=%f;\n" % (str(abs(self.MapIndx)), tlength))
            self.write("ENDSEQUENCE;\n\n")
            self.MapIndx = None
        return

    def writeDrift(self, ele):
        return

    def writeVacuum(self, ele):
        self.writeMarker(ele)
        return

    def writeAlignment(self, ele):
        self.writeMarker(ele)  # this line is needed, no?
        return

    def writeBend(self, ele):
        Lpath = ele.getLength()
        angrad = ele.angle * math.asin(1) / 90

        angradcor = angrad
        if 'cor' in ele.__dict__:
            angradcor = angrad + ele.cor
        self.write("%s.angle := %f;\n" % (ele.Name, angradcor))
        self.write(
            "%s: SBEND, L=%f, ANGLE:=%s.angle, FINT=0.5, HGAP=0.015, TILT=%f, E1=%f*%s.angle, E2=%f*%s.angle;\n"
            % (ele.Name, Lpath, ele.Name, ele.Tilt, ele.e1, ele.Name, ele.e2, ele.Name))

    def writeQuadrupole(self, ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap == 1:
                return
        if ('corx' in ele.__dict__) or ('cory' in ele.__dict__):
            self.write("%s.k1 := %f;\n" % (ele.Name, ele.k1))
            if 'corx' in ele.__dict__:
                self.write("%s.corx := %f;\n" % (ele.Name, ele.corx))
            if 'cory' in ele.__dict__:
                self.write("%s.cory := %f;\n" % (ele.Name, ele.cory))
            self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name, ele.Length))
            self.write("   %s.q1:  QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f, AT=%f;\n" % (
            ele.Name, ele.Length * 0.5, ele.Name, ele.Tilt, 0.25 * ele.Length))
            if 'corx' in ele.__dict__:
                # self.write("   %s.cx: HKICKER, L=0, kick:=%s.corx, AT=%f;\n" % (ele.Name,ele.Name,ele.Length*0.5)) # This change ahs to be discussed
                self.write("   %s.cx: HKICKER, L=0, kick:=%s.corx, AT=%f;\n" % (
                ele.Name, ele.Name.replace('MQUA', 'MCRX'), ele.Length * 0.5))
            if 'cory' in ele.__dict__:
                self.write("   %s.cy: VKICKER, L=0, kick:=%s.cory, AT=%f;\n" % (
                ele.Name, ele.Name.replace('MQUA', 'MCRY'), ele.Length * 0.5))  # This change ahs to be discussed
            self.write("   %s.q2:  QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f, at=%f;\n" % (
            ele.Name, ele.Length * 0.5, ele.Name, ele.Tilt, 0.75 * ele.Length))
            self.write("ENDSEQUENCE;\n")
        else:
            self.write("%s$START: MARKER, L=0.0;\n" % (ele.Name))
            self.write("%s.k1 := %f;\n" % (ele.Name, ele.k1))
            self.write("%s: QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f;\n" % (ele.Name, ele.Length, ele.Name, ele.Tilt))
            self.write("%s$END: MARKER, L=0.0;\n" % (ele.Name))

    def writeCorrector(self, ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap == 1:
                return
        shift = 0
        if 'MADshift' in ele.__dict__:
            shift = ele.MADshift
        if 'MADthin' in ele.__dict__:
            if ele.MADthin == 1:
                Length = 0
            else:
                Length = ele.Length
        else:
            Length = ele.Length

        if ('corx' in ele.__dict__) or ('cory' in ele.__dict__):
            if 'corx' in ele.__dict__:
                self.write("%s.corx := %f;\n" % (ele.Name.replace('MCOR', 'MCRX'), ele.corx))
            if 'cory' in ele.__dict__:
                self.write("%s.cory := %f;\n" % (ele.Name.replace('MCOR', 'MCRY'), ele.cory))
            if Length > 0:
                self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name, ele.LengthRes))
                if ('corx' in ele.__dict__) and ('cory' in ele.__dict__):
                    self.write("   %s.cxy: KICKER, L=%s, hkick:=%s.corx, vkick:=%s.cory, AT=%f;\n" % (
                    ele.Name, ele.Length, ele.Name.replace('MCOR', 'MCRX'), ele.Name.replace('MCOR', 'MCRY'),
                    ele.sRef + ele.Length * 0.5))
                elif 'corx' in ele.__dict__:
                    self.write("   %s.cx: HKICKER, L=%s, kick:=%s.corx, AT=%f;\n" % (
                    ele.Name, ele.Length, ele.Name.replace('MCOR', 'MCRX'), ele.sRef + ele.Length * 0.5))
                elif 'cory' in ele.__dict__:
                    self.write("   %s.cy: VKICKER, L=%s, kick:=%s.cory, AT=%f;\n" % (
                    ele.Name, ele.Length, ele.Name.replace('MCOR', 'MCRY'), ele.sRef + ele.Length * 0.5))
                self.write("ENDSEQUENCE;\n")
            else:
                if ('corx' in ele.__dict__) and ('cory' in ele.__dict__):
                    self.write("%s: KICKER, L=0, hkick:=%s.corx, vkick:=%s.cory;\n" % (
                    ele.Name, ele.Name.replace('MCOR', 'MCRX'), ele.Name.replace('MCOR', 'MCRY')))
                elif 'corx' in ele.__dict__:
                    self.write("%s: HKICKER, L=0, kick:=%s.corx;\n" % (ele.Name, ele.Name.replace('MCOR', 'MCRX')))
                elif 'cory' in ele.__dict__:
                    self.write("%s: VKICKER, L=0, kick:=%s.cory;\n" % (ele.Name, ele.Name.replace('MCOR', 'MCRY')))

            return ele.Name

    def writeSextupole(self, ele):
        self.write("%s.k2 := %f;\n" % (ele.Name, ele.k2))
        self.write("%s: SEXTUPOLE, L=%f, k2:=%s.k2, tilt=%f;\n" % (ele.Name, ele.Length, ele.Name, ele.Tilt))

    def writeRF(self, ele):
        #        print(ele.Name,ele.p0)
        p0 = ele.p0
        # dP=ele.Gradient/511000*math.sin(ele.Phase*math.asin(1)/90)*ele.Length
        if 'dP' in ele.__dict__:  # ele.dP is used??
            dP = ele.dP
        if ele.Gradient:
            ## p from Energy manager is in units of eV          => MeV since 29.06.2015
            dP = ele.Gradient * math.sin(ele.Phase * math.asin(1) / 90) * ele.Length
        else:
            dP = 0

        if 'TDS' in ele.Name:
            # This simplified implementation is to compute the beam trajectory only
            # Need to define all the matrix element if used for other purpose...
            m11 = 1
            m12 = ele.Length
            m21 = 0
            m22 = p0 / (p0 + dP)
            m33 = 1
            m34 = ele.Length
            m43 = 0
            m44 = 1
            m45 = dP / p0  # and set t=1.0 for the initial condition
            if self.invertMatrix:
                m34 = -m34
                m22 = (p0 + dP) / p0
                m12 = -m12 * (p0 + dP) / p0
                m45 = -dP / p0
        elif dP == 0 or ('RGUN' in ele.Name) or p0 <= 0 or (p0 + dP) < 0:
            # self.writeMarker(ele)
            # return
            m11 = 1.0
            m12 = ele.Length
            m21 = 0.0
            m22 = 1.0
            if self.invertMatrix:
                m12 = -m12
        else:
            m11 = 1
            m12 = p0 * ele.Length / dP * math.log((p0 + dP) / p0)
            m21 = 0
            m22 = p0 / (p0 + dP)
            e11 = 1
            e12 = 0
            e21 = -0.5 * dP / p0 / ele.Length
            e22 = 1
            d11 = m11 * e11 + m12 * e21
            d12 = m11 * e12 + m12 * e22
            d21 = m21 * e11 + m22 * e21
            d22 = m21 * e12 + m22 * e22
            e21 = 0.5 * dP / (p0 + dP) / ele.Length
            m11 = e11 * d11 + e12 * d21
            m12 = e11 * d12 + e12 * d22
            m21 = e21 * d11 + e22 * d21
            m22 = e21 * d12 + e22 * d22
            if self.invertMatrix:
                detm = m11 * m22 - m12 * m21
                m12 = -m12 / detm
                m21 = -m21 / detm
                tmp = m22 / detm
                m22 = m11 / detm
                m11 = tmp
        self.write("%s: MATRIX, L=%f,\n" % (ele.Name, ele.Length))
        self.write("   RM11=%f,\n" % (m11))
        self.write("   RM12=%f,\n" % (m12))
        self.write("   RM21=%f,\n" % (m21))
        self.write("   RM22=%f,\n" % (m22))
        if 'TDS' in ele.Name:
            self.write("   RM33=%f,\n" % (m33))
            self.write("   RM34=%f,\n" % (m34))
            self.write("   RM43=%f,\n" % (m43))
            self.write("   RM44=%f;\n" % (m44))
            self.write("   RM45=%f;\n" % (m45))
        else:
            self.write("   RM33=%f,\n" % (m11))
            self.write("   RM34=%f,\n" % (m12))
            self.write("   RM43=%f,\n" % (m21))
            self.write("   RM44=%f;\n" % (m22))

    def writeUndulator(self, ele):
        # Note that the value of p0 is given in eV
        p0 = ele.p0 / 511000
        kmax = ele.K * ele.ku / p0
        kx = ele.kx * 0.5 * kmax * kmax
        ky = ele.ky * 0.5 * kmax * kmax
        if kx > 0:
            omg = math.sqrt(kx) * ele.Length
            m11 = math.cos(omg)
            m12 = math.sin(omg) / math.sqrt(kx)
            m21 = -math.sin(omg) * math.sqrt(kx)
            m22 = math.cos(omg)
        else:
            if kx < 0:
                omg = math.sqrt(kx) * ele.Length
                m11 = math.cosh(omg)
                m12 = math.sinh(omg) / math.sqrt(kx)
                m21 = math.sinh(omg) * math.sqrt(kx)
                m22 = math.cosh(omg)
            else:
                m11 = 1
                m12 = ele.Length
                m21 = 0
                m22 = 1
        if self.invertMatrix:
            detm = m11 * m22 - m12 * m21
            m12 = -m12 / detm
            m21 = -m21 / detm
            tmp = m22 / detm
            m22 = m11 / detm
            m11 = tmp
        self.write("%s: MATRIX, L=%f,\n" % (ele.Name, ele.Length))
        self.write("   RM11=%f,\n" % (m11))
        self.write("   RM12=%f,\n" % (m12))
        self.write("   RM21=%f,\n" % (m21))
        self.write("   RM22=%f,\n" % (m22))
        if ky > 0:
            omg = math.sqrt(ky) * ele.Length
            m11 = math.cos(omg)
            m12 = math.sin(omg) / math.sqrt(ky)
            m21 = -math.sin(omg) * math.sqrt(ky)
            m22 = math.cos(omg)
        else:
            if ky < 0:
                omg = math.sqrt(ky) * ele.Length
                m11 = math.cosh(omg)
                m12 = math.sinh(omg) / math.sqrt(ky)
                m21 = math.sinh(omg) * math.sqrt(ky)
                m22 = math.cosh(omg)
            else:
                m11 = 1
                m12 = ele.Length
                m21 = 0
                m22 = 1
        if self.invertMatrix:
            detm = m11 * m22 - m12 * m21
            m12 = -m12 / detm
            m21 = -m21 / detm
            tmp = m22 / detm
            m22 = m11 / detm
            m11 = tmp
        self.write("   RM33=%f,\n" % (m11))
        self.write("   RM34=%f,\n" % (m12))
        self.write("   RM43=%f,\n" % (m21))
        self.write("   RM44=%f;\n" % (m22))

    def writeDiagnostic(self, ele):
        if (ele.enable == 0):
            self.writeMarker(ele)
            return
        Seval = ele.Seval
        if (Seval < 0):
            Seval = 0.5 * ele.Length
        self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name, ele.Length))
        self.write("    %s.diag: MONITOR, L=0, AT=%f;\n" % (ele.Name, Seval))
        self.write("ENDSEQUENCE;\n")

    def writeMarker(self, ele):
        Seval = 0.5 * ele.Length
        if ele.Length > 0:
            self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name, ele.Length))
            self.write("    %s.mark:  MARKER, AT=%f;\n" % (ele.Name, Seval))
            self.write("ENDSEQUENCE;\n")
        else:  # Simple marker, zero reserve length
            self.write("    %s:  MARKER;\n" % (ele.Name))

    def writeSolenoid(self, ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap == 1:
                return
        self.write("%s.ks := %f;\n" % (ele.Name, ele.ks))
        self.write("%s: SOLENOID, L=%f, ks:=%s.ks;\n" % (ele.Name, ele.Length, ele.Name))


