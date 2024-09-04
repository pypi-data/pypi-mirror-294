from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject

class SubGeographicalRegion(IdentifiedObject):
    """A subset of a geographical region of a power system network model.A subset of a geographical region of a power system network model.
    """

    def __init__(self, Substations=None, Lines=None, Region=None, *args, **kw_args):
        """Initialises a new 'SubGeographicalRegion' instance.

        @param Substations: The association is used in the naming hierarchy.
        @param Lines: A Line can be contained by a SubGeographical Region.
        @param Region: The association is used in the naming hierarchy.
        """
        self._Substations = []
        self.Substations = [] if Substations is None else Substations

        self._Lines = []
        self.Lines = [] if Lines is None else Lines

        self._Region = None
        self.Region = Region

        super(SubGeographicalRegion, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Substations", "Lines", "Region"]
    _many_refs = ["Substations", "Lines"]

    def getSubstations(self):
        """The association is used in the naming hierarchy.
        """
        return self._Substations

    def setSubstations(self, value):
        for x in self._Substations:
            x.Region = None
        for y in value:
            y._Region = self
        self._Substations = value

    Substations = property(getSubstations, setSubstations)

    def addSubstations(self, *Substations):
        for obj in Substations:
            obj.Region = self

    def removeSubstations(self, *Substations):
        for obj in Substations:
            obj.Region = None

    def getLines(self):
        """A Line can be contained by a SubGeographical Region.
        """
        return self._Lines

    def setLines(self, value):
        for x in self._Lines:
            x.Region = None
        for y in value:
            y._Region = self
        self._Lines = value

    Lines = property(getLines, setLines)

    def addLines(self, *Lines):
        for obj in Lines:
            obj.Region = self

    def removeLines(self, *Lines):
        for obj in Lines:
            obj.Region = None

    def getRegion(self):
        """The association is used in the naming hierarchy.
        """
        return self._Region

    def setRegion(self, value):
        if self._Region is not None:
            filtered = [x for x in self.Region.Regions if x != self]
            self._Region._Regions = filtered

        self._Region = value
        if self._Region is not None:
            if self not in self._Region._Regions:
                self._Region._Regions.append(self)

    Region = property(getRegion, setRegion)