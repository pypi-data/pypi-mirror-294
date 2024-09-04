from cim_converter.CIM_EG.Core.PowerSystemResource import PowerSystemResource


class Equipment(PowerSystemResource):

    def __init__(self,
                 normallyInService=True,
                 inService=False,
                 EquipmentContainer=None,
                 AdditionalEquipmentContainer=None,
                 UsagePoints=None,
                 *args,
                 **kw_args):

        self.normallyInService = normallyInService

        self.inService = inService

        self._EquipmentContainer = None
        self.EquipmentContainer = EquipmentContainer

        self._AdditionalEquipmentContainer = []
        self.AdditionalEquipmentContainer = [] if AdditionalEquipmentContainer is None else AdditionalEquipmentContainer

        self._UsagePoints = []
        self.UsagePoints = [] if UsagePoints is None else UsagePoints

        super(Equipment, self).__init__(*args, **kw_args)

    _attrs = ["normallyInService", "inService"]
    _attr_types = {"normallyInService": bool, "inService": bool}
    _defaults = {"normallyInService": True, "inService": False}
    _enums = {}
    _refs = [
        "EquipmentContainer", "AdditionalEquipmentContainer", "UsagePoints"
    ]
    _many_refs = ["AdditionalEquipmentContainer", "UsagePoints"]

    def getEquipmentContainer(self):
        return self._EquipmentContainer

    def setEquipmentContainer(self, value):
        if self._EquipmentContainer is not None:
            filtered = [
                x for x in self.EquipmentContainer.Equipments if x != self
            ]
            self._EquipmentContainer._Equipments = filtered
        if value is not None:
            value._Equipments.append(self)
        self._EquipmentContainer = value

    EquipmentContainer = property(getEquipmentContainer, setEquipmentContainer)

    def getAdditionalEquipmentContainer(self):
        return self._AdditionalEquipmentContainer

    def setAdditionalEquipmentContainer(self, value):
        for x in self._AdditionalEquipmentContainer:
            x.Equipment = None
        for y in value:
            y._Equipment = self
        self._AdditionalEquipmentContainer = value

    AdditionalEquipmentContainer = property(getAdditionalEquipmentContainer,
                                            setAdditionalEquipmentContainer)

    def addAdditionalEquipmentContainer(self, *AdditionalEquipmentContainer):
        for obj in AdditionalEquipmentContainer:
            obj.Equipment = self

    def getUsagePoints(self):
        return self._UsagePoints

    def setUsagePoints(self, value):
        for x in self._UsagePoints:
            x.Equipment = None
        for y in value:
            y._Equipment = self
        self._UsagePoints = value

    UsagePoints = property(getUsagePoints, setUsagePoints)

    def addUsagePoints(self, *UsagePoints):
        for obj in UsagePoints:
            self.UsagePoints.append(obj)

    def removeUsagePoints(self, *UsagePoints):
        for obj in UsagePoints:
            obj.Equipment = None
