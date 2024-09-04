from cim_converter.CIM_EG.Wires.RegulatingControl import RegulatingControl


class TapChangerControl(RegulatingControl):

    def __init__(self,
                 targetDeadband=0.0,
                 targetValue=0.0,
                 lineDropR=0.0,
                 lineDropX=0.0,
                 reverseLineDropX=0.0,
                 reverseLineDropR=0.0,
                 lineDropCompensation=False,
                 limitVoltage=0.0,
                 TapChanger=None,
                 *args,
                 **kw_args):

        self.targetDeadband = targetDeadband

        self.targetValue = targetValue

        self.lineDropR = lineDropR

        self.lineDropX = lineDropX

        self.reverseLineDropX = reverseLineDropX

        self.reverseLineDropR = reverseLineDropR

        self.lineDropCompensation = lineDropCompensation

        self.limitVoltage = limitVoltage

        self._TapChanger = []
        self.TapChanger = [] if TapChanger is None else TapChanger

        super(TapChangerControl, self).__init__(*args, **kw_args)

    _attrs = [
        "lineDropR", "lineDropX", "reverseLineDropX", "reverseLineDropR",
        "lineDropCompensation", "limitVoltage", "targetDeadband", "targetValue"
    ]
    _attr_types = {
        "lineDropR": float,
        "lineDropX": float,
        "reverseLineDropX": float,
        "reverseLineDropR": float,
        "lineDropCompensation": bool,
        "limitVoltage": float,
        "targetDeadband": float,
        "targetValue": float
    }
    _defaults = {
        "lineDropR": 0.0,
        "lineDropX": 0.0,
        "reverseLineDropX": 0.0,
        "reverseLineDropR": 0.0,
        "lineDropCompensation": False,
        "limitVoltage": 0.0,
        "targetDeadband": 0.0,
        "targetValue": 0.0
    }
    _enums = {}
    _refs = ["TapChanger"]
    _many_refs = ["TapChanger"]

    def getTapChanger(self):
        """copy from reg conduting eq
        """
        return self._TapChanger

    def setTapChanger(self, value):
        for x in self._TapChanger:
            x.TapChangerControl = None
        for y in value:
            y._TapChangerControl = self
        self._TapChanger = value

    TapChanger = property(getTapChanger, setTapChanger)

    def addTapChanger(self, *TapChanger):
        for obj in TapChanger:
            obj.TapChangerControl = self

    def removeTapChanger(self, *TapChanger):
        for obj in TapChanger:
            obj.TapChangerControl = None
