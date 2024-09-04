from cim_converter.CIM_EG.Wires.Switch import Switch


class Fuse(Switch):

    def __init__(self, *args, **kw_args):

        super(Fuse, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = []
    _many_refs = []
