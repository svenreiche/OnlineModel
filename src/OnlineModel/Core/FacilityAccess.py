import re
import numpy as np


class FacilityAccess:
    """
    Base class, to be inherited by the Facility class for basic interface with the elements in the model
    """
    def getSection(self, name):
        """
        returns a beamline by name
        :param name: name of the beamline
        :return: Bemaline or None if not found
        """
        name = name.upper()
        if name in self.SectionDB.keys():
            return self.SectionDB[name]
        else:
            return None

    def getElement(self, name):
        """
        returns a beamline element by name
        :param name: name of the bemaline element, following the naming convention, excpt replacing dash with dot
        :return: Element or None if not found
        """
        name = name.upper()
        if name in self.ElementDB.keys():
            return self.ElementDB[name]
        else:
            return None

    def getField(self, dn, field):
        """
        Retrieve a field for a group of elements
        :param dn: list of element names or a single element name
        :param field: name of the field to be retrieved
        :return: array of values or single value
        """
        isList = True
        if not isinstance(dn, list):
            isList = False
            dn = [dn]
        values = []
        for n in dn:
            if n in self.ElementDB.keys():
                ele = self.ElementDB[n]
                if field in dir(ele):
                    values.append(ele[field])
                else:
                    values.append(None)
            else:
                values.append(None)
        if isList:
            return values
        return values[0]

    def getFieldByRegExp(self, section, device, field):
        """
        Retrieve field for all elements matching the regular expression
        :param section: Regular expression for section name
        :param device: Regular expression for device name
        :param field: Field to be retrieved
        :return: array of values
        """
        val = []
        myRe = re.compile(section + '.*' + device)
        for key in self.ElementDB.keys():
            if (myRe.match(key)):
                ele = self.ElementDB[key]
                if field in ele.__dict__.keys():
                    val.append(ele[field])
        return val

    def setField(self, dn, field, value):
        """
        Set the value of a field for a single element or a list of elements
        :param dn: element name or list of element names
        :param field: field name to by updated
        :param values: single value or list of values, matching size of dn
        :return: Nothing
        """
        if isinstance(dn,list):   # if list, call recursively for each element
            if not (len(dn) == len(value)):
                return
            for i, n in enumerate(dn):
                self.setField(n, field, value[i])
            return
        if dn in self.ElementDB.keys():
            ele = self.ElementDB[dn]
            if field in dir(ele):
                ele.__dict__.update({field: value})
            else:
                print('Cannot find field:',dn,field)
        else:
            print('Cannot find element',dn)

    def setFieldByRegExp(self, section, device, field, value):
        """
        Set field of all elements to a common value if the name matches the regular expression
        :param section: Regular expression of the section name
        :param device: Regular expression of the deivce name
        :param field: Field name to be update
        :param value: value the fields are updated with
        :return: Nothing
        """
        myRe = re.compile(section + '.*' + device)
        for key in self.ElementDB.keys():
            if myRe.match(key):
                ele = self.ElementDB[key]
                if field in ele.__dict__.keys():
                    if field == 'angle':
                        ele.__dict__[field] = np.sign(ele['design_angle']) * abs(value)
                        # this is needed to set collectively a bunch compressor angle without flipping signs
                    else:
                        ele.__dict__[field] = value

    def EnergyAt(self, ele):
        """
        Returns the current energy at a given element in eV and the energy gain within this element
        :param ele: Element from the facility element database or the name of such element
        :return: List of energy and energy gain at that element
        """
        if isinstance(ele, str):
            name = ele
        else:
            name = ele.Name
        if name in self.EM.Energy.keys():
            return self.EM.Energy[name]
        else:
            print(name + ' is not found in Energy manager of Module Facility!')
            return [0.0, 0.0]

    def forceEnergyAt(self, elename, Ei):

        # force an update of the energy profile
        self.writeFacility(self.EM)

        if Ei < 0:
            # The initial energy should be positive
            return
        if elename in self.EM.Energy.keys():
            E0 = self.EM.Energy[elename][0]
            dE = Ei - E0
        else:
            return

        for k in self.EM.Energy.keys():
            if len(self.EM.Energy[k]) == 2:
                self.EM.Energy[k] = [self.EM.Energy[k][0] + dE, self.EM.Energy[k][1]]
            elif len(self.EM.Energy[k]) == 3:
                self.EM.Energy[k] = [self.EM.Energy[k][0] + dE, self.EM.Energy[k][1], self.EM.Energy[k][2]]
            ele = self.getElement(k)
            ele.p = ele.p + dE
    # ---------------------------
    # unused function kept




    def listElement(self, word=None, NoE=0):
        # Return a list of elements that includes word
        # Wild card (*) can be used
        # NoE stands for Name or Element, switching the output
        # 0: list of Element names, 1: list of element instances.
        if word == None:
            return
        elif word == '*':
            allRequested = 1
        elif len(word) == 0:
            return []
        else:
            word = word.upper()
            word = word.split('*')
            allRequested = 0

        ElementList = []
        for p in self.PartsList:
            for sec in p[0].Element:
                for ele in sec.Element:
                    requested = 1
                    for w in word:
                        if w not in ele.Name:
                            requested = allRequested
                    if requested:
                        if NoE:
                            ElementList.append(ele)
                        else:
                            if ele.Type != 'Corrector':
                                ElementList.append(ele.Name)
                            if ('cor' in ele.__dict__) or ('corx' in ele.__dict__):
                                ElementList.append(ele.Name.replace(ele.Name[8:12], 'MCRX'))
                            if ('cory' in ele.__dict__):
                                if (ele.Name[8:12] == 'MKAC') or (ele.Name[8:12] == 'MKDC'):
                                    ElementList.append(ele.Name)
                                else:
                                    ElementList.append(ele.Name.replace(ele.Name[8:12], 'MCRY'))

        return ElementList

    def listSection(self, word=None, NoE=0):
        # Return a list of elements that includes word
        # Wild card (*) can be used
        # NoE stands for Name or Element, switching the output
        # 0: list of Element names, 1: list of line instances.
        if word == None:
            return
        elif word == '*':
            allRequested = 1
        elif len(word) == 0:
            return []
        else:
            word = upper(word)
            word = word.split('*')
            allRequested = 0

        SectionList = []
        for p in self.PartsList:
            for sec in p[0].Element:
                requested = 1
                for w in word:
                    if w not in sec.Name:
                        requested = allRequested
                if requested:
                    if NoE:
                        SectionList.append(sec)
                    else:
                        SectionList.append(sec.Name)

        return SectionList



