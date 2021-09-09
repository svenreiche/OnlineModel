import math


class TypeManager:
    """
    Class to manage predefined objects in the online model,
    which then can be recalled when generating the lattice
    the class should only interface with the layout class
    """
    def __init__(self):
        # library which collects all predefined types.
        self.library = {}  # ----- dictionary to contain all the element and line definition
        # mimicx a switch case to generate an item once called by its reference name
        self.typecase = {'Solenoid': self.sol, 'Photonics': self.xray, 'Undulator': self.ID, 'Vacuum': self.vac, \
                         'Quadrupole': self.quad, 'Corrector': self.cor, 'Diagnostic': self.diag, 'RF': self.rf, \
                         'Dipole': self.bend, 'Sextupole': self.sext, 'Marker': self.marker}

    def info(self):
        """
        prints out name and all infos/parameters of predefined types.
        :return:
        """
        for ele in self.library.keys():
            eledef = self.library[ele]
            for att in eledef.keys():
                if isinstance(eledef[att], str):
                    print('\t', att, " = '", eledef[att], "'")
                else:
                    print('\t', att, ' = ', eledef[att])
            print('\n')

    def define(self, name, properties):  # ----------- Routine to call when an element or line is defined
        """
        Defines a type to be referenced latter when building up the lattice
        :param name: keyword Name of the element to be referred with
        :param properties: dictionary list of argument to be assigned to the constructor when the element is created
        :return: Nothing
        """
        indict = {name: properties}
        self.library.update(indict)

    def generate(self, name, index=0, option={}):
        """
        Generate an instance of an lattice element based on a predefined type
        :param name: Name of the type when it was defined
        :param index: Assigned index for the element name according to the naming convention of SwissFEL (default 0)
        :param option: Additional keyword arguments for specific implementation for type of the same series
        :return: either a single element object if name refers to a type or a list of element if name refers to a line
        """
        # !!!!!!! here should be check if the name exists
        prop = self.library[name]

        # Convert tuple to list (should not occur)
        if isinstance(prop, tuple):
            prop = list(prop)

        if isinstance(prop, list):  # list type indicate a line as a list of individual types
            # To do: check for consitency, e.g. Length is defined as first element and that Name is in the option dictionary

            prop0 = prop[0]  # first element should always be the total length of the line
            L = 0
            if 'Length' in prop0:  # prop0.has_key('Length'):
                L = prop0['Length']
            name = ''
            if 'Name' in option:  # option.has_key('Name'):
                name = option['Name']  # needed to get the right name of the section
            obj = LineContainer(name, L)  # create the line container to be returned
            for ele in prop[1:len(prop)]:
                eletype = ele['Element']
                sRef = ele['sRef']
                index = 0
                if 'index' in ele:  # ele.has_key('index'):
                    index = ele['index']
                if 'Option' in ele:  # ele.has_key('Option'):
                    opt = ele['Option']
                else:
                    opt = {}
                rel = 'absolute'
                if 'Ref' in ele:  # ele.has_key('Ref'):
                    if ele['Ref'] == 'relative':
                        rel = 'relative'
                obj.append(self.generate(eletype, index, opt), sRef, rel)
        else:   # is an individual type
            # calls internal function which temselves calls the constructor of the object, depending on type
            obj = self.typecase[prop['Type']](prop)
            option['index'] = index
            obj.__dict__.update(option)  # add index to the generated element
        return obj

    # functions to call the individual constructor for a given type.
    def xray(self, prop):
        return Photonic(prop)

    def ID(self, prop):
        return Undulator(prop)

    def vac(self, prop):
        return Vacuum(prop)

    def quad(self, prop):
        return Quadrupole(prop)

    def bend(self, prop):
        return Dipole(prop)

    def sol(self, prop):
        return Solenoid(prop)

    def sext(self, prop):
        return Sextupole(prop)

    def cor(self, prop):
        return Corrector(prop)

    def diag(self, prop):
        return Diagnostic(prop)

    def rf(self, prop):
        return RF(prop)

    def marker(self, prop):
        return Marker(prop)
# End of Type Manager


