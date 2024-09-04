from cim_converter.CIM_EG.Core.Equipment import Equipment


class CoordinateSystem(Equipment):

    def __init__(self, crsUrn='', Locations=None, *args, **kw_args):

        self.crsUrn = crsUrn

        self._Locations = []
        self.Locations = [] if Locations is None else Locations

        super(CoordinateSystem, self).__init__(*args, **kw_args)

    _attrs = ["crsUrn"]
    _attr_types = {"crsUrn": str}
    _defaults = {"crsUrn": ''}
    _enums = {}
    _refs = ["Locations"]
    _many_refs = ["Locations"]

    def getLocations(self):
        return self._Locations

    def setLocations(self, value):
        for x in self._Locations:
            x.CoordinateSystem = None
        for y in value:
            y._CoordinateSystem = self
        self._Locations = value

    Locations = property(getLocations, setLocations)

    def addLocations(self, *Locations):
        for obj in Locations:
            obj.CoordinateSystem = self

    def removeLocations(self, *Locations):
        for obj in Locations:
            obj.CoordinateSystem = None
