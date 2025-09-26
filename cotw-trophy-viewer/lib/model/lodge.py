from lib.model.lodge_type import LodgeType


class Lodge:
    def __init__(self, lodgeId: int, lodgeType: LodgeType):
        self.lodgeId = lodgeId
        self.lodgeType = lodgeType
