from cim_converter.CIM_EG.Core.EquipmentContainer import EquipmentContainer


class Substation(EquipmentContainer):

    def __init__(self,
                 Bays=None,
                 VoltageLevels=None,
                 Region=None,
                 *args,
                 **kw_args):

        self._Bays = []
        self.Bays = [] if Bays is None else Bays

        self._VoltageLevels = []
        self.VoltageLevels = [] if VoltageLevels is None else VoltageLevels

        self._Region = None
        self.Region = Region

        super(Substation, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Bays", "VoltageLevels", "Region"]
    _many_refs = ["Bays", "VoltageLevels"]

    def getBays(self):
        """The association is used in the naming hierarchy.
        """
        return self._Bays

    def setBays(self, value):
        for x in self._Bays:
            x.Substation = None
        for y in value:
            y._Substation = self
        self._Bays = value

    Bays = property(getBays, setBays)

    def addBays(self, *Bays):
        for obj in Bays:
            obj.Substation = self

    def removeBays(self, *Bays):
        for obj in Bays:
            obj.Substation = None

    def getVoltageLevels(self):
        """The association is used in the naming hierarchy.
        """
        return self._VoltageLevels

    def setVoltageLevels(self, value):
        for x in self._VoltageLevels:
            x.Substation = None
        for y in value:
            y._Substation = self
        self._VoltageLevels = value

    VoltageLevels = property(getVoltageLevels, setVoltageLevels)

    def addVoltageLevels(self, *VoltageLevels):
        for obj in VoltageLevels:
            obj.Substation = self

    def removeVoltageLevels(self, *VoltageLevels):
        for obj in VoltageLevels:
            obj.Substation = None

    def getRegion(self):
        """The association is used in the naming hierarchy.
        """
        return self._Region

    def setRegion(self, value):
        if self._Region is not None:
            filtered = [x for x in self.Region.Substations if x != self]
            self._Region._Substations = filtered

        self._Region = value
        if self._Region is not None:
            if self not in self._Region._Substations:
                self._Region._Substations.append(self)

    Region = property(getRegion, setRegion)
