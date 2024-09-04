from cim_converter.CIM_EG.AuxiliaryEquipment.Sensor import Sensor


class PotentialTransformer(Sensor):

    def __init__(self,
                 AliasName='',
                 nominalRatio=0.0,
                 accuracyClass='',
                 ptClass='',
                 PTInfo=None,
                 *args,
                 **kw_args):

        self.AliasName = AliasName

        self.nominalRatio = nominalRatio

        self.accuracyClass = accuracyClass

        self.ptClass = ptClass

        self._PTInfo = None
        self.PTInfo = PTInfo

        super(PotentialTransformer, self).__init__(*args, **kw_args)

    _attrs = ["nominalRatio", "accuracyClass", "ptClass", "AliasName"]
    _attr_types = {
        "nominalRatio": float,
        "accuracyClass": str,
        "ptClass": str,
        "AliasName": str
    }
    _defaults = {
        "nominalRatio": 0.0,
        "accuracyClass": '',
        "ptClass": '',
        "AliasName": ''
    }
    _enums = {}
    _refs = ["PTInfo"]
    _many_refs = []

    def getPTInfo(self):
        """Potential (voltage) transformer data.
        """
        return self._PTInfo

    def setPTInfo(self, value):
        if self._PTInfo is not None:
            filtered = [x for x in self.PTInfo.PTs if x != self]
            self._PTInfo._PTs = filtered

        self._PTInfo = value
        if self._PTInfo is not None:
            if self not in self._PTInfo._PTs:
                self._PTInfo._PTs.append(self)

    PTInfo = property(getPTInfo, setPTInfo)
