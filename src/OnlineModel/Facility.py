from src.OnlineModel.Layout.Build import Build
from src.OnlineModel.Core.Type import LineContainer, Dipole, Marker
from src.OnlineModel.Core.FacilityAccess import FacilityAccess
from src.OnlineModel.Core.EnergyProfile import EnergyManager
import src.OnlineModel.Layout.Initialization as Init

class SwissFEL(FacilityAccess):
    """
    class to create an instance of SwissFEL - the basic entry point for the online model
    """
    def __init__(self, alt=0):
        """
        initialize the layout
        :param alt: version of the lattice:
                    alt=0 is current phase
                    alt=1 is planned phase (near future)
                    alt=2 is future phase (far future)
        """

        # build layout
        layout = Build(alt)
        self.PartsList = layout.build()  # generate the lattice and return the beamlines
        print('Initializing Lattice', layout.Version)
        self.ElementDB = {}  # dictionary to hold all elements of the facility
        self.SectionDB = {}  # dictionary of subsections with 7 Letter ID  - atomic line

        # flatten beamlines so that only one outer container exists with the section container, e.g. SINSB01
        # In addition the element and section database are populated
        for p in self.PartsList:
            line = LineContainer('')
            p[0].flatten('S', line, self.ElementDB, self.SectionDB)
            p[0] = line  # replace the current nested line container with the list of atomic subsection

        # maps elements in the beamline
        self.mapping()

        # set default values for elements
        self.initialize(Init.initvalue)


