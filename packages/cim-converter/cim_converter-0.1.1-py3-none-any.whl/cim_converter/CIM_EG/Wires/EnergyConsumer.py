from cim_converter.CIM_EG.Core.ConductingEquipment import ConductingEquipment


class EnergyConsumer(ConductingEquipment):

    def __init__(self,
                 qfixedPct=0.0,
                 customerCount=0,
                 pfixedPct=0.0,
                 pfixed=0.0,
                 qfixed=0.0,
                 ServiceDeliveryPoints=None,
                 LoadResponse=None,
                 PowerCutZone=None,
                 EnergyConsumerPhases=None,
                 *args,
                 **kw_args):

        self.qfixedPct = qfixedPct

        self.customerCount = customerCount

        self.pfixedPct = pfixedPct

        self.pfixed = pfixed

        self.qfixed = qfixed

        self._ServiceDeliveryPoints = []
        self.ServiceDeliveryPoints = [] if ServiceDeliveryPoints is None else ServiceDeliveryPoints

        self._LoadResponse = None
        self.LoadResponse = LoadResponse

        self._PowerCutZone = None
        self.PowerCutZone = PowerCutZone

        self._EnergyConsumerPhases = []
        self.EnergyConsumerPhases = [] if EnergyConsumerPhases is None else EnergyConsumerPhases

        super(EnergyConsumer, self).__init__(*args, **kw_args)

    _attrs = ["qfixedPct", "customerCount", "pfixedPct", "pfixed", "qfixed"]
    _attr_types = {
        "qfixedPct": float,
        "customerCount": int,
        "pfixedPct": float,
        "pfixed": float,
        "qfixed": float
    }
    _defaults = {
        "qfixedPct": 0.0,
        "customerCount": 0,
        "pfixedPct": 0.0,
        "pfixed": 0.0,
        "qfixed": 0.0
    }
    _enums = {}
    _refs = [
        "ServiceDeliveryPoints", "LoadResponse", "PowerCutZone",
        "EnergyConsumerPhases"
    ]
    _many_refs = ["ServiceDeliveryPoints", "EnergyConsumerPhases"]

    def getServiceDeliveryPoints(self):

        return self._ServiceDeliveryPoints

    def setServiceDeliveryPoints(self, value):
        for x in self._ServiceDeliveryPoints:
            x.EnergyConsumer = None
        for y in value:
            y._EnergyConsumer = self
        self._ServiceDeliveryPoints = value

    ServiceDeliveryPoints = property(getServiceDeliveryPoints,
                                     setServiceDeliveryPoints)

    def addServiceDeliveryPoints(self, *ServiceDeliveryPoints):
        for obj in ServiceDeliveryPoints:
            obj.EnergyConsumer = self

    def removeServiceDeliveryPoints(self, *ServiceDeliveryPoints):
        for obj in ServiceDeliveryPoints:
            obj.EnergyConsumer = None

    def getLoadResponse(self):
        """The load response characteristic of this load.
        """
        return self._LoadResponse

    def setLoadResponse(self, value):
        if self._LoadResponse is not None:
            filtered = [
                x for x in self.LoadResponse.EnergyConsumer if x != self
            ]
            self._LoadResponse._EnergyConsumer = filtered

        self._LoadResponse = value
        if self._LoadResponse is not None:
            if self not in self._LoadResponse._EnergyConsumer:
                self._LoadResponse._EnergyConsumer.append(self)

    LoadResponse = property(getLoadResponse, setLoadResponse)

    def getPowerCutZone(self):
        """An energy consumer is assigned to a power cut zone
        """
        return self._PowerCutZone

    def setPowerCutZone(self, value):
        if self._PowerCutZone is not None:
            filtered = [
                x for x in self.PowerCutZone.EnergyConsumers if x != self
            ]
            self._PowerCutZone._EnergyConsumers = filtered

        self._PowerCutZone = value
        if self._PowerCutZone is not None:
            if self not in self._PowerCutZone._EnergyConsumers:
                self._PowerCutZone._EnergyConsumers.append(self)

    PowerCutZone = property(getPowerCutZone, setPowerCutZone)

    def getEnergyConsumerPhases(self):

        return self._EnergyConsumerPhases

    def setEnergyConsumerPhases(self, value):
        for x in self._EnergyConsumerPhases:
            x.EnergyConsumer = None
        for y in value:
            y._EnergyConsumer = self
        self._EnergyConsumerPhases = value

    EnergyConsumerPhases = property(getEnergyConsumerPhases,
                                    setEnergyConsumerPhases)

    def addEnergyConsumerPhases(self, *EnergyConsumerPhases):
        for obj in EnergyConsumerPhases:
            obj.EnergyConsumer = self

    def removeEnergyConsumerPhases(self, *EnergyConsumerPhases):
        for obj in EnergyConsumerPhases:
            obj.EnergyConsumer = None
