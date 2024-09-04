from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class TransformerEnd(IdentifiedObject):

    def __init__(self, rground=0, xground=0, *args, **kw_args):

        self.rground = rground

        self.xground = xground

        super(TransformerEnd, self).__init__(*args, **kw_args)

    _attrs = ["rground", "xground"]
    _attr_types = {"rground": float, "xground": float}
    _defaults = {"rground": 0, "xground": 0}
    _enums = {}
    _refs = []
    _many_refs = []