# calculate energy profile
        self.EM = EnergyManager()
        self.writeFacility(self.EM)


    def mapping(self):
        """
        Routine to find the corresponding beamline for a given element/atomic section
        :return: nothing
        """
        foundMarker = {}
        List1 = []
        for i in range(0, len(self.PartsList)):   # loop though all beamlines (e.g. Injector, Aramis)
            p = self.PartsList[i]
            found = 0
            # line=self.BeamPath(i)
            j = 1
            k = 0
            for subsec in p[0].Element:   # loops through atomic line of each beamline
                for ele in subsec.Element:  # search for a marker, indicating a branching point
                    if ele.Tag == 'MKBR':
                        key = str(i) + '_' + str(j)
                        found = found + 1
                        foundMarker[key] = ele.Name
                        j = j + 1
                    k = k + 1
                    ele.__dict__.update({'mapping': [i, j, k]})  # each element has a mapping triple:
                                                                 # i = in which beamline it can be found
                                                                 # j = after which marker it can be found
                                                                 # k = the index of the element in the atomic line

                section = self.SectionDB[subsec.Name]
                section.__dict__.update({'mapping': i})   # mapping of the section just in which beamline
            List1.append([p[1], p[2], found])

        self.foundMarker = foundMarker  # list of marker elements
        return

    def initialize(self,initval):
        """
        Initialize elements with some basic values from the dictionary.
        They are not necessarily the current design values
        :param initval: dictionary with element name and value
        :return: Nothing
        """
        for key in initval.keys():
            keysplit = key.split(':')
            name = keysplit[0].replace('-', '.')
            field = keysplit[1]
            val = initval[key]
            if 'K1L' in field or 'K2L' in field:
                L = self.getField(name, 'Length')
                if L is None:
                    L = 1
                val = val/L
                field = field[:-1].lower()
            if 'K0L' in field:
                field = 'angle'
            if 'Grad' in field:
                field = 'Gradient'
            if 'Gap' in field or 'Offset' in field:
                field = field.lower()
            self.setField(name, field, val)


    def writeFacility(self, app=None, simple=0):
        """
        Loops through all beamlines, invoking the writeLattice command.
        :param app: class which handles the events for each element, following the ExportBase structure
        :param simple: <>0 just write out the specific line (e.g. only injector) instead full line
        :return: Nothing
        """
        if not app:
            print('no application, no action')   # this should throw an exception
            return

        for i in range(0, len(self.PartsList)):
            p = self.PartsList[i]
            if 'demandMapID' in dir(app):
                if app.demandMapID():  # app is asking which part is under writing
                    if i == len(self.PartsList) - 1:
                        app.MapIndx = -i  # Give a negative index for the last part
                    else:
                        app.MapIndx = i
            if simple:
                line = p[0]
            else:
                line = self.BeamPath(self.PartsList.index(p))
            print('Writing Beam line for: ', p[3])
            line.writeLattice(app)

    def BeamPath(self, PathIndx, Branch=0):
        """
        construct a beam path for a given path index
        :param PathIndx: index of the selected path - this should be made easier
        :param Branch: Use in the recursive approach to indicate branching points of child lines
        :return: returns a line container with the new line
        """
        if PathIndx < 0 or PathIndx > len(self.PartsList) - 1:
            return None
        if not isinstance(PathIndx, int):
            return None

        path = self.PartsList[PathIndx]
        parentID = path[1]  # reference to parent beamline (0 means root and has no parent)
        branchID = path[2]  # branching point: the nth occurence of a marker in the parent beam line.
                            # If negative -1 than line is appended to parent line
        line = LineContainer('')  # create empty line which will be populated with the given elements

        if (branchID != 0):  # get line from parents first
            line = self.BeamPath(parentID, branchID)

        foundMarker = 0  # to count makers in a given line
        for sec in path[0].Element:  # loop over all subsection in a line
            for ele in sec.Element:  # check if the element of the subsection is a marker and increase counter if so
                if isinstance(ele, Marker):
                    foundMarker = foundMarker + 1
                    if Branch > 0 and foundMarker == Branch:  # check whether the branching point is found
                        found = 0  # find dipole before marker to sert to desing_angle
                        idx = sec.Element.index(ele) - 1
                        while found == 0 and idx > -1:
                            if isinstance(sec.Element[idx], Dipole):
                                sec.Element[idx].angle = sec.Element[idx].design_angle
                                found = 1
                            idx = idx - 1
                        secnew = LineContainer(sec.Name)  # create a new line container to hold reduced section
                        for i in range(0, sec.Element.index(ele)):
                            ref = sec.Ref[sec.Element[i]]
                            secnew.append(sec.Element[i], ref['pos'], ref['ref'])  # add element and its reference
                        line.append(secnew, 0, 'relative')
                        return line
                    else:
                        # check for dipoles to be set straight if not a branching point.
                        found = 0  # search backwards from the marker
                        idx = sec.Element.index(ele) - 1
                        while found == 0 and idx > -1:
                            if isinstance(sec.Element[idx], Dipole):
                                sec.Element[idx].angle = 0
                                found = 1
                            idx = idx - 1
            line.append(sec, 0, 'relative')  # append subsection
        return line

    def isUpstream(self, a, b):
        """
        Check whether element A is upstream of element B
        :param a: First element name
        :param b: Second element name
        :return: True or False
        """
        if not a in self.ElementDB.keys() or not b in self.ElementDB.keys():
            return None

        A = self.ElementDB[a]
        Amap = A.mapping

        B = self.ElementDB[b]
        Bmap = B.mapping

        if Amap[0] == Bmap[0]:  # Two elements are in the same part of the machine, easy case
            if Amap[2] < Bmap[2]:
                return True
            else:
                return False

        myself = Bmap[0]
        parent = 999
        while parent >= 0:
            parent = self.PartsList[myself][1]
            if Amap[0] == parent:
                branch = self.PartsList[myself][2]
                if branch == -1:
                    return True  # The part is connected to the paprent at the end, so Elem A is upstream of B
                elif Amap[1] <= branch:
                    return True  # The part is connected to the parent at a branch and Elem A is upstream of the branch, and thus upstream of B
                elif Amap[1] > branch:
                    return False  # The part is connected to the parent at a branch but Elem A is downstream of the branch and thus not upstream of B
            myself = parent

        return False  # The part which includes Elem A is not upstream of Elem B


