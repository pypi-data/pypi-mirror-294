from cim_converter.CIM_EG.Core.Equipment import Equipment


class AuxiliaryEquipment(Equipment):

    def __init__(self, Terminal=None, *args, **kw_args):

        self._Terminal = None
        self.Terminal = Terminal

        super(AuxiliaryEquipment, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = ["Terminal"]
    _many_refs = []

    def getTerminal(self):
        return self._Terminal

    def setTerminal(self, value):
        if self._Terminal is not None:
            filtered = [
                x for x in self.Terminal.AuxiliaryEquipment if x != self
            ]
            self._Terminal._AuxiliaryEquipment = filtered

        self._Terminal = value
        if self._Terminal is not None:
            if self not in self._Terminal._AuxiliaryEquipment:
                self._Terminal._AuxiliaryEquipment.append(self)

    Terminal = property(getTerminal, setTerminal)
