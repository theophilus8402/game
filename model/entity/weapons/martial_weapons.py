
from model.entity.living.size import Size
from .base_weapon import WeaponType,DmgType,WeaponSpecial,Weapon,WeaponCategory


class ShortSword(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d4"
        elif size == Size.medium:
            dmg = "1d6"
        super(ShortSword, self).__init__(
            WeaponType.short_sword, WeaponCategory.light_melee,
            10, dmg, "19x2", 0, 2, [DmgType.slashing], specials)

