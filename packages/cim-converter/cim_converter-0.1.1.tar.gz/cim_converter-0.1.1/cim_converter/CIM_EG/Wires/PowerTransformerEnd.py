from cim_converter.CIM_EG.Wires.TransformerEnd import TransformerEnd


class PowerTransformerEnd(TransformerEnd):

    def __init__(self,
                 endNumber=0,
                 phaseAngleClock=0,
                 ratedS=0,
                 ratedU=0,
                 connectionKind='Y',
                 BaseVoltage=None,
                 PowerTransformer=None,
                 RatioTapChanger=None,
                 *args,
                 **kw_args):

        self.endNumber = endNumber

        self.phaseAngleClock = phaseAngleClock

        self.ratedS = ratedS

        self.ratedU = ratedU

        self._BaseVoltage = None
        self.BaseVoltage = BaseVoltage

        self._PowerTransformer = None
        self.PowerTransformer = PowerTransformer

        self._RatioTapChanger = None
        self.RatioTapChanger = RatioTapChanger

        self.connectionKind = connectionKind

        super(PowerTransformerEnd, self).__init__(*args, **kw_args)

    _attrs = ["endNumber", "phaseAngleClock", "ratedS", "ratedU"]
    _attr_types = {
        "endNumber": int,
        "phaseAngleClock": int,
        "ratedS": float,
        "ratedU": float
    }
    _defaults = {
        "endNumber": 0,
        "phaseAngleClock": 0,
        "ratedS": 0,
        "ratedU": 0
    }
    _enums = {"connectionKind": "WindingConnection"}
    _refs = ["BaseVoltage", "PowerTransformer", "RatioTapChanger"]
    _many_refs = []

    def getBaseVoltage(self):
        return self._BaseVoltage

    def setBaseVoltage(self, value):
        if self._BaseVoltage is not None:
            filtered = [
                x for x in self.BaseVoltage.TransformerEnds if x != self
            ]
            self._BaseVoltage._TransformerEnds = filtered
        if value is not None:
            value.TransformerEnds.append(self)
        self._BaseVoltage = value

    BaseVoltage = property(getBaseVoltage, setBaseVoltage)

    def getPowerTransformer(self):
        return self._PowerTransformer

    def setPowerTransformer(self, value):
        if self._PowerTransformer is not None:
            filtered = [
                x for x in self.PowerTransformer.PowerTransformerEnd
                if x != self
            ]
            self._PowerTransformer._PowerTransformerEnd = filtered
        if value is not None:
            value.PowerTransformerEnd.append(self)
        self._PowerTransformer = value

    PowerTransformer = property(getPowerTransformer, setPowerTransformer)

    def getRatioTapChanger(self):
        return self._RatioTapChanger

    def setRatioTapChanger(self, value):
        if self._RatioTapChanger is not None:
            self._RatioTapChanger._PowerTransformerEnd = None
        if value is not None:
            value.PowerTransformerEnd = self
        self._RatioTapChanger = value

    RatioTapChanger = property(getRatioTapChanger, setRatioTapChanger)
