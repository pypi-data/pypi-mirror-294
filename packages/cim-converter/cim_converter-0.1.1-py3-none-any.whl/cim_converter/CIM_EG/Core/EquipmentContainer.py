from cim_converter.CIM_EG.Core.ConnectivityNodeContainer import ConnectivityNodeContainer


class EquipmentContainer(ConnectivityNodeContainer):

    def __init__(self, Equipments=None, *args, **kw_args):

        self._Equipments = []
        self.Equipments = [] if Equipments is None else Equipments

        super(EquipmentContainer, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Equipments"]
    _many_refs = ["Equipments"]

    def getEquipments(self):
        return self._Equipments

    def setEquipments(self, value):
        for x in self._Equipments:
            x.EquipmentContainer = None
        for y in value:
            y._EquipmentContainer = self
        self._Equipments = value

    Equipments = property(getEquipments, setEquipments)

    def addEquipments(self, *Equipments):
        for obj in Equipments:
            obj.EquipmentContainer = self

    def removeEquipments(self, *Equipments):
        for obj in Equipments:
            obj.EquipmentContainer = None
