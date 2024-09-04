from cim_converter.CIM_EG.Wires.Connector import Connector


class BusbarSection(Connector):

    def __init__(self, VoltageControlZone=None, *args, **kw_args):

        self._VoltageControlZone = None
        self.VoltageControlZone = VoltageControlZone

        super(BusbarSection, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["VoltageControlZone"]
    _many_refs = []

    def getVoltageControlZone(self):
        """A VoltageControlZone is controlled by a designated BusbarSection.
        """
        return self._VoltageControlZone

    def setVoltageControlZone(self, value):
        if self._VoltageControlZone is not None:
            self._VoltageControlZone._BusbarSection = None

        self._VoltageControlZone = value
        if self._VoltageControlZone is not None:
            self._VoltageControlZone.BusbarSection = None
            self._VoltageControlZone._BusbarSection = self

    VoltageControlZone = property(getVoltageControlZone, setVoltageControlZone)
