from cim_converter.CIM_EG.Core.EquipmentContainer import EquipmentContainer


class Line(EquipmentContainer):

    def __init__(self, Region=None, *args, **kw_args):

        self._Region = None
        self.Region = Region

        super(Line, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Region"]
    _many_refs = []

    def getRegion(self):
        return self._Region

    def setRegion(self, value):
        if self._Region is not None:
            filtered = [x for x in self.Region.Lines if x != self]
            self._Region._Lines = filtered

        self._Region = value
        if self._Region is not None:
            if self not in self._Region._Lines:
                self._Region._Lines.append(self)

    Region = property(getRegion, setRegion)