class LineContainer:
    """
    Class to manage a series of basic elements in conjunction with their longitudinal position.
    Line elements can be nested
    """
    def __init__(self, namein='', Lin=0):
        """
        Initialization of en empty container with a fixed length
        :param namein: name of the element
        :param Lin: reserved length. If positive it extends beyond last element if Lin is larger than the Lin=0 case.
                    If zero, the length is terminated after last element
                    If negative the length is extended relative to the end of the last element
        """
        self.Name = namein
        self.LengthRes = Lin
        self.Ref = {}
        self.Element = []
        self.sRef = 0
        self.initiated = 0
        self.output = 1
        self.isFlat = 0

    def getLength(self):
        """
        Returns the reserved length for the section. No difference to the actually length unlike basic elements
        :return: length of the line
        """
        return self.getResLength()

    def getResLength(self):
        """
        Returns the reserved length of the line
        :return: length of the line
        """
        if len(self.Element) == 0:
            return self.LengthRes
        ele = self.Element[-1]
        slen = self.position(ele) + ele.getLength()
        if (self.LengthRes < 0):
            return slen - self.LengthRes  # add to end of last element
        else:
            if (self.LengthRes < slen):
                return slen
            else:
                return self.LengthRes   # extend at least by the reserved length

    def position(self, ele):  # Beginning of the element (Reserve length inclusive)
        """
        Calculates the starting position of an existing element in the line
        :param ele: element name for which the position is evaluated
        :return: starting position of the element
        """
        Ref = self.Ref[ele]   # should check if name exists
        if Ref['ref'] == 'absolute':
            return Ref['pos']
        else:
            idx = self.Element.index(ele) - 1
            srel = 0
            if idx >= 0:
                srel = self.position(self.Element[idx]) + self.Element[idx].getResLength()
            if Ref['ref'] == 'relative':
                return srel + Ref['pos']
            else:
                idx = Ref['pos']
                angle = self.Element[idx].angle

                return srel + Ref['ref'].len(angle)

    def positionCenter(self, ele):  # Centre of the element
        """
        Calculates the center position for an existing element in the line
        :param ele: element name of an existing element of the line
        :return: center position of the element
        """
        return self.position(ele) + ele.sRef + ele.getLength() * 0.5

    def append(self, ele, sRef=0, Ref='absolute'):
        """
        Inserts a new element into the line
        :param ele: new element to be added
        :param sRef: reference position within the line, depending on the reference type
        :param Ref: string keyword:
            'relative' advance by sRef from last element
            'absolute' place element at position sRef in element, resetting the counter
            'variable' relative by with a function (class) to calculate the position on the fly
        :return: None (the internal list Element is extended by its name and
                        the reference position is added to dictionary Ref
        """
        if isinstance(ele, list):  # a quick way to add a series of elements if they are given in a list
            sRef = 0
            Ref = 'relative'
            for p in ele:
                self.Element.append(p)
                reference = {'pos': sRef, 'ref': Ref}
                self.Ref.update({p: reference})
        else:  # otherwise a single element is added
            self.Element.append(ele)
            reference = {'pos': sRef, 'ref': Ref}
            self.Ref.update({ele: reference})

    def flatten(self, name, line, eleDB, secDB):
        """
        Flatten a given line in the case it has nested lines. This is done after the layout has been parsed.
        this is done in the facility class.
        :param name: Name of the line
        :param line: finale list to contain all atomic lines, indicated by a 7 letter EPICS prefix
        :param eleDB: existing database of elements
        :param secDB: existing database of sections
        :return: Nothing
        """
        if self.isFlat > 0:  # check whether a given line has been already flatten (needed for phase 2 lines
            # the basic line element has a 7 character name as the most atomic line structure. In this case the line
            # adds itself to the line contain holding all lines
            if (len(self.Name) == 7):  # this follows SwissFEL naming convention that the unit line has a 7 letter tag
                line.append(self)
            return

        self.Name = name + self.Name  # add its name if not at atomic level of line, e.g. 'IN' for injector line
                                      # or 'S' for whole swissfel

        if (len(self.Name) == 7):  # is lowest level for flattening reached?
            for ele in self.Element:
                ele.initiate(self.Name)  # initiate all basic elements
                eleDB[ele.Name] = ele    # add element to database
            line.append(self)  # add section to beamline
            secDB[self.Name] = self  # Revive sectionDB...09.06.2015 Masamitsu
            self.isFlat = 1  # indicate that the line has been flatten
        else:
            for ele in self.Element:   # loop though the lines if not reach the atomic line level
                ele.flatten(self.Name, line, eleDB, secDB)

    def initiate(self, name=''):
        """
        Initiate a line, defining its name and eneable output by default (overwritten by setRange)
        :param name: Root name of the parent line
        :return: Nothing
        """
        self.Name = name + self.Name
        self.output = 1
        for ele in self.Element:
            ele.initiate(self.Name)

    def setRange(self, start='start', end='end', out=0):
        """
        set the range for any output of the line, define by starting and end point
        :param start: line name to start output
        :param end:  line name to end output
        :param out: directly controlling if line has output or not
        :return: either -1 if end of line has reached or the output of a child line
        """
        self.output = out  # inherit output from parent container

        # if no start point is given then use first line encountered as output
        if start == 'start':
            start = self.Name

        if self.Name == start:  # start output if name math
            self.output = 1

        hasend = 0
        output = self.output
        for ele in self.Element:
            if isinstance(ele, LineContainer):
                outchild = ele.setRange(start, end, output)
                if outchild != 0:  # if child is part of the range - parent has output
                    self.output = 1
                    output = 1
                if outchild == -1:  # if child was last then
                    output = 0  # suppress output for following children
                    hasend = 1  # indicate parent that this is the last element

        if (self.Name == end) or (hasend == 1):
            return -1
        return self.output

    def writeLattice(self, app):
        """
        function to loop through all the child elements and call the event handler from aan external class
        if line is enabled for output.
        :param app: the class which handles the element by element event function
        :return: returning sequences back to parent line.
        """
        if self.output == 0:
            return 0

        seq = []
        Last = 0   # position counter within the sequence

        if (len(self.Name) == 7):  # atomic level of line element
            for ele in self.Element:
                ds = self.position(ele) - Last
                app.writeDrift(ds)
                name = ele.writeElement(app)
                Last = self.position(ele) + ele.getResLength()
                if name != 0:
                    seq.append(ele)
            app.writeDrift(self.getResLength() - Last)
            app.writeLine(self, seq)
            baseseq = {'Name': self.Name, 'L': self.getResLength()}
            return baseseq   # return name and length of atomic elemet
        else:
            for ele in self.Element:
                name = ele.writeLattice(app)
                # if name<>0: # not valid in python3.x
                if name != 0:
                    seq.append(name)
            if len(self.Name) > 1:
                return seq
            else:
                app.writeLine(self, seq)
            return 0
