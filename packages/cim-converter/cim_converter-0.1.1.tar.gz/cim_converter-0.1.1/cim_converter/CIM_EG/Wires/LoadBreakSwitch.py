from cim_converter.CIM_EG.Wires.ProtectedSwitch import ProtectedSwitch


class LoadBreakSwitch(ProtectedSwitch):

    def __init__(self, *args, **kw_args):

        super(LoadBreakSwitch, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = []
    _many_refs = []
