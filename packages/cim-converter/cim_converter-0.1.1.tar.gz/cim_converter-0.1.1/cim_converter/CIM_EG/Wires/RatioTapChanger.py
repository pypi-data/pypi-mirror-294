from cim_converter.CIM_EG.Wires.TapChanger import TapChanger


class RatioTapChanger(TapChanger):

    def __init__(self,
                 controlEnabled=False,
                 step=0,
                 stepVoltageIncrement=0.0,
                 tculControlMode="reactive",
                 RatioTapChangerTabular=None,
                 TransformerEnd=None,
                 *args,
                 **kw_args):

        self.controlEnabled = controlEnabled

        self.step = step

        self.stepVoltageIncrement = stepVoltageIncrement

        self.tculControlMode = tculControlMode

        self._RatioTapChangerTabular = None
        self.RatioTapChangerTabular = RatioTapChangerTabular

        self._TransformerEnd = None
        self.TransformerEnd = TransformerEnd

        super(RatioTapChanger, self).__init__(*args, **kw_args)

    _attrs = [
        "stepVoltageIncrement", "tculControlMode", "step", "controlEnabled"
    ]
    _attr_types = {
        "stepVoltageIncrement": float,
        "tculControlMode": str,
        "step": int,
        "controlEnabled": bool
    }
    _defaults = {
        "stepVoltageIncrement": 0.0,
        "tculControlMode": "reactive",
        "step": 0,
        "controlEnabled": False
    }
    _enums = {"tculControlMode": "TransformerControlMode"}
    _refs = ["RatioTapChangerTabular", "TransformerEnd"]
    _many_refs = []

    def getRatioTapChangerTabular(self):

        return self._RatioTapChangerTabular

    def setRatioTapChangerTabular(self, value):
        if self._RatioTapChangerTabular is not None:
            filtered = [
                x for x in self.RatioTapChangerTabular.RatioTapChanger
                if x != self
            ]
            self._RatioTapChangerTabular._RatioTapChanger = filtered

        self._RatioTapChangerTabular = value
        if self._RatioTapChangerTabular is not None:
            if self not in self._RatioTapChangerTabular._RatioTapChanger:
                self._RatioTapChangerTabular._RatioTapChanger.append(self)

    RatioTapChangerTabular = property(getRatioTapChangerTabular,
                                      setRatioTapChangerTabular)

    def getTransformerEnd(self):
        """Transformer end to which this ratio tap changer belongs.
        """
        return self._TransformerEnd

    def setTransformerEnd(self, value):
        if self._TransformerEnd is not None:
            self._TransformerEnd._RatioTapChanger = None

        self._TransformerEnd = value
        if self._TransformerEnd is not None:
            self._TransformerEnd.RatioTapChanger = None
            self._TransformerEnd._RatioTapChanger = self

    TransformerEnd = property(getTransformerEnd, setTransformerEnd)