# end of Line Container


class VariableContainer:
    """
    Simple class to calculate the path length if a section of the line is tilted, e.g. in dog leg, where the angle is
    dynamic and not fixed in the layout
    the model is a fix length subtracted first from the reserved length and then add the elongation dL/cos(angle)
    """
    def __init__(self, L=0, Loff=0):
        self.L = L
        self.Loff = Loff

    def len(self, angle):
        dL = self.L / math.cos(angle * math.asin(1) / 90) - self.Loff
        return dL
# end of Variable Container


class SimpleContainer:
    """
    Base class to inherited by all basic elements to ensure a common set of members.
    """
    def __init__(self, prop={}):
        """
        define default member elements
        :param prop: dictionary to use for define elements values
        """
        # makes sure that common elements are defined and calculates the length and reserved length
        if not ('Name' in prop):  # prop.has_key('Name')):
            prop.update({'Name': ''})

        if not ('Baugruppe' in prop):  # prop.has_key('Baugruppe')):
            prop.update({'Baugruppe': 'none'})

        if not ('index' in prop):  # prop.has_key('index')):
            prop.update({'index': 0})

        if not ('p0' in prop):  # prop.has_key('p0')):
            prop.update({'p0': 0})

        if not ('Length' in prop):  # prop.has_key('Length')):
            prop.update({'Length': 0})

        if not ('LengthRes' in prop):  # prop.has_key('LengthRes')):
            prop.update({'LengthRes': 0})

        if not ('sRef' in prop):  # prop.has_key('sRef')):
            prop.update({'sRef': -1})

        if not ('Tilt' in prop):  # prop.has_key('Tilt')):
            prop.update({'Tilt': 0})

        self.__dict__.update(prop)

        if self.LengthRes <= 0:
            self.LengthRes = self.Length
            self.sRef = 0
        elif self.sRef >= 0:
            LRes = self.sRef + self.Length
            if self.LengthRes < LRes:
                self.LengthRes = LRes
        else:
            if self.LengthRes < self.Length:
                self.sRef = 0
                self.LengthRes = self.Length
            else:
                self.sRef = 0.5 * (self.LengthRes - self.Length)

    # check where this is needed. It is ugly and should be avoided
    def __getitem__(self, field):
        exec('a=self.' + field)
        # fine for python2 and python3
        return locals()['a']

    def getResLength(self):
        # return the reserved length for that element
        return self.LengthRes

    def getLength(self):
        # return the length for that element
        return self.Length

    def writeElement(self, app):
        return 0

    def initiate(self, name=""):
        """
        Defines name of element following the naming convention which is
        7 character section indication + 4 character tag name + 3 character number
        :param name: section name to which the element belongs
        :return:  None
        """
        # defined element name and local energy and the element entrance
        self.Name = "%s.%s%3.3d" % (name, self.Tag, self.index)

    def register(self):
        return

    # ---------------------------------------
