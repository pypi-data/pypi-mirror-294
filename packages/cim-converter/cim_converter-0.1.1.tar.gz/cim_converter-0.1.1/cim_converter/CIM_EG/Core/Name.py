from cim_converter.CIM_EG.Element import Element


class Name(Element):

    def __init__(self,
                 name='',
                 NameType=None,
                 IdentifiedObject=None,
                 *args,
                 **kw_args):
        self.name = name

        self._NameType = None
        self.NameType = NameType

        self._IdentifiedObject = None
        self.IdentifiedObject = IdentifiedObject

        super(Name, self).__init__(*args, **kw_args)

    _attrs = ["name"]
    _attr_types = {"name": str}
    _defaults = {"name": ''}
    _enums = {}
    _refs = ["NameType", "IdentifiedObject"]
    _many_refs = []

    def getNameType(self):
        """Type of this name.
        """
        return self._NameType

    def setNameType(self, value):
        if self._NameType is not None:
            filtered = [x for x in self.NameType.Names if x != self]
            self._NameType._Names = filtered

        self._NameType = value
        if self._NameType is not None:
            if self not in self._NameType._Names:
                self._NameType._Names.append(self)

    NameType = property(getNameType, setNameType)

    def getIdentifiedObject(self):
        """Identified object that this name designates.
        """
        return self._IdentifiedObject

    def setIdentifiedObject(self, value):
        if self._IdentifiedObject is not None:
            filtered = [x for x in self.IdentifiedObject.Names if x != self]
            self._IdentifiedObject._Names = filtered

        self._IdentifiedObject = value
        if self._IdentifiedObject is not None:
            if self not in self._IdentifiedObject._Names:
                self._IdentifiedObject._Names.append(self)

    IdentifiedObject = property(getIdentifiedObject, setIdentifiedObject)
