from cim_converter.CIM_EG.AuxiliaryEquipment.Sensor import Sensor


class CurrentTransformer(Sensor):

    def __init__(self,
                 AliasName='',
                 ctClass='',
                 accuracyLimit='',
                 usage='',
                 accuracyClass='',
                 coreCount=0,
                 maxRatio=0.0,
                 CTInfo=None,
                 *args,
                 **kw_args):

        self.AliasName = AliasName

        self.ctClass = ctClass

        self.accuracyLimit = accuracyLimit

        self.usage = usage

        self.accuracyClass = accuracyClass

        self.coreCount = coreCount

        self.maxRatio = maxRatio

        self._CTInfo = None
        self.CTInfo = CTInfo

        super(CurrentTransformer, self).__init__(*args, **kw_args)

    _attrs = [
        "ctClass", "accuracyLimit", "usage", "accuracyClass", "coreCount",
        "maxRatio", "AliasName"
    ]
    _attr_types = {
        "ctClass": str,
        "accuracyLimit": str,
        "usage": str,
        "accuracyClass": str,
        "coreCount": int,
        "maxRatio": float,
        "AliasName": str
    }
    _defaults = {
        "ctClass": '',
        "accuracyLimit": '',
        "usage": '',
        "accuracyClass": '',
        "coreCount": 0,
        "maxRatio": 0.0,
        "AliasName": ''
    }
    _enums = {}
    _refs = ["CTInfo"]
    _many_refs = []

    def getCTInfo(self):
        """Current transformer data.
        """
        return self._CTInfo

    def setCTInfo(self, value):
        if self._CTInfo is not None:
            filtered = [x for x in self.CTInfo.CTs if x != self]
            self._CTInfo._CTs = filtered

        self._CTInfo = value
        if self._CTInfo is not None:
            if self not in self._CTInfo._CTs:
                self._CTInfo._CTs.append(self)

    CTInfo = property(getCTInfo, setCTInfo)
