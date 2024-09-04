from cim_converter.CIM_EG.Wires.ProtectedSwitch import ProtectedSwitch


class Breaker(ProtectedSwitch):

    def __init__(self, inTransitTime=0.0, *args, **kw_args):

        self.inTransitTime = inTransitTime

        super(Breaker, self).__init__(*args, **kw_args)

    _attrs = ["inTransitTime"]
    _attr_types = {"inTransitTime": float}
    _defaults = {"inTransitTime": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []
