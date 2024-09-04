from cim_converter.CIM_EG.Core.Equipment import Equipment


class TapChanger(Equipment):
    """Mechanism for changing transformer winding tap positions.Mechanism for changing transformer winding tap positions.
    """

    def __init__(self,
                 neutralU=0.0,
                 regulationStatus=False,
                 subsequentDelay=0.0,
                 normalStep=0,
                 ltcFlag=False,
                 lowStep=0,
                 neutralStep=0,
                 initialDelay=0.0,
                 highStep=0,
                 TapChangerInfo=None,
                 TapSchedules=None,
                 TapChangerControl=None,
                 SvTapStep=None,
                 *args,
                 **kw_args):
        self.neutralU = neutralU

        self.regulationStatus = regulationStatus

        self.subsequentDelay = subsequentDelay

        self.normalStep = normalStep

        self.ltcFlag = ltcFlag

        self.lowStep = lowStep

        self.neutralStep = neutralStep

        self.initialDelay = initialDelay

        self.highStep = highStep

        self._TapChangerInfo = None
        self.TapChangerInfo = TapChangerInfo

        self._TapSchedules = []
        self.TapSchedules = [] if TapSchedules is None else TapSchedules

        self._TapChangerControl = None
        self.TapChangerControl = TapChangerControl

        self._SvTapStep = None
        self.SvTapStep = SvTapStep

        super(TapChanger, self).__init__(*args, **kw_args)

    _attrs = [
        "neutralU", "regulationStatus", "subsequentDelay", "normalStep",
        "ltcFlag", "lowStep", "neutralStep", "initialDelay", "highStep"
    ]
    _attr_types = {
        "neutralU": float,
        "regulationStatus": bool,
        "subsequentDelay": float,
        "normalStep": int,
        "ltcFlag": bool,
        "lowStep": int,
        "neutralStep": int,
        "initialDelay": float,
        "highStep": int
    }
    _defaults = {
        "neutralU": 0.0,
        "regulationStatus": False,
        "subsequentDelay": 0.0,
        "normalStep": 0,
        "ltcFlag": False,
        "lowStep": 0,
        "neutralStep": 0,
        "initialDelay": 0.0,
        "highStep": 0
    }
    _enums = {}
    _refs = [
        "TapChangerInfo", "TapSchedules", "TapChangerControl", "SvTapStep"
    ]
    _many_refs = ["TapSchedules"]

    def getTapChangerInfo(self):
        """Data for this tap changer.
        """
        return self._TapChangerInfo

    def setTapChangerInfo(self, value):
        if self._TapChangerInfo is not None:
            filtered = [
                x for x in self.TapChangerInfo.TapChangers if x != self
            ]
            self._TapChangerInfo._TapChangers = filtered

        self._TapChangerInfo = value
        if self._TapChangerInfo is not None:
            if self not in self._TapChangerInfo._TapChangers:
                self._TapChangerInfo._TapChangers.append(self)

    TapChangerInfo = property(getTapChangerInfo, setTapChangerInfo)

    def getTapSchedules(self):
        """A TapChanger can have TapSchedules.
        """
        return self._TapSchedules

    def setTapSchedules(self, value):
        for x in self._TapSchedules:
            x.TapChanger = None
        for y in value:
            y._TapChanger = self
        self._TapSchedules = value

    TapSchedules = property(getTapSchedules, setTapSchedules)

    def addTapSchedules(self, *TapSchedules):
        for obj in TapSchedules:
            obj.TapChanger = self

    def removeTapSchedules(self, *TapSchedules):
        for obj in TapSchedules:
            obj.TapChanger = None

    def getTapChangerControl(self):

        return self._TapChangerControl

    def setTapChangerControl(self, value):
        if self._TapChangerControl is not None:
            filtered = [
                x for x in self.TapChangerControl.TapChanger if x != self
            ]
            self._TapChangerControl._TapChanger = filtered

        self._TapChangerControl = value
        if self._TapChangerControl is not None:
            if self not in self._TapChangerControl._TapChanger:
                self._TapChangerControl._TapChanger.append(self)

    TapChangerControl = property(getTapChangerControl, setTapChangerControl)

    def getSvTapStep(self):
        """The tap step state associated with the tap changer.
        """
        return self._SvTapStep

    def setSvTapStep(self, value):
        if self._SvTapStep is not None:
            self._SvTapStep._TapChanger = None

        self._SvTapStep = value
        if self._SvTapStep is not None:
            self._SvTapStep.TapChanger = None
            self._SvTapStep._TapChanger = self

    SvTapStep = property(getSvTapStep, setSvTapStep)
