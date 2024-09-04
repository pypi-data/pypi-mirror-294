from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class TransformerTest(IdentifiedObject):

    def __init__(self, basePower=0.0, temperature=0.0, *args, **kw_args):
        self.basePower = basePower

        self.temperature = temperature

        super(TransformerTest, self).__init__(*args, **kw_args)

    _attrs = ["basePower", "temperature"]
    _attr_types = {"basePower": float, "temperature": float}
    _defaults = {"basePower": 0.0, "temperature": 0.0}
    _enums = {}
    _refs = []
    _many_refs = []
