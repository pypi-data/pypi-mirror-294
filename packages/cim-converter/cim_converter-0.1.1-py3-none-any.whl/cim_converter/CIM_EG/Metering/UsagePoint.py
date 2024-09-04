from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class UsagePoint(IdentifiedObject):

    def __init__(self,
                 connectionState='',
                 ratedPower=0.0,
                 connectionCategory='',
                 Equipments=None,
                 *args,
                 **kw_args):

        self.connectionState = connectionState

        self.ratedPower = ratedPower

        self.connectionCategory = connectionCategory

        self._Equipments = []
        self.Equipments = [] if Equipments is None else Equipments

        super(UsagePoint, self).__init__(*args, **kw_args)

    _attrs = ["connectionState", "ratedPower", "connectionCategory"]
    _attr_types = {
        "connectionState": str,
        "ratedPower": float,
        "connectionCategory": str
    }
    _defaults = {
        "connectionState": '',
        "ratedPower": 0.0,
        "connectionCategory": ''
    }
    _enums = {}
    _refs = ["Equipments"]
    _many_refs = ["Equipments"]

    def getEquipments(self):
        return self._Equipments

    def setEquipments(self, value):
        for x in self._Equipments:
            x.UsagePoint = None
        for y in value:
            y._UsagePoint = self
        self._Equipments = value

    Equipments = property(getEquipments, setEquipments)

    def addEquipments(self, *Equipments):
        for obj in Equipments:
            self.Equipments.append(obj)

    def removeEquipments(self, *Equipments):
        for obj in Equipments:
            obj.UsagePoint = None
