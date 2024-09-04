from cim_converter.CIM_EG.Core.Equipment import Equipment


class RegulatingControl(Equipment):

    def __init__(self,
                 mode="fixed",
                 targetRange=0.0,
                 discrete=False,
                 targetValue=0.0,
                 monitoredPhase="s12N",
                 RegulatingCondEq=None,
                 Terminal=None,
                 RegulationSchedule=None,
                 *args,
                 **kw_args):

        self.mode = mode

        self.targetRange = targetRange

        self.discrete = discrete

        self.targetValue = targetValue

        self.monitoredPhase = monitoredPhase

        self._RegulatingCondEq = []
        self.RegulatingCondEq = [] if RegulatingCondEq is None else RegulatingCondEq

        self._Terminal = None
        self.Terminal = Terminal

        self._RegulationSchedule = []
        self.RegulationSchedule = [] if RegulationSchedule is None else RegulationSchedule

        super(RegulatingControl, self).__init__(*args, **kw_args)

    _attrs = [
        "mode", "targetRange", "discrete", "targetValue", "monitoredPhase"
    ]
    _attr_types = {
        "mode": str,
        "targetRange": float,
        "discrete": bool,
        "targetValue": float,
        "monitoredPhase": str
    }
    _defaults = {
        "mode": "fixed",
        "targetRange": 0.0,
        "discrete": False,
        "targetValue": 0.0,
        "monitoredPhase": "s12N"
    }
    _enums = {
        "mode": "RegulatingControlModeKind",
        "monitoredPhase": "PhaseCode"
    }
    _refs = ["RegulatingCondEq", "Terminal", "RegulationSchedule"]
    _many_refs = ["RegulatingCondEq", "RegulationSchedule"]

    def getRegulatingCondEq(self):
        """The equipment that participates in this regulating control scheme.
        """
        return self._RegulatingCondEq

    def setRegulatingCondEq(self, value):
        for x in self._RegulatingCondEq:
            x.RegulatingControl = None
        for y in value:
            y._RegulatingControl = self
        self._RegulatingCondEq = value

    RegulatingCondEq = property(getRegulatingCondEq, setRegulatingCondEq)

    def addRegulatingCondEq(self, *RegulatingCondEq):
        for obj in RegulatingCondEq:
            obj.RegulatingControl = self

    def removeRegulatingCondEq(self, *RegulatingCondEq):
        for obj in RegulatingCondEq:
            obj.RegulatingControl = None

    def getTerminal(self):
        """The terminal associated with this regulating control.
        """
        return self._Terminal

    def setTerminal(self, value):
        if self._Terminal is not None:
            filtered = [
                x for x in self.Terminal.RegulatingControl if x != self
            ]
            self._Terminal._RegulatingControl = filtered

        self._Terminal = value
        if self._Terminal is not None:
            if self not in self._Terminal._RegulatingControl:
                self._Terminal._RegulatingControl.append(self)

    Terminal = property(getTerminal, setTerminal)

    def getRegulationSchedule(self):
        """Schedule for this Regulating regulating control.
        """
        return self._RegulationSchedule

    def setRegulationSchedule(self, value):
        for x in self._RegulationSchedule:
            x.RegulatingControl = None
        for y in value:
            y._RegulatingControl = self
        self._RegulationSchedule = value

    RegulationSchedule = property(getRegulationSchedule, setRegulationSchedule)

    def addRegulationSchedule(self, *RegulationSchedule):
        for obj in RegulationSchedule:
            obj.RegulatingControl = self

    def removeRegulationSchedule(self, *RegulationSchedule):
        for obj in RegulationSchedule:
            obj.RegulatingControl = None
