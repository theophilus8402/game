
from model.entity.classes.util import ClassName,BaseClass


paladin_babs = {
    1 : [1],
    2 : [2],
    3 : [3],
    4 : [4],
    5 : [5],
    6 : [6, 1],
    7 : [7, 2],
    8 : [8, 3],
    9 : [9, 4],
    10 : [10, 5],
    11 : [11, 6, 1],
    12 : [12, 7, 2],
    13 : [13, 8, 3],
    14 : [14, 9, 4],
    15 : [15, 10, 5],
    16 : [16, 11, 6, 1],
    17 : [17, 12, 7, 2],
    18 : [18, 13, 8, 3],
    19 : [19, 14, 9, 4],
    20 : [20, 15, 10, 5],
}

class Paladin(BaseClass):

    name = ClassName.paladin

    def __init__(self):
        super().__init__()
        self.bonuses = []
        self.proficiencies = set()
        self.level_up()

