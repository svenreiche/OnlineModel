class ExportBase:
    """
    Base class to be inherited from other modules to export from the online model.
    It just provides that in writeLine of LineContainer Module always an event handler function is called
    """
    def __init__(self):
        self.switch = 0
        self.path = ''
        self.avoidPreset = 0
        self.MapIndx = []
        self.MapIndxSave = []

    def isType(self, key):
        return 0

    def demandMapID(self):
        return 0

    def writeLine(self, line, seq):
        return

    def writeDrift(self, ele):
        return

    def writeVacuum(self, ele):
        self.writeMarker(ele)
        return

    def writeAlignment(self, ele):
        self.writeMarker(ele)
        return

    def writeBend(self, ele):
        return

    def writeQuadrupole(self, ele):
        return

    def writeCorrector(self, ele):
        return

    def writeSextupole(self, ele):
        return

    def writeRF(self, ele):
        return

    def writeUndulator(self, ele):
        return

    def writeDiagnostic(self, ele):
        return

    def writeMarker(self, ele):
        return

    def writeSolenoid(self, ele):
        return

    def writeDechirper(self,ele):
        return
