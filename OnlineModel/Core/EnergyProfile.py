import math
from OnlineModel.Export.ExportBase import ExportBase


class EnergyManager(ExportBase):
    """
    Class which calculates the energy profile along the machine and update the corresponding fields in the elements
    """
    def __init__(self):
        ExportBase.__init__(self)
        self.p0 = 0    # reference energy
        self.p = 0     # floating energy to be accumulated
        self.Energy = {}

    def update(self, p0):
        self.p0 = p0

    def writeLine(self, line, seq):
        return

    def register(self, ele, Egain=0.0):
        if (self.MapIndx != self.MapIndxSave):  # New line comes
            self.p = 0
            self.MapIndxSave = self.MapIndx
        self.Energy[ele.Name] = [self.p, Egain]
        ele.p0 = self.p           # save energy in each element for easier exporting
        return

    def demandMapID(self):
        return 1

    def writeVacuum(self, ele):
        self.writeMarker(ele)
        return

    def writeAlignment(self, ele):
        self.writeMarker(ele)
        return

    def writeBend(self, ele):
        self.register(ele)

    def writeQuadrupole(self, ele):
        self.register(ele)

    def writeCorrector(self, ele):
        self.register(ele)

    def writeSextupole(self, ele):
        self.register(ele)

    def writeRF(self, ele):
        if (self.MapIndx != self.MapIndxSave):  # New line comes   ! this has currently no functionality
            self.p = 0
            self.MapIndxSave = self.MapIndx
        if ('Gradient' in ele.__dict__) and ('Phase' in ele.__dict__):  # needs a check for TDS to not give energy gain
            if 'TDS' in ele.Name:
                Egain = 0.0
            else:
                E = ele.Gradient
                V = E * ele.Length
                phase = ele.Phase * math.pi / 180.0
                Egain = V * math.sin(phase)
        else:
            Egain = 0.0
        self.Energy[ele.Name] = [self.p, Egain, ele.Length]
        self.p = self.p + Egain

    def writeUndulator(self, ele):
        self.register(ele)

    def writeDiagnostic(self, ele):
        self.register(ele)

    def writeSolenoid(self, ele):
        self.register(ele)

    def writeMarker(self, ele):
        self.register(ele)

    def demandMapID(self):
        'Energy manager always requests Map ID to Layout manger'
        return 1



