from cim_converter.CIM_EG.AuxiliaryEquipment.AuxiliaryEquipment import AuxiliaryEquipment


class Sensor(AuxiliaryEquipment):

    def __init__(self, *args, **kw_args):

        super(Sensor, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = []
    _many_refs = []
