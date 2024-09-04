from cim_converter.CIM_EG.Wires.Switch import Switch


class ProtectedSwitch(Switch):

    def __init__(self,
                 breakingCapacity=0.0,
                 ProtectionEquipments=None,
                 RecloseSequences=None,
                 *args,
                 **kw_args):

        self.breakingCapacity = breakingCapacity

        self._ProtectionEquipments = []
        self.ProtectionEquipments = [] if ProtectionEquipments is None else ProtectionEquipments

        self._RecloseSequences = []
        self.RecloseSequences = [] if RecloseSequences is None else RecloseSequences

        super(ProtectedSwitch, self).__init__(*args, **kw_args)

    _attrs = ["breakingCapacity"]
    _attr_types = {"breakingCapacity": float}
    _defaults = {"breakingCapacity": 0.0}
    _enums = {}
    _refs = ["ProtectionEquipments", "RecloseSequences"]
    _many_refs = ["ProtectionEquipments", "RecloseSequences"]

    def getProtectionEquipments(self):
        """Protection equipments that operate this ProtectedSwitch.
        """
        return self._ProtectionEquipments

    def setProtectionEquipments(self, value):
        for p in self._ProtectionEquipments:
            filtered = [q for q in p.ProtectedSwitches if q != self]
            self._ProtectionEquipments._ProtectedSwitches = filtered
        for r in value:
            if self not in r._ProtectedSwitches:
                r._ProtectedSwitches.append(self)
        self._ProtectionEquipments = value

    ProtectionEquipments = property(getProtectionEquipments,
                                    setProtectionEquipments)

    def addProtectionEquipments(self, *ProtectionEquipments):
        for obj in ProtectionEquipments:
            if self not in obj._ProtectedSwitches:
                obj._ProtectedSwitches.append(self)
            self._ProtectionEquipments.append(obj)

    def removeProtectionEquipments(self, *ProtectionEquipments):
        for obj in ProtectionEquipments:
            if self in obj._ProtectedSwitches:
                obj._ProtectedSwitches.remove(self)
            self._ProtectionEquipments.remove(obj)

    def getRecloseSequences(self):
        """A breaker may have zero or more automatic reclosures after a trip occurs.
        """
        return self._RecloseSequences

    def setRecloseSequences(self, value):
        for x in self._RecloseSequences:
            x.ProtectedSwitch = None
        for y in value:
            y._ProtectedSwitch = self
        self._RecloseSequences = value

    RecloseSequences = property(getRecloseSequences, setRecloseSequences)

    def addRecloseSequences(self, *RecloseSequences):
        for obj in RecloseSequences:
            obj.ProtectedSwitch = self

    def removeRecloseSequences(self, *RecloseSequences):
        for obj in RecloseSequences:
            obj.ProtectedSwitch = None
