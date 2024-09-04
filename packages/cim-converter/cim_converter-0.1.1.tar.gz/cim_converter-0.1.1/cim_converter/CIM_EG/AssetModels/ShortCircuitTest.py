from cim_converter.CIM_EG.AssetModels.TransformerTest import TransformerTest


class ShortCircuitTest(TransformerTest):

    def __init__(self,
                 voltage=0.0,
                 lossZero=0.0,
                 leakageImpedance=0.0,
                 loss=0.0,
                 groundedEndStep=0,
                 leakageImpedanceZero=0.0,
                 energisedEndStep=0,
                 GroundedEnds=None,
                 EnergisedEnd=None,
                 *args,
                 **kw_args):

        self.voltage = voltage

        self.lossZero = lossZero

        self.leakageImpedance = leakageImpedance

        self.loss = loss

        self.groundedEndStep = groundedEndStep

        self.leakageImpedanceZero = leakageImpedanceZero

        self.energisedEndStep = energisedEndStep

        self._GroundedEnds = []
        self.GroundedEnds = [] if GroundedEnds is None else GroundedEnds

        self._EnergisedEnd = None
        self.EnergisedEnd = EnergisedEnd

        super(ShortCircuitTest, self).__init__(*args, **kw_args)

    _attrs = [
        "lossZero", "leakageImpedance", "loss", "groundedEndStep",
        "leakageImpedanceZero", "energisedEndStep", "voltage"
    ]
    _attr_types = {
        "lossZero": float,
        "leakageImpedance": float,
        "loss": float,
        "groundedEndStep": int,
        "leakageImpedanceZero": float,
        "energisedEndStep": int,
        "voltage": float
    }
    _defaults = {
        "lossZero": 0.0,
        "leakageImpedance": 0.0,
        "loss": 0.0,
        "groundedEndStep": 0,
        "leakageImpedanceZero": 0.0,
        "energisedEndStep": 0,
        "voltage": 0.0
    }
    _enums = {}
    _refs = ["GroundedEnds", "EnergisedEnd"]
    _many_refs = ["GroundedEnds"]

    def getGroundedEnds(self):
        """All ends short-circuited in this short-circuit test.
        """
        return self._GroundedEnds

    def setGroundedEnds(self, value):
        for p in self._GroundedEnds:
            filtered = [q for q in p.GroundedEndShortCircuitTests if q != self]
            self._GroundedEnds._GroundedEndShortCircuitTests = filtered
        for r in value:
            if self not in r._GroundedEndShortCircuitTests:
                r._GroundedEndShortCircuitTests.append(self)
        self._GroundedEnds = value

    GroundedEnds = property(getGroundedEnds, setGroundedEnds)

    def addGroundedEnds(self, *GroundedEnds):
        for obj in GroundedEnds:
            if self not in obj._GroundedEndShortCircuitTests:
                obj._GroundedEndShortCircuitTests.append(self)
            self._GroundedEnds.append(obj)

    def removeGroundedEnds(self, *GroundedEnds):
        for obj in GroundedEnds:
            if self in obj._GroundedEndShortCircuitTests:
                obj._GroundedEndShortCircuitTests.remove(self)
            self._GroundedEnds.remove(obj)

    def getEnergisedEnd(self):
        """Transformer end that voltage is applied to in this short-circuit test. The test voltage is chosen to induce rated current in the energised end.
        """
        return self._EnergisedEnd

    def setEnergisedEnd(self, value):
        if self._EnergisedEnd is not None:
            filtered = [
                x for x in self.EnergisedEnd.EnergisedEndShortCircuitTests
                if x != self
            ]
            self._EnergisedEnd._EnergisedEndShortCircuitTests = filtered

        self._EnergisedEnd = value
        if self._EnergisedEnd is not None:
            if self not in self._EnergisedEnd._EnergisedEndShortCircuitTests:
                self._EnergisedEnd._EnergisedEndShortCircuitTests.append(self)

    EnergisedEnd = property(getEnergisedEnd, setEnergisedEnd)
