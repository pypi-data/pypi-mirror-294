from cim_converter.CIM_EG.Core.IdentifiedObject import IdentifiedObject


class ACDCTerminal(IdentifiedObject):

    def __init__(self, *args, **kw_args):
        """Initialises a new 'ACDCTerminal' instance.

        """
        super(ACDCTerminal, self).__init__(*args, **kw_args)

    _attrs = []
    _attr_types = {}
    _defaults = {}
    _enums = {}
    _refs = []
    _many_refs = []
