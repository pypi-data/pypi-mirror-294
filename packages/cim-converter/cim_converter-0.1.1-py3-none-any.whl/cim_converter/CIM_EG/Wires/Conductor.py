from cim_converter.CIM_EG.Core.ConductingEquipment import ConductingEquipment


class Conductor(ConductingEquipment):

    def __init__(self, length=0.0, *args, **kw_args):

        self.length = length

        super(Conductor, self).__init__(*args, **kw_args)

    _attrs = ["length"]
    _attr_types = {"length": float}
    _defaults = {"length": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []
