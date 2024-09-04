from cim_converter.CIM_EG.Wires.Conductor import Conductor


class ACLineSegment(Conductor):

    def __init__(self,
                 OverheadWireInfo=None,
                 AssetDatasheet=None,
                 g0ch=0.0,
                 r=0.0,
                 x=0.0,
                 gch=0.0,
                 r0=0.0,
                 bch=0.0,
                 b0ch=0.0,
                 x0=0.0,
                 PerLengthImpedance=None,
                 *args,
                 **kw_args):

        self.g0ch = g0ch
        self.r = r
        self.x = x
        self.gch = gch
        self.r0 = r0
        self.bch = bch
        self.b0ch = b0ch
        self.x0 = x0

        self._SequenceImpedance = None
        self._PhaseImpedance = None
        self._PerLengthImpedance = None

        self._AssetDatasheet = None
        self.AssetDatasheet = AssetDatasheet

        self._OverheadWireInfo = None
        self.OverheadWireInfo = OverheadWireInfo

        super(ACLineSegment, self).__init__(*args, **kw_args)

    _attrs = ["g0ch", "r", "x", "gch", "r0", "bch", "b0ch", "x0"]
    _attr_types = {
        "g0ch": float,
        "r": float,
        "x": float,
        "gch": float,
        "r0": float,
        "bch": float,
        "b0ch": float,
        "x0": float
    }
    _defaults = {
        "g0ch": 0.0,
        "r": 0.0,
        "x": 0.0,
        "gch": 0.0,
        "r0": 0.0,
        "bch": 0.0,
        "b0ch": 0.0,
        "x0": 0.0
    }
    _enums = {}
    _refs = ["PerLengthImpedance", "OverheadWireInfo"]
    _many_refs = ["ConductorAssets", "Cut", "Clamp", "ACLineSegmentPhases"]

    def getAssetDatasheet(self):
        return self._AssetDatasheet

    def setAssetDatasheet(self, value):
        if self._AssetDatasheet is not None:
            filtered = [
                x for x in self.AssetDatasheet.ACLineSegments if x != self
            ]
            self._AssetDatasheet._ACLineSegments = filtered

        self._AssetDatasheet = value
        if self._AssetDatasheet is not None:
            if self not in self._AssetDatasheet._ACLineSegments:
                self._AssetDatasheet._ACLineSegments.append(self)

    def getPerLengthImpedance(self):
        return self._PerLengthImpedance

    def setPerLengthImpedance(self, value):
        if self._PerLengthImpedance is not None:
            filtered = [
                x for x in self.PerLengthImpedance.AclineSegments if x != self
            ]
            self._PerLengthImpedance._AclineSegments = filtered

        self._PerLengthImpedance = value
        if self._PerLengthImpedance is not None:
            if self not in self._PerLengthImpedance._AclineSegments:
                self._PerLengthImpedance._AclineSegments.append(self)

    PerLengthImpedance = property(getPerLengthImpedance, setPerLengthImpedance)
