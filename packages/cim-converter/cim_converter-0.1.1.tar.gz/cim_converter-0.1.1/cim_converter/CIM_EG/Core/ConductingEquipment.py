from cim_converter.CIM_EG.Core.Equipment import Equipment


class ConductingEquipment(Equipment):

    def __init__(self,
                 BaseVoltage=None,
                 Terminals=None,
                 ProtectionEquipments=None,
                 *args,
                 **kw_args):

        self._BaseVoltage = None
        self.BaseVoltage = BaseVoltage

        self._Terminals = []
        self.Terminals = [] if Terminals is None else Terminals

        self._ProtectionEquipments = []
        self.ProtectionEquipments = [] if ProtectionEquipments is None else ProtectionEquipments

        super(ConductingEquipment, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["BaseVoltage", "Terminals", "ProtectionEquipments"]
    _many_refs = ["Terminals", "ProtectionEquipments"]

    def getBaseVoltage(self):
        return self._BaseVoltage

    def setBaseVoltage(self, value):
        if self._BaseVoltage is not None:
            filtered = [
                x for x in self.BaseVoltage.ConductingEquipment if x != self
            ]
            self._BaseVoltage._ConductingEquipment = filtered

        self._BaseVoltage = value
        if self._BaseVoltage is not None:
            if self not in self._BaseVoltage._ConductingEquipment:
                self._BaseVoltage._ConductingEquipment.append(self)

    BaseVoltage = property(getBaseVoltage, setBaseVoltage)

    def getTerminals(self):
        """ConductingEquipment has 1 or 2 terminals that may be connected to other ConductingEquipment terminals via ConnectivityNodes
        """
        return self._Terminals

    def setTerminals(self, value):
        for x in self._Terminals:
            x.ConductingEquipment = None
        for y in value:
            y._ConductingEquipment = self
        self._Terminals = value

    Terminals = property(getTerminals, setTerminals)

    def addTerminals(self, *Terminals):
        for obj in Terminals:
            obj.ConductingEquipment = self

    def removeTerminals(self, *Terminals):
        for obj in Terminals:
            obj.ConductingEquipment = None

    def getProtectionEquipments(self):
        return self._ProtectionEquipments

    def setProtectionEquipments(self, value):

        for x in self._ProtectionEquipments:
            x.ConductingEquipment = None
        for y in value:
            y._ConductingEquipment = self
        self._ProtectionEquipments = value

    ProtectionEquipments = property(getProtectionEquipments,
                                    setProtectionEquipments)

    def addProtectionEquipments(self, *ProtectionEquipments):
        for obj in ProtectionEquipments:
            obj.ConductingEquipment = self

    def removeProtectionEquipments(self, *ProtectionEquipments):
        for obj in ProtectionEquipments:
            obj.ConductingEquipment = None
