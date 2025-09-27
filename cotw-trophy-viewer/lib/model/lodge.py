from lib.model.lodge_type import LodgeType


class Lodge:
    def __init__(self, lodgeId: int, lodgeType: LodgeType, lodgeTypeId: int):
        self.lodgeId = lodgeId
        self.lodgeType = lodgeType
        self.lodgeTypeId = lodgeTypeId

    def lodgeName(self):
        return self.lodgeType.lodgeName() + " #" + str(self.lodgeTypeId)
