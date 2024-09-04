from cim_converter.CIM_EG.Core.Equipment import Equipment


class AssetInfo(Equipment):

    def __init__(self,
                 Assets=None,
                 PowerSystemResource=None,
                 *args,
                 **kw_args):

        self._Assets = []
        self.Assets = [] if Assets is None else Assets

        self._PowerSystemResource = []
        self.PowerSystemResource = [] if PowerSystemResource is None else PowerSystemResource

        super(AssetInfo, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Assets", "PowerSystemResource"]
    _many_refs = ["Assets", "PowerSystemResource"]

    def getAssets(self):
        return self._Assets

    def setAssets(self, value):
        for x in self._Assets:
            x.AssetInfo = None
        for y in value:
            y._AssetInfo = self
        self._Assets = value

    Assets = property(getAssets, setAssets)

    def addAssets(self, *Assets):
        for obj in Assets:
            obj.AssetInfo = self

    def removeAssets(self, *Assets):
        for obj in Assets:
            obj.AssetInfo = None

    def getPowerSystemResource(self):
        return self._PowerSystemResource

    def setPowerSystemResource(self, value):
        for x in self._PowerSystemResource:
            x.AssetInfo = None
        for y in value:
            y._AssetInfo = self
        self._PowerSystemResource = value

    PowerSystemResource = property(getPowerSystemResource,
                                   setPowerSystemResource)

    def addPowerSystemResource(self, *PowerSystemResource):
        for obj in PowerSystemResource:
            self.PowerSystemResource.append(obj)

    def removePowerSystemResource(self, *PowerSystemResource):
        for obj in PowerSystemResource:
            obj.AssetInfo = None
