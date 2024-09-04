from cim_converter.CIM_EG.Assets.AssetInfo import AssetInfo


class TransformerEndInfo(AssetInfo):

    def __init__(self,
                 r=0.0,
                 insulationU=0.0,
                 emergencyS=0.0,
                 shortTermS=0.0,
                 connectionKind="Z",
                 endNumber=0,
                 ratedS=0.0,
                 ratedU=0.0,
                 phaseAngleClock=0,
                 FromMeshImpedance=None,
                 EnergisedEndNoLoadTests=None,
                 OpenEndOpenCircuitTests=None,
                 ToMeshImpedance=None,
                 TransformerEnd=None,
                 TransformerTankInfo=None,
                 EnergisedEndOpenCircuitTests=None,
                 GroundedEndShortCircuitTests=None,
                 EnergisedEndShortCircuitTests=None,
                 CoreAdmittance=None,
                 *args,
                 **kw_args):

        self.r = r

        self.insulationU = insulationU

        self.emergencyS = emergencyS

        self.shortTermS = shortTermS

        self.connectionKind = connectionKind

        self.endNumber = endNumber

        self.ratedS = ratedS

        self.ratedU = ratedU

        self.phaseAngleClock = phaseAngleClock

        self._FromMeshImpedance = []
        self.FromMeshImpedance = [] if FromMeshImpedance is None else FromMeshImpedance

        self._EnergisedEndNoLoadTests = []
        self.EnergisedEndNoLoadTests = [] if EnergisedEndNoLoadTests is None else EnergisedEndNoLoadTests

        self._OpenEndOpenCircuitTests = []
        self.OpenEndOpenCircuitTests = [] if OpenEndOpenCircuitTests is None else OpenEndOpenCircuitTests

        self._ToMeshImpedance = []
        self.ToMeshImpedance = [] if ToMeshImpedance is None else ToMeshImpedance

        self._TransformerEnd = []
        self.TransformerEnd = [] if TransformerEnd is None else TransformerEnd

        self._TransformerTankInfo = None
        self.TransformerTankInfo = TransformerTankInfo

        self._EnergisedEndOpenCircuitTests = []
        self.EnergisedEndOpenCircuitTests = [] if EnergisedEndOpenCircuitTests is None else EnergisedEndOpenCircuitTests

        self._GroundedEndShortCircuitTests = []
        self.GroundedEndShortCircuitTests = [] if GroundedEndShortCircuitTests is None else GroundedEndShortCircuitTests

        self._EnergisedEndShortCircuitTests = []
        self.EnergisedEndShortCircuitTests = [] if EnergisedEndShortCircuitTests is None else EnergisedEndShortCircuitTests

        self._CoreAdmittance = None
        self.CoreAdmittance = CoreAdmittance

        super(TransformerEndInfo, self).__init__(*args, **kw_args)

    _attrs = [
        "r", "insulationU", "emergencyS", "shortTermS", "connectionKind",
        "endNumber", "ratedS", "ratedU", "phaseAngleClock"
    ]
    _attr_types = {
        "r": float,
        "insulationU": float,
        "emergencyS": float,
        "shortTermS": float,
        "connectionKind": str,
        "endNumber": int,
        "ratedS": float,
        "ratedU": float,
        "phaseAngleClock": int
    }
    _defaults = {
        "r": 0.0,
        "insulationU": 0.0,
        "emergencyS": 0.0,
        "shortTermS": 0.0,
        "connectionKind": "Z",
        "endNumber": 0,
        "ratedS": 0.0,
        "ratedU": 0.0,
        "phaseAngleClock": 0
    }
    _enums = {"connectionKind": "WindingConnection"}
    _refs = [
        "FromMeshImpedance", "EnergisedEndNoLoadTests",
        "OpenEndOpenCircuitTests", "ToMeshImpedance", "TransformerEnd",
        "TransformerTankInfo", "EnergisedEndOpenCircuitTests",
        "GroundedEndShortCircuitTests", "EnergisedEndShortCircuitTests",
        "CoreAdmittance"
    ]
    _many_refs = [
        "FromMeshImpedance", "EnergisedEndNoLoadTests",
        "OpenEndOpenCircuitTests", "ToMeshImpedance", "TransformerEnd",
        "EnergisedEndOpenCircuitTests", "GroundedEndShortCircuitTests",
        "EnergisedEndShortCircuitTests"
    ]

    def getFromMeshImpedance(self):
        """All mesh impedances between this 'to' and other 'from' transformer ends.
        """
        return self._FromMeshImpedance

    def setFromMeshImpedance(self, value):
        for x in self._FromMeshImpedance:
            x.FromTransformerEndInfo = None
        for y in value:
            y._FromTransformerEndInfo = self
        self._FromMeshImpedance = value

    FromMeshImpedance = property(getFromMeshImpedance, setFromMeshImpedance)

    def addFromMeshImpedance(self, *FromMeshImpedance):
        for obj in FromMeshImpedance:
            obj.FromTransformerEndInfo = self

    def removeFromMeshImpedance(self, *FromMeshImpedance):
        for obj in FromMeshImpedance:
            obj.FromTransformerEndInfo = None

    def getEnergisedEndNoLoadTests(self):
        """All no-load test measurements in which this transformer end was energised.
        """
        return self._EnergisedEndNoLoadTests

    def setEnergisedEndNoLoadTests(self, value):
        for x in self._EnergisedEndNoLoadTests:
            x.EnergisedEnd = None
        for y in value:
            y._EnergisedEnd = self
        self._EnergisedEndNoLoadTests = value

    EnergisedEndNoLoadTests = property(getEnergisedEndNoLoadTests,
                                       setEnergisedEndNoLoadTests)

    def addEnergisedEndNoLoadTests(self, *EnergisedEndNoLoadTests):
        for obj in EnergisedEndNoLoadTests:
            obj.EnergisedEnd = self

    def removeEnergisedEndNoLoadTests(self, *EnergisedEndNoLoadTests):
        for obj in EnergisedEndNoLoadTests:
            obj.EnergisedEnd = None

    def getOpenEndOpenCircuitTests(self):
        """All open-circuit test measurements in which this transformer end was not excited.
        """
        return self._OpenEndOpenCircuitTests

    def setOpenEndOpenCircuitTests(self, value):
        for x in self._OpenEndOpenCircuitTests:
            x.OpenEnd = None
        for y in value:
            y._OpenEnd = self
        self._OpenEndOpenCircuitTests = value

    OpenEndOpenCircuitTests = property(getOpenEndOpenCircuitTests,
                                       setOpenEndOpenCircuitTests)

    def addOpenEndOpenCircuitTests(self, *OpenEndOpenCircuitTests):
        for obj in OpenEndOpenCircuitTests:
            obj.OpenEnd = self

    def removeOpenEndOpenCircuitTests(self, *OpenEndOpenCircuitTests):
        for obj in OpenEndOpenCircuitTests:
            obj.OpenEnd = None

    def getToMeshImpedance(self):
        """All mesh impedances between this 'from' and other 'to' transformer ends.
        """
        return self._ToMeshImpedance

    def setToMeshImpedance(self, value):
        for p in self._ToMeshImpedance:
            filtered = [q for q in p.ToTransformerEndInfo if q != self]
            self._ToMeshImpedance._ToTransformerEndInfo = filtered
        for r in value:
            if self not in r._ToTransformerEndInfo:
                r._ToTransformerEndInfo.append(self)
        self._ToMeshImpedance = value

    ToMeshImpedance = property(getToMeshImpedance, setToMeshImpedance)

    def addToMeshImpedance(self, *ToMeshImpedance):
        for obj in ToMeshImpedance:
            if self not in obj._ToTransformerEndInfo:
                obj._ToTransformerEndInfo.append(self)
            self._ToMeshImpedance.append(obj)

    def removeToMeshImpedance(self, *ToMeshImpedance):
        for obj in ToMeshImpedance:
            if self in obj._ToTransformerEndInfo:
                obj._ToTransformerEndInfo.remove(self)
            self._ToMeshImpedance.remove(obj)

    def getTransformerEnd(self):
        """All transformer ends described by this end data.
        """
        return self._TransformerEnd

    def setTransformerEnd(self, value):
        for x in self._TransformerEnd:
            x.TransformerEndInfo = None
        for y in value:
            y._TransformerEndInfo = self
        self._TransformerEnd = value

    TransformerEnd = property(getTransformerEnd, setTransformerEnd)

    def addTransformerEnd(self, *TransformerEnd):
        for obj in TransformerEnd:
            obj.TransformerEndInfo = self

    def removeTransformerEnd(self, *TransformerEnd):
        for obj in TransformerEnd:
            obj.TransformerEndInfo = None

    def getTransformerTankInfo(self):
        """Transformer tank data that this end description is part of.
        """
        return self._TransformerTankInfo

    def setTransformerTankInfo(self, value):
        if self._TransformerTankInfo is not None:
            filtered = [
                x for x in self.TransformerTankInfo.TransformerEndInfos
                if x != self
            ]
            self._TransformerTankInfo._TransformerEndInfos = filtered

        self._TransformerTankInfo = value
        if self._TransformerTankInfo is not None:
            if self not in self._TransformerTankInfo._TransformerEndInfos:
                self._TransformerTankInfo._TransformerEndInfos.append(self)

    TransformerTankInfo = property(getTransformerTankInfo,
                                   setTransformerTankInfo)

    def getEnergisedEndOpenCircuitTests(self):
        """All open-circuit test measurements in which this transformer end was excited.
        """
        return self._EnergisedEndOpenCircuitTests

    def setEnergisedEndOpenCircuitTests(self, value):
        for x in self._EnergisedEndOpenCircuitTests:
            x.EnergisedEnd = None
        for y in value:
            y._EnergisedEnd = self
        self._EnergisedEndOpenCircuitTests = value

    EnergisedEndOpenCircuitTests = property(getEnergisedEndOpenCircuitTests,
                                            setEnergisedEndOpenCircuitTests)

    def addEnergisedEndOpenCircuitTests(self, *EnergisedEndOpenCircuitTests):
        for obj in EnergisedEndOpenCircuitTests:
            obj.EnergisedEnd = self

    def removeEnergisedEndOpenCircuitTests(self,
                                           *EnergisedEndOpenCircuitTests):
        for obj in EnergisedEndOpenCircuitTests:
            obj.EnergisedEnd = None

    def getGroundedEndShortCircuitTests(self):
        """All short-circuit test measurements in which this transformer end was short-circuited.
        """
        return self._GroundedEndShortCircuitTests

    def setGroundedEndShortCircuitTests(self, value):
        for p in self._GroundedEndShortCircuitTests:
            filtered = [q for q in p.GroundedEnds if q != self]
            self._GroundedEndShortCircuitTests._GroundedEnds = filtered
        for r in value:
            if self not in r._GroundedEnds:
                r._GroundedEnds.append(self)
        self._GroundedEndShortCircuitTests = value

    GroundedEndShortCircuitTests = property(getGroundedEndShortCircuitTests,
                                            setGroundedEndShortCircuitTests)

    def addGroundedEndShortCircuitTests(self, *GroundedEndShortCircuitTests):
        for obj in GroundedEndShortCircuitTests:
            if self not in obj._GroundedEnds:
                obj._GroundedEnds.append(self)
            self._GroundedEndShortCircuitTests.append(obj)

    def removeGroundedEndShortCircuitTests(self,
                                           *GroundedEndShortCircuitTests):
        for obj in GroundedEndShortCircuitTests:
            if self in obj._GroundedEnds:
                obj._GroundedEnds.remove(self)
            self._GroundedEndShortCircuitTests.remove(obj)

    def getEnergisedEndShortCircuitTests(self):
        """All short-circuit test measurements in which this transformer end was energised.
        """
        return self._EnergisedEndShortCircuitTests

    def setEnergisedEndShortCircuitTests(self, value):
        for x in self._EnergisedEndShortCircuitTests:
            x.EnergisedEnd = None
        for y in value:
            y._EnergisedEnd = self
        self._EnergisedEndShortCircuitTests = value

    EnergisedEndShortCircuitTests = property(getEnergisedEndShortCircuitTests,
                                             setEnergisedEndShortCircuitTests)

    def addEnergisedEndShortCircuitTests(self, *EnergisedEndShortCircuitTests):
        for obj in EnergisedEndShortCircuitTests:
            obj.EnergisedEnd = self

    def removeEnergisedEndShortCircuitTests(self,
                                            *EnergisedEndShortCircuitTests):
        for obj in EnergisedEndShortCircuitTests:
            obj.EnergisedEnd = None

    def getCoreAdmittance(self):
        """Core admittance of this transformer end info, representing magnetising current and core losses. The full values of the transformer should be supplied for one transformer end info only.
        """
        return self._CoreAdmittance

    def setCoreAdmittance(self, value):
        if self._CoreAdmittance is not None:
            self._CoreAdmittance._TransformerEndInfo = None

        self._CoreAdmittance = value
        if self._CoreAdmittance is not None:
            self._CoreAdmittance.TransformerEndInfo = None
            self._CoreAdmittance._TransformerEndInfo = self

    CoreAdmittance = property(getCoreAdmittance, setCoreAdmittance)
