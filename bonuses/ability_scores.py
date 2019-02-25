
import random
from math import floor

from .bonuses import Bonus

def roll_ability_score():

    # roll 4d6
    num_dice = 4
    results = []
    for i in range(num_dice):
        results.append(random.randint(1, 6))

    # total the three largest dice rolled
    results.sort(reverse=True)
    print(results)
    return sum(results[:3])


def calculate_ab_modifier(score):
    return floor((score - 10)/2)


def get_ab_score(world, entity, ab):
    bonuses = world.get_bonuses(entity, "ab", ab)
    return sum([bon.amt for bon in bonuses])


def use_weapon_finesse(entity, weapon):
    return False


def use_dex_attack_bonus(entity, weapon):
    return (use_weapon_finesse(entity, weapon) or 
            (weapon.range > 40))


def get_melee_dmg(entity, str_mod, weapon, two_handed=False, off_hand=False):
    if two_handed and weapon.subtype != "light_melee" and str_mod > 0:
        dmg = floor(1.5*str_mod)
    elif off_hand:
        dmg = floor(.5*str_mod)
    else:
        dmg = str_mod
    return Bonus("dmg", dmg, "str_mod", ents={entity.id},
                    test=lambda weapon: weapon == main_weapon)


def get_ranged_dmg(entity, str_mod, weapon):
    dmg = 0
    return Bonus("dmg", dmg, "str_mod", ents={entity.id},
                    test=lambda weapon: weapon == main_weapon)


def get_wielding_dmg_bonus(entity, str_mod, dex_mod):
    # will look at both weapons being wielded and return
    # appropriate dmg bonuses for both hands

    main_weapon = entity.eq.right_hand
    off_weapon = entity.eq.left_hand

    # make sure the weapons exist and find out something about them
    two_handed = main_weapon and main_weapon == off_weapon
    main_ranged = main_weapon and main_weapon.range >= 50
    off_ranged = off_weapon and off_weapon.range >= 50

    bonuses = []
    dmg_bonus = None

    if two_handed and not main_ranged:
        # two handed melee
        dmg_bonus = get_melee_dmg(entity, str_mod, main_weapon, two_handed=True)
    elif two_handed:
        # two handed ranged
        dmg_bonus = get_ranged_dmg(entity, str_mod, main_weapon)
    elif main_weapon:
        # one handed melee
        dmg_bonus = get_melee_dmg(entity, str_mod, main_weapon)

    if dmg_bonus:
        bonuses.append(dmg_bonus)

    if not two_handed and off_weapon:
        if off_ranged:
            # one handed ranged
            off_dmg = get_ranged_dmg(entity, str_mod, off_weapon)
        else:
            # one handed melee
            off_dmg = get_melee_dmg(entity, str_mod, off_weapon, off_hand=True)
        bonuses.append(off_dmg)

    return bonuses


def determine_wielding_bonuses(world, entity):

    # this should be called when wielding/unwielding a weapon
    # or when str/dex are changed

    bonuses = []

    main_weapon = entity.eq.right_hand
    off_weapon = entity.eq.left_hand

    str_mod = calculate_ab_modifier(get_ab_score(world, entity, "str"))
    dex_mod = calculate_ab_modifier(get_ab_score(world, entity, "dex"))

    # main hand
    if use_dex_attack_bonus(entity, main_weapon):
        att_bonus = Bonus("attack", dex_mod, "dex_mod", ents={entity.id},
                            test=lambda weapon: weapon == main_weapon)
    else:
        att_bonus = Bonus("attack", str_mod, "str_mod", ents={entity.id},
                            test=lambda weapon,**kwargs: weapon == main_weapon)
    bonuses.append(att_bonus)

    dmg_bonuses = get_wielding_dmg_bonus(entity, str_mod, dex_mod)
    bonuses.extend(dmg_bonuses)

    # off hand
    if (off_weapon == main_weapon) or (off_weapon == None):
        # this is either a two-handed weapon or no weapon
        pass

    elif use_dex_attack_bonus(entity, main_weapon):
        off_attack = Bonus("attack", dex_mod, "dex_mod", ents={entity.id},
                            test=lambda weapon: weapon == main_weapon)
        bonuses.append(off_attack)

    else:
        off_attack = Bonus("attack", str_mod, "str_mod", ents={entity.id},
                            test=lambda weapon,**kwargs: weapon == main_weapon)
        bonuses.append(off_attack)

    # determine dmg bonus
    # one handed/two handed
    # composite bow

    return bonuses

def calculate_str_modifiers(world, entity):

    # world is needed to be able to keep track of the bonuses
    # the entity is needed to determine what wielding he/she is wielding
    #   this affects ab bonuses and dmg bonuses
    # and, the entity is needed to determine any applicable feats
    #   i.e. weapon_finesse

    str_mod = calculate_ab_modifier(get_ab_score(world, entity, "str"))

    str_bonuses = []

    # attack and dmg bonuses based on str
    wielding_bonuses = determine_wielding_bonuses(world, entity)
    str_bonuses.extend([b for b in wielding_bonuses if b.reason == "str_mod"])

    # cmb, may change if entity has agile maneuvers feat
    cmb_str_mod = Bonus("cmb", str_mod, "str_mod", ents={entity.id})
    str_bonuses.append(cmb_str_mod)

    # cmd
    cmd_str_mod = Bonus("cmd", str_mod, "str_mod", ents={entity.id})
    str_bonuses.append(cmd_str_mod)

    # skills
    str_skills = ["climb", "swim"]
    for skill in str_skills:
        skill_mod = Bonus("skill", str_mod, "str_mod", subtype=skill,
                            ents={entity.id})
        str_bonuses.append(skill_mod)

    return str_bonuses

