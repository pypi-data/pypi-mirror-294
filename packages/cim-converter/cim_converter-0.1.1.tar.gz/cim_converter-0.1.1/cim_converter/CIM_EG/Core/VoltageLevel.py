from cim_converter.CIM_EG.Core.EquipmentContainer import EquipmentContainer


class VoltageLevel(EquipmentContainer):

    def __init__(self,
                 BaseVoltage=None,
                 Substation=None,
                 Bays=None,
                 *args,
                 **kw_args):

        self._BaseVoltage = None
        self.BaseVoltage = BaseVoltage

        self._Substation = None
        self.Substation = Substation

        self._Bays = []
        self.Bays = [] if Bays is None else Bays

        super(VoltageLevel, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["BaseVoltage", "Substation", "Bays"]
    _many_refs = ["Bays"]

    def getBaseVoltage(self):
        return self._BaseVoltage

    def setBaseVoltage(self, value):
        if self._BaseVoltage is not None:
            filtered = [x for x in self.BaseVoltage.VoltageLevels if x != self]
            self._BaseVoltage._VoltageLevels = filtered

        self._BaseVoltage = value
        if self._BaseVoltage is not None:
            if self not in self._BaseVoltage._VoltageLevels:
                self._BaseVoltage._VoltageLevels.append(self)

    BaseVoltage = property(getBaseVoltage, setBaseVoltage)

    def getSubstation(self):
        return self._Substation

    def setSubstation(self, value):
        if self._Substation is not None:
            filtered = [x for x in self.Substation.VoltageLevels if x != self]
            self._Substation._VoltageLevels = filtered

        self._Substation = value
        if self._Substation is not None:
            if self not in self._Substation._VoltageLevels:
                self._Substation._VoltageLevels.append(self)

    Substation = property(getSubstation, setSubstation)

    def getBays(self):
        return self._Bays

    def setBays(self, value):
        for x in self._Bays:
            x.VoltageLevels = None
        for y in value:
            y._VoltageLevels = self
        self._Bays = value

    Bays = property(getBays, setBays)

    def addBays(self, *Bays):
        for obj in Bays:
            obj.VoltageLevels = self

    def removeBays(self, *Bays):
        for obj in Bays:
            obj.VoltageLevels = None
