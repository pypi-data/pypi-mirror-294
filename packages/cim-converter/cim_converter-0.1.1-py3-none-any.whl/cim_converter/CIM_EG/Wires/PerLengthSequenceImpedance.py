from cim_converter.CIM_EG.Core.Equipment import Equipment


class PerLengthSequenceImpedance(Equipment):

    def __init__(self,
                 x=0.0,
                 r=0.0,
                 bch=0.0,
                 r0=0.0,
                 g0ch=0.0,
                 b0ch=0.0,
                 gch=0.0,
                 x0=0.0,
                 AclineSegments=None,
                 WireInfos=None,
                 *args,
                 **kw_args):
        self.x = x
        self.r = r
        self.bch = bch
        self.r0 = r0
        self.g0ch = g0ch
        self.b0ch = b0ch
        self.gch = gch
        self.x0 = x0

        self._AclineSegments = []
        self.AclineSegments = [] if AclineSegments is None else AclineSegments

        self._WireInfos = []
        self.WireInfos = [] if WireInfos is None else WireInfos

        super(PerLengthSequenceImpedance, self).__init__(*args, **kw_args)

    _attrs = ["x", "r", "bch", "r0", "g0ch", "b0ch", "gch", "x0"]
    _attr_types = {
        "x": float,
        "r": float,
        "bch": float,
        "r0": float,
        "g0ch": float,
        "b0ch": float,
        "gch": float,
        "x0": float,
    }
    _defaults = {
        "x": 0.0,
        "r": 0.0,
        "bch": 0.0,
        "r0": 0.0,
        "g0ch": 0.0,
        "b0ch": 0.0,
        "gch": 0.0,
        "x0": 0.0,
    }
    _enums = {}
    _refs = ["AclineSegments", "WireInfos"]
    _many_refs = ["AclineSegments", "WireInfos"]

    def getAclineSegments(self):
        return self._AclineSegments

    def setAclineSegments(self, value):
        for x in self._AclineSegments:
            x.SequenceImpedance = None
        for y in value:
            y._SequenceImpedance = self
        self._AclineSegments = value

    AclineSegments = property(getAclineSegments, setAclineSegments)

    def addAclineSegments(self, *AclineSegments):
        for obj in AclineSegments:
            obj.SequenceImpedance = self

    def removeAclineSegments(self, *AclineSegments):
        for obj in AclineSegments:
            obj.SequenceImpedance = None

    def getWireInfos(self):
        return self._WireInfos

    def setWireInfos(self, value):

        for x in self._WireInfos:
            x.SequenceImpedance = None
        for y in value:
            y._SequenceImpedance = self
        self._WireInfos = value

    WireInfos = property(getWireInfos, setWireInfos)

    def addWireInfos(self, *WireInfos):
        for obj in WireInfos:
            obj.SequenceImpedance = self

    def removeWireInfos(self, *WireInfos):
        for obj in WireInfos:
            obj.SequenceImpedance = None
