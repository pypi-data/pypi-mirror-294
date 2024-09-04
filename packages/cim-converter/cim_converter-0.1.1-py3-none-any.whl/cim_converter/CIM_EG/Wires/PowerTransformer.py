from cim_converter.CIM_EG.Core.ConductingEquipment import ConductingEquipment


class PowerTransformer(ConductingEquipment):

    def __init__(self,
                 AliasName='',
                 PowerTransformerEnd=None,
                 AssetDatasheet=None,
                 *args,
                 **kw_args):

        self.AliasName = AliasName

        self._PowerTransformerEnd = []
        self.PowerTransformerEnd = [] if PowerTransformerEnd is None else PowerTransformerEnd

        self._AssetDatasheet = []
        self.AssetDatasheet = [] if AssetDatasheet is None else AssetDatasheet

        super(PowerTransformer, self).__init__(*args, **kw_args)

    _attrs = ["AliasName"]
    _attr_types = {"AliasName": str}
    _defaults = {"AliasName": ''}
    _enums = {}
    _refs = ["PowerTransformerEnd", "AssetDatasheet"]
    _many_refs = ["PowerTransformerEnd", "AssetDatasheet"]

    def getPowerTransformerEnd(self):
        return self._PowerTransformerEnd

    def setPowerTransformerEnd(self, value):
        for x in self._PowerTransformerEnd:
            x.PowerTransformer = None
        for y in value:
            y._PowerTransformer = self
        self._PowerTransformerEnd = value

    PowerTransformerEnd = property(getPowerTransformerEnd,
                                   setPowerTransformerEnd)

    def addPowerTransformerEnd(self, *PowerTransformerEnd):
        for obj in PowerTransformerEnd:
            obj.PowerTransformer = self

    def removePowerTransformerEnd(self, *PowerTransformerEnd):
        for obj in PowerTransformerEnd:
            obj.PowerTransformer = None

    def getAssetDatasheet(self):
        return self._AssetDatasheet

    def setAssetDatasheet(self, value):
        for x in self._AssetDatasheet:
            x.PowerTransformer = None
        for y in value:
            y._PowerTransformer = self
        self._AssetDatasheet = value

    AssetDatasheet = property(getAssetDatasheet, setAssetDatasheet)

    def addAssetDatasheet(self, *AssetDatasheet):
        for obj in AssetDatasheet:
            self.AssetDatasheet.append(obj)

    def removeAssetDatasheet(self, *AssetDatasheet):
        for obj in AssetDatasheet:
            self.AssetDatasheet.remove(obj)
