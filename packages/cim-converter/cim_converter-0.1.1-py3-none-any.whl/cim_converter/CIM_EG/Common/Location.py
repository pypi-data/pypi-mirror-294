from cim_converter.CIM_EG.Core.Equipment import Equipment


class Location(Equipment):

    def __init__(self,
                 geoInfoReference='',
                 direction='',
                 secondaryAddress='',
                 type='',
                 electronicAddress='',
                 mainAddress='',
                 status='',
                 CoordinateSystem=None,
                 Assets=None,
                 PowerSystemResources=None,
                 PositionPoints=None,
                 *args,
                 **kw_args):

        self.geoInfoReference = geoInfoReference
        self.direction = direction
        self.secondaryAddress = secondaryAddress
        self.type = type
        self.electronicAddress = electronicAddress
        self.mainAddress = mainAddress
        self.status = status

        self._CoordinateSystem = None
        self.CoordinateSystem = CoordinateSystem

        self._Assets = []
        self.Assets = [] if Assets is None else Assets

        self._PowerSystemResources = []
        self.PowerSystemResources = [] if PowerSystemResources is None else PowerSystemResources

        self._PositionPoints = []
        self.PositionPoints = [] if PositionPoints is None else PositionPoints

        super(Location, self).__init__(*args, **kw_args)

    _attrs = [
        "geoInfoReference", "direction", "secondaryAddress", "type",
        "electronicAddress", "mainAddress", "status"
    ]
    _attr_types = {
        "geoInfoReference": str,
        "direction": str,
        "secondaryAddress": str,
        "type": str,
        "electronicAddress": str,
        "mainAddress": str,
        "status": str,
    }
    _defaults = {
        "geoInfoReference": '',
        "direction": '',
        "secondaryAddress": '',
        "type": '',
        "electronicAddress": '',
        "mainAddress": '',
        "status": '',
    }
    _enums = {}
    _refs = [
        "CoordinateSystem", "Assets", "PowerSystemResources", "PositionPoints"
    ]
    _many_refs = ["Assets", "PowerSystemResources", "PositionPoints"]

    def getCoordinateSystem(self):
        return self._CoordinateSystem

    def setCoordinateSystem(self, value):
        if self._CoordinateSystem is not None:
            filtered = [
                x for x in self.CoordinateSystem.Locations if x != self
            ]
            self._CoordinateSystem._Locations = filtered

        self._CoordinateSystem = value
        if self._CoordinateSystem is not None:
            if self not in self._CoordinateSystem._Locations:
                self._CoordinateSystem._Locations.append(self)

    CoordinateSystem = property(getCoordinateSystem, setCoordinateSystem)

    def getAssets(self):
        return self._Assets

    def setAssets(self, value):
        for x in self._Assets:
            x.Location = None
        for y in value:
            y._Location = self
        self._Assets = value

    Assets = property(getAssets, setAssets)

    def addAssets(self, *Assets):
        for obj in Assets:
            obj.Location = self

    def removeAssets(self, *Assets):
        for obj in Assets:
            obj.Location = None

    def getPowerSystemResources(self):
        return self._PowerSystemResources

    def setPowerSystemResources(self, value):
        for x in self._PowerSystemResources:
            x.Location = None
        for y in value:
            y._Location = self
        self._PowerSystemResources = value

    PowerSystemResources = property(getPowerSystemResources,
                                    setPowerSystemResources)

    def addPowerSystemResources(self, *PowerSystemResources):
        for obj in PowerSystemResources:
            obj.Location = self

    def removePowerSystemResources(self, *PowerSystemResources):
        for obj in PowerSystemResources:
            obj.Location = None

    def getPositionPoints(self):
        return self._PositionPoints

    def setPositionPoints(self, value):
        for x in self._PositionPoints:
            x.Location = None
        for y in value:
            y._Location = self
        self._PositionPoints = value

    PositionPoints = property(getPositionPoints, setPositionPoints)

    def addPositionPoints(self, *PositionPoints):
        for obj in PositionPoints:
            obj.Location = self

    def removePositionPoints(self, *PositionPoints):
        for obj in PositionPoints:
            obj.Location = None
