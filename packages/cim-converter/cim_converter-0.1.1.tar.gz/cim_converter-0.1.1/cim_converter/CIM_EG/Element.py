class Element(object):

    def __init__(self, UUID=''):
        """Initialises a new 'Element' instance.

        @param UUID: 
        """

        self.UUID = UUID

    _attrs = ["UUID"]
    _attr_types = {"UUID": str}
    _defaults = {"UUID": ''}
    _enums = {}
    _refs = []
    _many_refs = []
