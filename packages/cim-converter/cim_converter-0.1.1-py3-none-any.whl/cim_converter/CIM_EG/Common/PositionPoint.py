from cim_converter.CIM_EG.Core.Equipment import Equipment


class PositionPoint(Equipment):

    def __init__(self,
                 xPosition=0.0,
                 yPosition=0.0,
                 sequenceNumber=0,
                 Location=None,
                 *args,
                 **kw_args):

        self.xPosition = xPosition
        self.yPosition = yPosition
        self.sequenceNumber = sequenceNumber

        self._Location = None
        self.Location = Location

        super(PositionPoint, self).__init__(*args, **kw_args)

    _attrs = ["xPosition", "yPosition", "sequenceNumber"]
    _attr_types = {
        "xPosition": float,
        "yPosition": float,
        "sequenceNumber": int
    }
    _defaults = {"xPosition": 0.0, "yPosition": 0.0, "sequenceNumber": 0}
    _enums = {}
    _refs = ["Location"]
    _many_refs = []

    def getLocation(self):
        return self._Location

    def setLocation(self, value):
        if self._Location is not None:
            filtered = [x for x in self.Location.PositionPoints if x != self]
            self._Location._PositionPoints = filtered

        self._Location = value
        if self._Location is not None:
            if self not in self._Location._PositionPoints:
                self._Location._PositionPoints.append(self)

    Location = property(getLocation, setLocation)
