#from copy import deepcopy
#from string import *
#import math
#import re
#import numpy as np
#import sys

from OnlineModel.Layout.Build import Build



#from OMFacilityAccess import FacilityAccess
#from OMType import *
#from OMEnergyManager import *
#from OMLayout import SwissFEL

#class Facility(FacilityAccess):


class SwissFEL:
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
        print('SwissFEL init')
        L=Build(alt)
        if True:
            return
        if layout is not None and Layout.Version is not layout:
            module_name = 'OMLayout_%s' % layout.replace('.', '_')
            module = __import__(module_name)
            Layout = module.SwissFEL(alt)
            print('Importing Layout Module:', module_name)
        print('Initializing Lattice', Layout.Version);

        self.PartsList = Layout.build()  # generate the lattice and return the beamlines
        self.EM = EnergyManager()

        # Note that the subsections have also a direct reference to the elements but if elements are altered
        # in ElementDB then the SectionDB is automatically updated with the new values.
        self.ElementDB = {}  # dictionary to hold all elements of the facility
        self.SectionDB = {}  # dictionary of subsections with 7 Letter ID
        self.IntegratedCorrDB = {}  # Database for integrated correctors

        # flatten beamlines so that only one outer container exists with the section container, e.g. SINSB01

        for p in self.PartsList:
            line = LineContainer('')  #
            p[0].flatten('S', line, self.ElementDB, self.SectionDB, self.IntegratedCorrDB)
            p[0] = line  # replace the current nested line container with the list of atomic subsection

        # initiate the element values with default values
        if init:
            Layout.initialize(self.ElementDB)
        if init == 2:
            self.turnOffBends()
        if init == 3:
            self.turnOffBranchBends()

        # define the mapping of the element, defining their position and asignment to a branch
        self.mapping()

        # setup a dictionary of bending magnets.
        BCdict = {}
        self.BranchBend = []
        for k in self.ElementDB.keys():
            if isinstance(self.ElementDB[k], Dipole):
                try:
                    self.ElementDB[k].branch
                    #                    print(k)
                    self.BranchBend.append(k)
                except:
                    None
                try:
                    self.ElementDB[k].BC
                    if self.ElementDB[k].BC in BCdict:
                        # It must be the element itself (not Element.Name) becuase the new feature altSection allows the same element name in the altered section...
                        BCdict[self.ElementDB[k].BC].append(self.ElementDB[k])
                    else:
                        BCdict[self.ElementDB[k].BC] = [self.ElementDB[k]]
                except:
                    None

        # get braching points and bunch compressor magnets

        self.BC = []
        self.BCBPM = {}
        for k in BCdict.keys():
            BC = BCdict[k]
            BCsorted = [0] * len(BC)
            for i in range(0, len(BC)):
                judge = []
                for j in range(0, len(BC)):
                    if i != j:
                        judge.append(self.isUpstream(BC[i].Name, BC[j].Name))
                jsum = sum(judge)
                BCsorted[len(BC) - jsum - 1] = BC[i]

            if len(BCsorted) == 4:
                sect = BCsorted[3].Name.split('.')[0]
                for s in self.SectionDB.keys():
                    if s == sect:
                        # if BCsorted[3].altSection==s.altSection: # altSection is turned off for now... 29.05.2015
                        # arm=self.SectionDB[s].position(self.ElementDB[BCsorted[3].Name])-self.SectionDB[s].position(self.ElementDB[BCsorted[2].Name])
                        arm = self.SectionDB[s].position(BCsorted[3]) - self.SectionDB[s].position(BCsorted[2])
                        BCsorted.append(arm)
                        self.BCBPM[BCsorted[0].Name] = ['', '', 0]
                        for ele in self.SectionDB[s].Element:
                            if 'DBPM' in ele.Name:  # This does not detect Laser heater...
                                if self.isUpstream(BCsorted[0].Name, ele.Name) and self.isUpstream(ele.Name,
                                                                                                   BCsorted[1].Name):
                                    self.BCBPM[BCsorted[0].Name][0] = ele  # BPM between the first and second dipoles
                                if self.isUpstream(BCsorted[2].Name, ele.Name) and self.isUpstream(ele.Name,
                                                                                                   BCsorted[3].Name):
                                    self.BCBPM[BCsorted[0].Name][1] = ele  # BPM between the third and fourth dipoles
                                    self.BCBPM[BCsorted[0].Name][2] = self.SectionDB[s].position(BCsorted[3]) + \
                                                                      BCsorted[3].Length / 2 - self.SectionDB[
                                                                          s].position(ele) - ele.Length / 2

            self.BC.append(BCsorted)

        # get list of first nd last magnetin bunch compressor.
        self.BCstart = {}
        self.BCend = {}
        for ele in self.BC:
            self.BCstart[ele[0]] = 1
            self.BCend[ele[-1]] = 1

        # initialize all element with the energy. All elements need to be registered first to avoid an error message of not registered elements
        for ele in self.ElementDB.values():
            self.EM.register(ele)
        self.writeFacility(self.EM)

    def turnOffBends(self):
        for ele in self.ElementDB.values():
            if isinstance(ele, Dipole):
                ele.angle = 0.0

    def turnOffBranchBends(self):
        for ele in self.ElementDB.values():
            if isinstance(ele, Dipole) and ('branch' in ele.__dict__):
                ele.angle = 0.0

    # end of initialization
    # ----------------------------------------------------------------------------------

    def isUpstream(self, a, b):
        # Tell you if a is upstream of b.
        try:
            A = self.ElementDB[a]
            Amap = A.mapping
        except:
            try:
                A = self.IntegratedCorrDB[a]
                Amap = A.mapping
            except:
                print('Your input element name is not in Element data base...A:', a)
                return None

        try:
            B = self.ElementDB[b]
            Bmap = B.mapping
        except:
            try:
                B = self.IntegratedCorrDB[b]
                Bmap = B.mapping
            except:
                print('Your input element name is not in Element data base...B:', b)
                return None

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

    def mapping(self):

        foundMarker = {}
        List1 = []
        for i in range(0, len(self.PartsList)):
            p = self.PartsList[i]
            found = 0
            # line=self.BeamPath(i)
            j = 1
            k = 0
            for subsec in p[0].Element:
                for ele in subsec.Element:
                    if ele.Tag == 'MKBR':
                        key = str(i) + '_' + str(j)
                        found = found + 1
                        foundMarker[key] = ele.Name
                        j = j + 1
                    k = k + 1
                    ele.__dict__.update({'mapping': [i, j, k]})
                    # if ele.__dict__.has_key('cor') or ele.__dict__.has_key('corx') or ele.__dict__.has_key('cor'):
                    if 'cor' in ele.__dict__ or 'corx' in ele.__dict__ or 'cor' in ele.__dict__:
                        if ('MQUA' in ele.Name) or ('MBND' in ele.Name) or ('UIND' in ele.Name):
                            # if ele.__dict__.has_key('cor') or ele.__dict__.has_key('corx'):
                            if 'cor' in ele.__dict__ or 'corx' in ele.__dict__:
                                cname = ele.Name.replace('MQUA', 'MCRX').replace('MBND', 'MCRX').replace('UIND', 'MCRX')
                                cele = self.IntegratedCorrDB[cname]
                                cele.__dict__.update({'mapping': [i, j, k]})
                            # if ele.__dict__.has_key('cory'):
                            if 'cory' in ele.__dict__:
                                cname = ele.Name.replace('MQUA', 'MCRY').replace('MBND', 'MCRY').replace('UIND', 'MCRY')
                                cele = self.IntegratedCorrDB[cname]
                                cele.__dict__.update({'mapping': [i, j, k]})

                section = self.SectionDB[subsec.Name]
                section.__dict__.update({'mapping': i})
            List1.append([p[1], p[2], found])

        self.foundMarker = foundMarker

        return List1

    def BeamPath(self, PathIndx, Branch=0):

        # Branch indicates that for a branching marker is searched and then stopped at the correct occurence (e.g. Branch=2 stops at the second marker)
        if PathIndx < 0 or PathIndx > len(self.PartsList) - 1:
            return None
        if not isinstance(PathIndx, int):
            return None

        path = self.PartsList[PathIndx]
        parentID = path[1]  # reference to parent beamline (0 means root and has no parent)
        branchID = path[
            2]  # branching point: the nth occurence of a marker in the parent beam line. If negative -1 than line is appended to parent line
        line = LineContainer('')  # clear current line

        if (branchID != 0):  # get line from parents first
            line = self.BeamPath(parentID, branchID)

        foundMarker = 0  # to count makers in a given line
        for sec in path[0].Element:  # loob over all subsection in a line
            for ele in sec.Element:  # check if the element of the subsection is a marker and increase counter if so
                # if isinstance(ele,Dipole):
                #    ele.angle=ele.design_angle
                if isinstance(ele, Marker):
                    foundMarker = foundMarker + 1
                    if Branch > 0 and foundMarker == Branch:  # check whether the branching point is found
                        found = 0  # find dipole before marker to sert to desing_angle
                        idx = sec.Element.index(ele) - 1
                        while found == 0 and idx > -1:
                            if isinstance(sec.Element[idx], Dipole):
                                #                                print('setting branching angle for',sec.Element[idx].Name,'for branch', Branch)
                                sec.Element[idx].angle = sec.Element[idx].design_angle;
                                found = 1;
                            idx = idx - 1;
                        secnew = LineContainer(sec.Name)  # create a new line container to hold reduced section
                        for i in range(0, sec.Element.index(ele)):
                            ref = sec.Ref[sec.Element[i]]
                            secnew.append(sec.Element[i], ref['pos'], ref['ref'])  # add element and its reference
                        line.append(secnew, 0, 'relative')
                        return line
                    else:
                        # check for dipoles to be set straight if not a branching point.
                        found = 0;  # search backwards from the marker
                        idx = sec.Element.index(ele) - 1
                        while found == 0 and idx > -1:
                            if isinstance(sec.Element[idx], Dipole):
                                sec.Element[idx].angle = 0;
                                found = 1;
                            idx = idx - 1;
            line.append(sec, 0, 'relative')  # append subsection
        return line

    def writeFacility(self, app=None, simple=0, EM=None):
        # Handle the entire facility at one time - experimental
        # Particular application is the energy manager

        if not app:
            'no application, no action'
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
                line = p[
                    0]  # this might be wrong if a branching has happen, because it takes the full cenn and not the adjusted on eup to branch
            else:
                line = self.BeamPath(self.PartsList.index(p))
            print('Writing Beam line for: ', p[3])
            # if no energy manager is specified than use the internal one as default
            if not EM:
                EM = self
            line.writeLattice(app, EM)


