from cim_converter.CIM_EG.Assets.AssetInfo import AssetInfo


class WireInfo(AssetInfo):

    def __init__(self,
                 material='aluminum',
                 sizeDescription='',
                 ratedCurrent='',
                 gmr='',
                 rDC20='',
                 coreRadius='',
                 radius='',
                 WirePhaseInfo=None,
                 PerLengthParameters=None,
                 *args,
                 **kw_args):

        self.material = material

        self.sizeDescription = sizeDescription

        self.ratedCurrent = ratedCurrent

        self.gmr = gmr

        self.rDC20 = rDC20

        self.coreRadius = coreRadius

        self.radius = radius

        self._WirePhaseInfo = []
        self.WirePhaseInfo = [] if WirePhaseInfo is None else WirePhaseInfo

        self._PerLengthParameters = None
        self.PerLengthParameters = PerLengthParameters

        super(WireInfo, self).__init__(*args, **kw_args)

    _attrs = [
        "material", "sizeDescription", "ratedCurrent", "gmr", "rDC20",
        "coreRadius", "radius"
    ]
    _attr_types = {
        "material": str,
        "sizeDescription": str,
        "ratedCurrent": str,
        "gmr": str,
        "rDC20": str,
        "coreRadius": str,
        "radius": str
    }
    _defaults = {
        "material": 'aluminum',
        "sizeDescription": '',
        "ratedCurrent": '',
        "gmr": '',
        "rDC20": '',
        "coreRadius": '',
        "radius": ''
    }
    _enums = {"material": "WireMaterialKind"}
    _refs = ["WirePhaseInfo", "PerLengthParameters"]
    _many_refs = ["WirePhaseInfo", "PerLengthParameters"]

    def getWirePhaseInfo(self):
        return self._WirePhaseInfo

    def setWirePhaseInfo(self, value):
        for x in self._WirePhaseInfo:
            x.WireInfo = None
        for y in value:
            y._WireInfo = self
        self._WirePhaseInfo = value

    WirePhaseInfo = property(getWirePhaseInfo, setWirePhaseInfo)

    def addWirePhaseInfo(self, *WirePhaseInfo):
        for obj in WirePhaseInfo:
            obj.WireInfo = self

    def removeWirePhaseInfo(self, *WirePhaseInfo):
        for obj in WirePhaseInfo:
            obj.WireInfo = None

    def getPerLengthParameters(self):
        return self._PerLengthParameters

    def setPerLengthParameters(self, value):
        if self._PerLengthParameters is not None:
            filtered = [
                x for x in self.PerLengthParameters.WireInfos if x != self
            ]
            self._PerLengthParameters._WireInfos = filtered
        if value is not None:
            value.WireInfos.append(self)
        self._PerLengthParameters = value

    PerLengthParameters = property(getPerLengthParameters,
                                   setPerLengthParameters)
