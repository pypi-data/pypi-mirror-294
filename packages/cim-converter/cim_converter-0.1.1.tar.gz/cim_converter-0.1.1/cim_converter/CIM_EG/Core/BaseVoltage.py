from cim_converter.CIM_EG.Core.Equipment import Equipment


class BaseVoltage(Equipment):

    def __init__(self,
                 nominalVoltage=0.0,
                 ConductingEquipment=None,
                 VoltageLevels=None,
                 TransformerEnds=None,
                 *args,
                 **kw_args):

        self.nominalVoltage = nominalVoltage

        self._ConductingEquipment = []
        self.ConductingEquipment = [] if ConductingEquipment is None else ConductingEquipment

        self._VoltageLevels = []
        self.VoltageLevels = [] if VoltageLevels is None else VoltageLevels

        self._TransformerEnds = []
        self.TransformerEnds = [] if TransformerEnds is None else TransformerEnds

        super(BaseVoltage, self).__init__(*args, **kw_args)

    _attrs = ["nominalVoltage"]
    _attr_types = {"nominalVoltage": float}
    _defaults = {"nominalVoltage": 0.0}
    _enums = {}
    _refs = ["ConductingEquipment", "VoltageLevels", "TransformerEnds"]
    _many_refs = ["ConductingEquipment", "VoltageLevels", "TransformerEnds"]

    def getConductingEquipment(self):
        return self._ConductingEquipment

    def setConductingEquipment(self, value):
        for x in self._ConductingEquipment:
            x.BaseVoltage = None
        for y in value:
            y._BaseVoltage = self
        self._ConductingEquipment = value

    ConductingEquipment = property(getConductingEquipment,
                                   setConductingEquipment)

    def addConductingEquipment(self, *ConductingEquipment):
        for obj in ConductingEquipment:
            obj.BaseVoltage = self

    def removeConductingEquipment(self, *ConductingEquipment):
        for obj in ConductingEquipment:
            obj.BaseVoltage = None

    def getVoltageLevels(self):
        return self._VoltageLevels

    def setVoltageLevels(self, value):

        for x in self._VoltageLevels:
            x.BaseVoltage = None
        for y in value:
            y._BaseVoltage = self
        self._VoltageLevels = value

    VoltageLevels = property(getVoltageLevels, setVoltageLevels)

    def addVoltageLevels(self, *VoltageLevels):
        for obj in VoltageLevels:
            obj.BaseVoltage = self

    def removeVoltageLevels(self, *VoltageLevels):
        for obj in VoltageLevels:
            obj.BaseVoltage = None

    def getTransformerEnds(self):
        return self._TransformerEnds

    def setTransformerEnds(self, value):
        for x in self._TransformerEnds:
            x.BaseVoltage = None
        for y in value:
            y._BaseVoltage = self
        self._TransformerEnds = value

    TransformerEnds = property(getTransformerEnds, setTransformerEnds)

    def addTransformerEnds(self, *TransformerEnds):
        for obj in TransformerEnds:
            obj.BaseVoltage = self

    def removeTransformerEnds(self, *TransformerEnds):
        for obj in TransformerEnds:
            obj.BaseVoltage = None
