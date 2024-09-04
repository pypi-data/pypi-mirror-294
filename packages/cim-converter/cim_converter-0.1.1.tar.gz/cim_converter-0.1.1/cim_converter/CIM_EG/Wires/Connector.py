from cim_converter.CIM_EG.Core.ConductingEquipment import ConductingEquipment


class Connector(ConductingEquipment):

    def __init__(self, *args, **kw_args):

        super(Connector, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = []
    _many_refs = []
