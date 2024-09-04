from cim_converter.CIM_EG.AssetModels.TransformerTest import TransformerTest


class NoLoadTest(TransformerTest):

    def __init__(self,
                 excitingCurrent=0.0,
                 lossZero=0.0,
                 excitingCurrentZero=0.0,
                 energisedEndVoltage=0.0,
                 loss=0.0,
                 EnergisedEnd=None,
                 *args,
                 **kw_args):
        self.excitingCurrent = excitingCurrent

        self.lossZero = lossZero

        self.excitingCurrentZero = excitingCurrentZero

        self.energisedEndVoltage = energisedEndVoltage

        self.loss = loss

        self._EnergisedEnd = None
        self.EnergisedEnd = EnergisedEnd

        super(NoLoadTest, self).__init__(*args, **kw_args)

    _attrs = [
        "excitingCurrent", "lossZero", "excitingCurrentZero",
        "energisedEndVoltage", "loss"
    ]
    _attr_types = {
        "excitingCurrent": float,
        "lossZero": float,
        "excitingCurrentZero": float,
        "energisedEndVoltage": float,
        "loss": float
    }
    _defaults = {
        "excitingCurrent": 0.0,
        "lossZero": 0.0,
        "excitingCurrentZero": 0.0,
        "energisedEndVoltage": 0.0,
        "loss": 0.0
    }
    _enums = {}
    _refs = ["EnergisedEnd"]
    _many_refs = []

    def getEnergisedEnd(self):
        """Transformer end that current is applied to in this no-load test.
        """
        return self._EnergisedEnd

    def setEnergisedEnd(self, value):
        if self._EnergisedEnd is not None:
            filtered = [
                x for x in self.EnergisedEnd.EnergisedEndNoLoadTests
                if x != self
            ]
            self._EnergisedEnd._EnergisedEndNoLoadTests = filtered

        self._EnergisedEnd = value
        if self._EnergisedEnd is not None:
            if self not in self._EnergisedEnd._EnergisedEndNoLoadTests:
                self._EnergisedEnd._EnergisedEndNoLoadTests.append(self)

    EnergisedEnd = property(getEnergisedEnd, setEnergisedEnd)