# end of Simple Container


class Magnet(SimpleContainer):
    """
    bass class around simple container, which is common to all magnets
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'Magnets'})
# end of Magnet


class Dipole(Magnet):
    """
    Class for a dipole magnet
    """
    def __init__(self, prop):
        Magnet.__init__(self, prop)
        if not ('angle' in prop):  # prop.has_key('angle')):
            self.__dict__.update({'angle': 0})
        if not ('design_angle' in prop):  # prop.has_key('design_angle')):
            self.__dict__.update({'design_angle': 0})
        if not ('e1' in prop):  # prop.has_key('e1')):
            self.__dict__.update({'e1': 0})
        if not ('e2' in prop):  # prop.has_key('e2')):
            self.__dict__.update({'e2': 0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'MBND'})

    def getResLength(self):
        if (self.angle == 0):
            return self.LengthRes
        else:
            return self.LengthRes - self.Length + self.getLength()

    def getLength(self):
        if (self.angle == 0):
            return self.Length
        else:
            angrad = math.asin(1) * self.angle / 90.
            if self.e1 == 0 or self.e2 == 0:
                Lpath = self.Length / math.sin(angrad) * angrad
            else:
                Lpath = 0.5 * self.Length / math.sin(angrad * 0.5) * angrad
            return Lpath

    def writeElement(self, app):
        app.writeBend(self)
        return self.Name
# end of Dipole


class Quadrupole(Magnet):
    """
    Class to describe quadrupole magnets
    """
    def __init__(self, prop):
        Magnet.__init__(self, prop)
        if not ('k1' in prop):  # prop.has_key('k1')):
            self.__dict__.update({'k1': 0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'MQUA'})

    def writeElement(self, app):
        app.writeQuadrupole(self)
        return self.Name
# end of quadrupole


class Sextupole(Magnet):
    """
    class to describe sextupole magnets
    """
    def __init__(self, prop):
        Magnet.__init__(self, prop)
        if not ('k2' in prop):  # prop.has_key('k2')):
            self.__dict__.update({'k2': 0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'MSEX'})

    def writeElement(self, app):
        app.writeSextupole(self)
        return self.Name
# end of sextupole


class Solenoid(Magnet):
    """
    Class to describe solenoid
    """
    def __init__(self, prop):
        Magnet.__init__(self, prop)
        if not ('ks' in prop):  # prop.has_key('ks')):
            self.__dict__.update({'ks': 0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'MSOL'})

    def writeElement(self, app):
        app.writeSolenoid(self)
        return self.Name
# end of solenoid


class Corrector(Magnet):
    """
    class which describes stand-alone correctors
    """
    def __init__(self, prop):
        Magnet.__init__(self, prop)

    def writeElement(self, app):
        app.writeCorrector(self)
        return self.Name
# end of corrector


class Vacuum(SimpleContainer):
    """
    class to define vacuum components or other inactive elements
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'Vacuum'})

    def writeElement(self, app):
        app.writeVacuum(self)
        return self.Name
# end of vacuum


