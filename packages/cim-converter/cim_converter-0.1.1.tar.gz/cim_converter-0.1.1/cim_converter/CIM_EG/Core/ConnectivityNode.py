from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class ConnectivityNode(IdentifiedObject):

    def __init__(self,
                 TopologicalNode=None,
                 ConnectivityNodeContainer=None,
                 Terminals=None,
                 *args,
                 **kw_args):
        """Initialises a new 'ConnectivityNode' instance.

        @param TopologicalNode: Several ConnectivityNode(s) may combine together to form a single TopologicalNode, depending on the current state of the network.
        @param ConnectivityNodeContainer: Container of this connectivity node.
        @param Terminals: Terminals interconnect with zero impedance at a node.  Measurements on a node apply to all of its terminals.
        """
        self._TopologicalNode = None
        self.TopologicalNode = TopologicalNode

        self._ConnectivityNodeContainer = None
        self.ConnectivityNodeContainer = ConnectivityNodeContainer

        self._Terminals = []
        self.Terminals = [] if Terminals is None else Terminals

        super(ConnectivityNode, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["TopologicalNode", "ConnectivityNodeContainer", "Terminals"]
    _many_refs = ["Terminals"]

    def getTopologicalNode(self):
        """Several ConnectivityNode(s) may combine together to form a single TopologicalNode, depending on the current state of the network.
        """
        return self._TopologicalNode

    def setTopologicalNode(self, value):
        if self._TopologicalNode is not None:
            filtered = [
                x for x in self.TopologicalNode.ConnectivityNodes if x != self
            ]
            self._TopologicalNode._ConnectivityNodes = filtered

        self._TopologicalNode = value
        if self._TopologicalNode is not None:
            if self not in self._TopologicalNode._ConnectivityNodes:
                self._TopologicalNode._ConnectivityNodes.append(self)

    TopologicalNode = property(getTopologicalNode, setTopologicalNode)

    def getConnectivityNodeContainer(self):
        """Container of this connectivity node.
        """
        return self._ConnectivityNodeContainer

    def setConnectivityNodeContainer(self, value):
        if self._ConnectivityNodeContainer is not None:
            filtered = [
                x for x in self.ConnectivityNodeContainer.ConnectivityNodes
                if x != self
            ]
            self._ConnectivityNodeContainer._ConnectivityNodes = filtered

        self._ConnectivityNodeContainer = value
        if self._ConnectivityNodeContainer is not None:
            if self not in self._ConnectivityNodeContainer._ConnectivityNodes:
                self._ConnectivityNodeContainer._ConnectivityNodes.append(self)

    ConnectivityNodeContainer = property(getConnectivityNodeContainer,
                                         setConnectivityNodeContainer)

    def getTerminals(self):
        """Terminals interconnect with zero impedance at a node.  Measurements on a node apply to all of its terminals.
        """
        return self._Terminals

    def setTerminals(self, value):
        for x in self._Terminals:
            x.ConductingEquipment = None
        for y in value:
            y._ConductingEquipment = self
        self._Terminals = value

    Terminals = property(getTerminals, setTerminals)

    def addTerminals(self, *Terminals):
        for obj in Terminals:
            self.Terminals.append(obj)

    def removeTerminals(self, *Terminals):
        for obj in Terminals:
            obj.ConductingEquipment = None
