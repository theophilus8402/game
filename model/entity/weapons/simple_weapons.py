
from model.entity.living.size import Size
from .base_weapon import WeaponType,DmgType,WeaponSpecial,Weapon,WeaponCategory


class Gauntlet(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d2"
        elif size == Size.medium:
            dmg = "1d3"
        super(Gauntlet, self).__init__(
            WeaponType.gauntlet, WeaponCategory.light_melee,
            2, dmg, "20x2", 0, 1, [DmgType.bludgeoning], specials)


class UnarmedStrike(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        specials.append(WeaponSpecial.nonlethal)
        if size == Size.small:
            dmg = "1d2"
        elif size == Size.medium:
            dmg = "1d3"
        super(UnarmedStrike, self).__init__(
            WeaponType.unarmed_strike, WeaponCategory.light_melee,
            0, dmg, "20x2", 0, 0, [DmgType.bludgeoning], specials)


class Dagger(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d3"
        elif size == Size.medium:
            dmg = "1d4"
        super(Dagger, self).__init__(
            WeaponType.dagger, WeaponCategory.light_melee,
            2, dmg, "19x2", 10, 1, [DmgType.piercing, DmgType.slashing], specials)


class PunchingDagger(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d3"
        elif size == Size.medium:
            dmg = "1d4"
        super(PunchingDagger, self).__init__(
            WeaponType.punching_dagger, WeaponCategory.light_melee,
            2, dmg, "20x3", 0, 1, [DmgType.piercing], specials)


class SpikedGauntlet(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d3"
        elif size == Size.medium:
            dmg = "1d4"
        super(SpikedGauntlet, self).__init__(
            WeaponType.spiked_gauntlet, WeaponCategory.light_melee,
            5, dmg, "20x2", 0, 1, [DmgType.piercing], specials)


class LightMace(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d4"
        elif size == Size.medium:
            dmg = "1d6"
        super(LightMace, self).__init__(
            WeaponType.light_mace, WeaponCategory.light_melee,
            5, dmg, "20x2", 0, 4, [DmgType.bludgeoning], specials)


class Sickle(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        specials.append(WeaponSpecial.trip)
        if size == Size.small:
            dmg = "1d4"
        elif size == Size.medium:
            dmg = "1d6"
        super(Sickle, self).__init__(
            WeaponType.sickle, WeaponCategory.light_melee,
            6, dmg, "20x2", 0, 2, [DmgType.slashing], specials)


class Club(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d4"
        elif size == Size.medium:
            dmg = "1d6"
        super(Club, self).__init__(
            WeaponType.club, WeaponCategory.one_handed_melee,
            0, dmg, "20x2", 10, 3, [DmgType.bludgeoning], specials)


class HeavyMace(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d6"
        elif size == Size.medium:
            dmg = "1d8"
        super(HeavyMace, self).__init__(
            WeaponType.heavy_mace, WeaponCategory.one_handed_melee,
            12, dmg, "20x2", 0, 8, [DmgType.bludgeoning], specials)


class Morningstar(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d6"
        elif size == Size.medium:
            dmg = "1d8"
        super(Morningstar, self).__init__(
            WeaponType.morningstar, WeaponCategory.one_handed_melee,
            8, dmg, "20x2", 0, 6, [DmgType.bludgeoning, DmgType.piercing], specials)


class Shortspear(Weapon):

    def __init__(self, size=Size.medium, specials=[]):
        if size == Size.small:
            dmg = "1d4"
        elif size == Size.medium:
            dmg = "1d6"
        super(Shortspear, self).__init__(
            WeaponType.shortspear, WeaponCategory.one_handed_melee,
            1, dmg, "20x3", 0, 2, [DmgType.slashing], specials)