class Undulator(SimpleContainer):
    """
    class to define insertion devices
    Dechirper are currently handled as undulators. This should be changed
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'ID'})
        if not ('K' in prop):  # prop.has_key('K')):
            self.__dict__.update({'K': 0})
        if not ('ku' in prop):  # prop.has_key('ku')):
            self.__dict__.update({'ku': 0})
        if not ('kx' in prop):  # prop.has_key('kx')):
            self.__dict__.update({'kx': 0})
        if not ('ky' in prop):  # prop.has_key('ky')):
            self.__dict__.update({'ky': 1})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'UIND'})
        if not ('Power' in prop):  # prop.has_key('Power')):
            self.__dict__.update({'Power': 0})
        if not ('Waist' in prop):  # prop.has_key('Waist')):
            self.__dict__.update({'Waist': 1})

    def writeElement(self, app):
        app.writeUndulator(self)
        return self.Name
# end of undulator


class RF(SimpleContainer):
    """
    class which describes RF structures
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Gradient' in prop):  # prop.has_key('Gradient')):
            self.__dict__.update({'Gradient': 0})
        if not ('Phase' in prop):  # prop.has_key('Phase')):
            self.__dict__.update({'Phase': 0})
        if not ('Band' in prop):  # prop.has_key('Band')):
            self.__dict__.update({'Band': 'S'})
        if not ('Frequency' in prop):  # prop.has_key('Frequency')):
            f0 = 5.712e9
            if 'S' in self.Band:
                f0 = 2.9988e9
            if 'X' in self.Band:
                f0 = 11.9952e9
            self.__dict__.update({'Frequency': f0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'RACC'})
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'RF'})

        # Enable flag for TDS as well as in the diagnostics
        if 'TDS' in prop['Baugruppe']:
            self.__dict__.update({'enable': 0})

    def writeElement(self, app):
        app.writeRF(self)
        return self.Name
# end of RF


class Diagnostic(SimpleContainer):
    """
    class which describes diagnostics elements
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Seval' in prop):  # prop.has_key('Seval')):
            self.__dict__.update({'Seval': -1})
        if not ('Cx' in prop):  # prop.has_key('Cx')):
            self.__dict__.update({'Cx': 1})
        if not ('Cy' in prop):  # prop.has_key('Cy')):
            self.__dict__.update({'Cy': 1})
        if not ('Cz' in prop):  # prop.has_key('Cz')):
            self.__dict__.update({'Cz': 0})
        if not ('Sx' in prop):  # prop.has_key('Sx')):
            self.__dict__.update({'Sx': 0})
        if not ('Sy' in prop):  # prop.has_key('Sy')):
            self.__dict__.update({'Sy': 0})
        if not ('Sz' in prop):  # prop.has_key('Sz')):
            self.__dict__.update({'Sz': 0})
        if not ('Distribution' in prop):  # prop.has_key('Distribution')):
            self.__dict__.update({'Distribution': 0})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            self.__dict__.update({'Tag': 'DBPM'})
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'Diagnostics'})
        if not ('enable' in prop):  # prop.has_key('enable')):
            self.__dict__.update({'enable': 0})

    def writeElement(self, app):
        app.writeDiagnostic(self)
        return self.Name
# end of Diagnostics


class Photonic(Diagnostic):
    """
    class describes photonics elements
    """
    def __init__(self, prop):
        prop.update({'Group': 'Photonics'})
        if not ('Tag' in prop):  # prop.has_key('Tag')):
            prop.update({'Tag': 'PPRM'})
        Diagnostic.__init__(self, prop)
# end of Photonic


class Alignment(SimpleContainer):
    """
    class which describes alignment elements, not really a physical device
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'Alignment'})

    def writeElement(self, app):
        app.writeAlignment(self)
        return self.Name

    def getLength(self):
        return 0
# end of alignment


class Marker(SimpleContainer):
    """
    class defining a marker for specific action, mostly used for branching points
    """
    def __init__(self, prop):
        SimpleContainer.__init__(self, prop)
        if not ('Group' in prop):  # prop.has_key('Group')):
            self.__dict__.update({'Group': 'Marker'})

    def writeElement(self, app):
        app.writeMarker(self)
        return self.Name

    def getLength(self):
        return 0
#end of marker
