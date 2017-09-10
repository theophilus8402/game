
from model.entity.living.size import Size
from .base_weapon import WeaponType,DmgType,WeaponSpecial,Weapon,WeaponCategory


class Gauntlet(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            super(Gauntlet, self).__init__(
                WeaponType.gauntlet, WeaponCategory.light_melee,
                2, "1d2", "20x2", 0, 1, [DmgType.bludgeoning], specials)
        elif size == Size.medium:
            super(Gauntlet, self).__init__(
                WeaponType.gauntlet, WeaponCategory.light_melee,
                2, "1d3", "20x2", 0, 1, [DmgType.bludgeoning], specials)


class UnarmedStrike(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        specials.append(WeaponSpecial.nonlethal)
        if size == Size.small:
            super(UnarmedStrike, self).__init__(
                WeaponType.unarmed_strike, WeaponCategory.light_melee,
                0, "1d2", "20x2", 0, 0, [DmgType.bludgeoning], specials)
        elif size == Size.medium:
            super(UnarmedStrike, self).__init__(
                WeaponType.unarmed_strike, WeaponCategory.light_melee,
                0, "1d3", "20x2", 0, 0, [DmgType.bludgeoning], specials)




