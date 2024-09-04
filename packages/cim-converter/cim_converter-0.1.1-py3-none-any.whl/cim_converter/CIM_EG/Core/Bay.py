from cim_converter.CIM_EG.Core.EquipmentContainer import EquipmentContainer


class Bay(EquipmentContainer):

    def __init__(self,
                 bayPowerMeasFlag=False,
                 bayEnergyMeasFlag=False,
                 busBarConfiguration="doubleBus",
                 breakerConfiguration="breakerAndAHalf",
                 VoltageLevel=None,
                 Substation=None,
                 *args,
                 **kw_args):

        self.bayPowerMeasFlag = bayPowerMeasFlag

        self.bayEnergyMeasFlag = bayEnergyMeasFlag

        self.busBarConfiguration = busBarConfiguration

        self.breakerConfiguration = breakerConfiguration

        self._VoltageLevel = None
        self.VoltageLevel = VoltageLevel

        self._Substation = None
        self.Substation = Substation

        super(Bay, self).__init__(*args, **kw_args)

    _attrs = [
        "bayPowerMeasFlag", "bayEnergyMeasFlag", "busBarConfiguration",
        "breakerConfiguration"
    ]
    _attr_types = {
        "bayPowerMeasFlag": bool,
        "bayEnergyMeasFlag": bool,
        "busBarConfiguration": str,
        "breakerConfiguration": str
    }
    _defaults = {
        "bayPowerMeasFlag": False,
        "bayEnergyMeasFlag": False,
        "busBarConfiguration": "doubleBus",
        "breakerConfiguration": "breakerAndAHalf"
    }
    _enums = {
        "busBarConfiguration": "BusbarConfiguration",
        "breakerConfiguration": "BreakerConfiguration"
    }
    _refs = ["VoltageLevel", "Substation"]
    _many_refs = []

    def getVoltageLevel(self):
        """The association is used in the naming hierarchy.
        """
        return self._VoltageLevel

    def setVoltageLevel(self, value):
        if self._VoltageLevel is not None:
            filtered = [x for x in self.VoltageLevel.Bays if x != self]
            self._VoltageLevel._Bays = filtered

        self._VoltageLevel = value
        if self._VoltageLevel is not None:
            if self not in self._VoltageLevel._Bays:
                self._VoltageLevel._Bays.append(self)

    VoltageLevel = property(getVoltageLevel, setVoltageLevel)

    def getSubstation(self):
        """The association is used in the naming hierarchy.
        """
        return self._Substation

    def setSubstation(self, value):
        if self._Substation is not None:
            filtered = [x for x in self.Substation.Bays if x != self]
            self._Substation._Bays = filtered

        self._Substation = value
        if self._Substation is not None:
            if self not in self._Substation._Bays:
                self._Substation._Bays.append(self)

    Substation = property(getSubstation, setSubstation)
