from cim_converter.CIM_EG.Core.PowerSystemResource import PowerSystemResource


class ConnectivityNodeContainer(PowerSystemResource):
    """A base class for all objects that may contain ConnectivityNodes or TopologicalNodes.A base class for all objects that may contain ConnectivityNodes or TopologicalNodes.
    """

    def __init__(self,
                 TopologicalNode=None,
                 ConnectivityNodes=None,
                 *args,
                 **kw_args):
        """Initialises a new 'ConnectivityNodeContainer' instance.

        @param TopologicalNode: The topological nodes which belong to this connectivity node container.
        @param ConnectivityNodes: Connectivity nodes contained by this container.
        """
        self._TopologicalNode = []
        self.TopologicalNode = [] if TopologicalNode is None else TopologicalNode

        self._ConnectivityNodes = []
        self.ConnectivityNodes = [] if ConnectivityNodes is None else ConnectivityNodes

        super(ConnectivityNodeContainer, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["TopologicalNode", "ConnectivityNodes"]
    _many_refs = ["TopologicalNode", "ConnectivityNodes"]

    def getTopologicalNode(self):
        """The topological nodes which belong to this connectivity node container.
        """
        return self._TopologicalNode

    def setTopologicalNode(self, value):
        for x in self._TopologicalNode:
            x.ConnectivityNodeContainer = None
        for y in value:
            y._ConnectivityNodeContainer = self
        self._TopologicalNode = value

    TopologicalNode = property(getTopologicalNode, setTopologicalNode)

    def addTopologicalNode(self, *TopologicalNode):
        for obj in TopologicalNode:
            obj.ConnectivityNodeContainer = self

    def removeTopologicalNode(self, *TopologicalNode):
        for obj in TopologicalNode:
            obj.ConnectivityNodeContainer = None

    def getConnectivityNodes(self):
        """Connectivity nodes contained by this container.
        """
        return self._ConnectivityNodes

    def setConnectivityNodes(self, value):
        for x in self._ConnectivityNodes:
            x.ConnectivityNodeContainer = None
        for y in value:
            y._ConnectivityNodeContainer = self
        self._ConnectivityNodes = value

    ConnectivityNodes = property(getConnectivityNodes, setConnectivityNodes)

    def addConnectivityNodes(self, *ConnectivityNodes):
        for obj in ConnectivityNodes:
            obj.ConnectivityNodeContainer = self

    def removeConnectivityNodes(self, *ConnectivityNodes):
        for obj in ConnectivityNodes:
            obj.ConnectivityNodeContainer = None
