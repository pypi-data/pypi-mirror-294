from cim_converter.CIM_EG.Core.ACDCTerminal import ACDCTerminal


class Terminal(ACDCTerminal):

    def __init__(self,
                 phases='s12N',
                 ConductingEquipment=None,
                 AuxiliaryEquipment=None,
                 ConnectivityNode=None,
                 Circuit=None,
                 TransformerEnd=None,
                 NormalHeadFeeder=None,
                 *args,
                 **kw_args):

        self.phases = phases

        self._ConductingEquipment = None
        self.ConductingEquipment = ConductingEquipment

        self._AuxiliaryEquipment = []
        self.AuxiliaryEquipment = [] if AuxiliaryEquipment is None else AuxiliaryEquipment

        self._ConnectivityNode = None
        self.ConnectivityNode = ConnectivityNode

        self._Circuit = None
        self.Circuit = Circuit

        self._TransformerEnd = []
        self.TransformerEnd = [] if TransformerEnd is None else TransformerEnd

        self._NormalHeadFeeder = None
        self.NormalHeadFeeder = NormalHeadFeeder

        super(Terminal, self).__init__(*args, **kw_args)

    _attrs = ["phases"]
    _attr_types = {"phases": str}
    _defaults = {"phases": 's12N'}
    _enums = {"phases": "PhaseCode"}
    _refs = [
        "ConductingEquipment", "AuxiliaryEquipment", "ConnectivityNode",
        "Circuit", "TransformerEnd", "NormalHeadFeeder"
    ]
    _many_refs = ["AuxiliaryEquipment", "TransformerEnd"]

    def getConductingEquipment(self):
        return self._ConductingEquipment

    def setConductingEquipment(self, value):
        if self._ConductingEquipment is not None:
            filtered = [
                x for x in self.ConductingEquipment.Terminals if x != self
            ]
            self._ConductingEquipment._Terminals = filtered
        if value is not None:
            value.Terminals.append(self)
        self._ConductingEquipment = value

    ConductingEquipment = property(getConductingEquipment,
                                   setConductingEquipment)

    def getAuxiliaryEquipment(self):
        return self._AuxiliaryEquipment

    def setAuxiliaryEquipment(self, value):
        for x in self._AuxiliaryEquipment:
            x.Terminal = None
        for y in value:
            y._Terminal = self
        self._AuxiliaryEquipment = value

    AuxiliaryEquipment = property(getAuxiliaryEquipment, setAuxiliaryEquipment)

    def addAuxiliaryEquipment(self, *AuxiliaryEquipment):
        for obj in AuxiliaryEquipment:
            self.AuxiliaryEquipment.append(obj)

    def removeAuxiliaryEquipment(self, *AuxiliaryEquipment):
        for obj in AuxiliaryEquipment:
            obj.Terminal = None

    def getConnectivityNode(self):
        return self._ConnectivityNode

    def setConnectivityNode(self, value):
        if self._ConnectivityNode is not None:
            self._ConnectivityNode._Terminal = None
        if value is not None:
            value.Terminal = self
        self._ConnectivityNode = value

    ConnectivityNode = property(getConnectivityNode, setConnectivityNode)

    def getCircuit(self):
        return self._Circuit

    def setCircuit(self, value):
        if self._Circuit is not None:
            self._Circuit._Terminal = None
        if value is not None:
            value.Terminal = self
        self._Circuit = value

    Circuit = property(getCircuit, setCircuit)

    def getTransformerEnd(self):
        return self._TransformerEnd

    def setTransformerEnd(self, value):

        for x in self._TransformerEnd:
            x.Terminal = None
        for y in value:
            y._Terminal = self
        self._TransformerEnd = value

    TransformerEnd = property(getTransformerEnd, setTransformerEnd)

    def addTransformerEnd(self, *TransformerEnd):
        for obj in TransformerEnd:
            obj.Terminal = self

    def removeTransformerEnd(self, *TransformerEnd):
        for obj in TransformerEnd:
            obj.Terminal = None

    def getNormalHeadFeeder(self):
        return self._NormalHeadFeeder

    def setNormalHeadFeeder(self, value):
        if self._NormalHeadFeeder is not None:
            self._NormalHeadFeeder._Terminal = None
        if value is not None:
            value.Terminal = self
        self._NormalHeadFeeder = value

    NormalHeadFeeder = property(getNormalHeadFeeder, setNormalHeadFeeder)
