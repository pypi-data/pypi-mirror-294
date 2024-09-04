from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject

class GeographicalRegion(IdentifiedObject):
    """A geographical region of a power system network model.A geographical region of a power system network model.
    """

    def __init__(self, Regions=None, *args, **kw_args):
        """Initialises a new 'GeographicalRegion' instance.

        @param Regions: The association is used in the naming hierarchy.
        """
        self._Regions = []
        self.Regions = [] if Regions is None else Regions

        super(GeographicalRegion, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Regions"]
    _many_refs = ["Regions"]

    def getRegions(self):
        """The association is used in the naming hierarchy.
        """
        return self._Regions

    def setRegions(self, value):
        for x in self._Regions:
            x.Region = None
        for y in value:
            y._Region = self
        self._Regions = value

    Regions = property(getRegions, setRegions)

    def addRegions(self, *Regions):
        for obj in Regions:
            obj.Region = self

    def removeRegions(self, *Regions):
        for obj in Regions:
            obj.Region = None