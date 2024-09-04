from cim_converter.CIM_EG.Element import Element


class NameType(Element):

    def __init__(self,
                 name='',
                 description='',
                 Names=None,
                 NameTypeAuthority=None,
                 *args,
                 **kw_args):
        self.name = name
        self.description = description

        self._Names = []
        self.Names = [] if Names is None else Names

        self._NameTypeAuthority = None
        self.NameTypeAuthority = NameTypeAuthority

        super(NameType, self).__init__(*args, **kw_args)

    _attrs = ["name", "description"]
    _attr_types = {"name": str, "description": str}
    _defaults = {"name": '', "description": ''}
    _enums = {}
    _refs = ["Names", "NameTypeAuthority"]
    _many_refs = ["Names"]

    def getNames(self):
        """All names of this type.
        """
        return self._Names

    def setNames(self, value):
        for x in self._Names:
            x.NameType = None
        for y in value:
            y._NameType = self
        self._Names = value

    Names = property(getNames, setNames)

    def addNames(self, *Names):
        for obj in Names:
            obj.NameType = self

    def removeNames(self, *Names):
        for obj in Names:
            obj.NameType = None

    def getNameTypeAuthority(self):
        """Authority responsible for managing names of this type.
        """
        return self._NameTypeAuthority

    def setNameTypeAuthority(self, value):
        if self._NameTypeAuthority is not None:
            filtered = [
                x for x in self.NameTypeAuthority.NameTypes if x != self
            ]
            self._NameTypeAuthority._NameTypes = filtered

        self._NameTypeAuthority = value
        if self._NameTypeAuthority is not None:
            if self not in self._NameTypeAuthority._NameTypes:
                self._NameTypeAuthority._NameTypes.append(self)

    NameTypeAuthority = property(getNameTypeAuthority, setNameTypeAuthority)
