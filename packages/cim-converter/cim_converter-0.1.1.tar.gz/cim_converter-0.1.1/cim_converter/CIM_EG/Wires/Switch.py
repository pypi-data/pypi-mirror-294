from cim_converter.CIM_EG.Core.ConductingEquipment import ConductingEquipment


class Switch(ConductingEquipment):

    def __init__(self,
                 ratedCurrent=0.0,
                 open=False,
                 normalOpen=False,
                 retained=False,
                 *args,
                 **kw_args):

        self.ratedCurrent = ratedCurrent
        self.open = open
        self.normalOpen = normalOpen
        self.retained = retained

        super(Switch, self).__init__(*args, **kw_args)

    _attrs = ["ratedCurrent", "open", "normalOpen", "retained"]
    _attr_types = {
        "ratedCurrent": float,
        "open": bool,
        "normalOpen": bool,
        "retained": bool
    }
    _defaults = {
        "ratedCurrent": 0.0,
        "open": False,
        "normalOpen": False,
        "retained": False
    }
    _enums = {}
    _refs = []
    _many_refs = []
