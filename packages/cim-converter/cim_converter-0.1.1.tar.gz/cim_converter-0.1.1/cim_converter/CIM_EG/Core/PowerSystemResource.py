from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class PowerSystemResource(IdentifiedObject):

    def __init__(self,
                 *args,
                 PSRType=None,
                 Location=None,
                 Assets=None,
                 **kw_args):
        """Initialises a new 'PowerSystemResource' instance.

        @param AssetDataSheet: 
        @param Assets: 
        @param Location: 
        @param PSRType: 
        """

        self._Location = None
        self.Location = Location

        super(PowerSystemResource, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ['Assets', 'Location', 'PSRType']
    _many_refs = ['Assets']

    def getAssets(self):

        return self.Assets

    def setAssets(self, value):
        for x in self.Assets:
            x.PowerSystemResource = None
        for y in value:
            y._PowerSystemResource = self
        self._Assets = value

    Assets = property(getAssets, setAssets)

    def addAssets(self, *Assets):
        for obj in Assets:
            obj.PowerSystemResource = self

    def removeAssets(self, *Assets):
        for obj in Assets:
            obj.PowerSystemResource = None

    def getLocation(self):
        """Location of this power system resource.
        """
        return self._Location

    def setLocation(self, value):
        if self._Location is not None:
            filtered = [
                x for x in self.Location.PowerSystemResources if x != self
            ]
            self._Location._PowerSystemResources = filtered

        self._Location = value
        if self._Location is not None:
            if self not in self._Location._PowerSystemResources:
                self._Location._PowerSystemResources.append(self)

    Location = property(getLocation, setLocation)

    def getPSRType(self):

        return self.PSRType

    def setPSRType(self, value):
        if self.PSRType != value:
            self.PSRType = value

    PSRType = property(getPSRType, setPSRType)
