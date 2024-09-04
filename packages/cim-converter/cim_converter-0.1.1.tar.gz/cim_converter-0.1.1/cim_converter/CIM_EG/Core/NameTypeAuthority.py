from cim_converter.CIM_EG.Element import Element


class NameTypeAuthority(Element):

    def __init__(self,
                 name='',
                 description='',
                 NameTypes=None,
                 *args,
                 **kw_args):
        self.name = name
        self.description = description

        self._NameTypes = []
        self.NameTypes = [] if NameTypes is None else NameTypes

        super(NameTypeAuthority, self).__init__(*args, **kw_args)

    _attrs = ["name", "description"]
    _attr_types = {"name": str, "description": str}
    _defaults = {"name": '', "description": ''}
    _enums = {}
    _refs = ["NameTypes"]
    _many_refs = ["NameTypes"]

    def getNameTypes(self):
        """All name types managed by this authority.
        """
        return self._NameTypes

    def setNameTypes(self, value):
        for x in self._NameTypes:
            x.NameTypeAuthority = None
        for y in value:
            y._NameTypeAuthority = self
        self._NameTypes = value

    NameTypes = property(getNameTypes, setNameTypes)

    def addNameTypes(self, *NameTypes):
        for obj in NameTypes:
            obj.NameTypeAuthority = self

    def removeNameTypes(self, *NameTypes):
        for obj in NameTypes:
            obj.NameTypeAuthority = None
