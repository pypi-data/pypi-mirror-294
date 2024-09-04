from cim_converter.CIM_EG.Element import Element


class IdentifiedObject(Element):

    def __init__(self,
                 mRID='',
                 aliasName='',
                 description='',
                 name='',
                 Names=None,
                 *args,
                 **kw_args):
        self.mRID = mRID
        self.aliasName = aliasName
        self.description = description
        self.name = name

        self._Names = []
        self.Names = [] if Names is None else Names

        super(IdentifiedObject, self).__init__(*args, **kw_args)

    _attrs = ["mRID", "aliasName", "description", "name"]
    _attr_types = {
        "mRID": str,
        "aliasName": str,
        "description": str,
        "name": str
    }
    _defaults = {"mRID": '', "aliasName": '', "description": '', "name": ''}
    _enums = {}
    _refs = ["Names"]
    _many_refs = ["Names"]

    def getNames(self):
        return self._Names

    def setNames(self, value):
        for x in self._Names:
            x.IdentifiedObject = None
        for y in value:
            y._IdentifiedObject = self
        self._Names = value

    Names = property(getNames, setNames)

    def addNames(self, *Names):
        for obj in Names:
            obj.IdentifiedObject = self

    def removeNames(self, *Names):
        for obj in Names:
            obj.IdentifiedObject = None
