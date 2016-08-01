
import enum
from math import floor

from model.entity.living.status_effects import Body

@enum.unique
class Proficiency(enum.Enum):
    # armour:
    light_armour = 0
    medium_armour = 1
    heavy_armour = 2
    shields = 3
    # weapons:
    simple_weapons = 4
    martial_weapons = 5
    # tools: TODO
    # saving throws:
    strength = 6
    constitution = 7
    charisma = 8
    dexterity = 9
    intelligence = 10
    wisdom = 11
    # skills:
    acrobatics = 12
    animal_handling = 13
    arcana = 14
    athletics = 15
    deception = 16
    history = 17
    insight = 18
    intimidation = 19
    investigation = 20
    medicine = 21
    nature = 22
    perception = 23
    performance = 24
    persuasion = 25
    religion = 26
    sleight_of_hand = 27
    stealth = 28
    survival = 29


@enum.unique
class Class(enum.Enum):
    fighter = 0
    cleric = 1
    rogue = 2
    wizard = 3


@enum.unique
class Ability(enum.Enum):
    strength = 0
    dexterity = 1
    constitution = 2
    intelligence = 3
    wisdom = 4
    charisma = 5


@enum.unique
class Property(enum.Enum):
    light = 0
    finesse = 1
    thrown = 2
    two_handed = 3
    versatile = 4
    ammunition = 5
    loading = 6
    heavy = 7
    reach = 8
    special = 9


@enum.unique
class ActionType(enum.Enum):
    # this is used for determinig what actions are still available for the
    #   entity this round not for fully defining every action available
    move = 0
    ready = 1
    defend = 2
    attack_left_hand = 3
    attack_right_hand = 4
    interact_obj = 5


proficiency_modifiers = {
    # right now, it doesn't look the other classes are any different
    # but, this might change.  So, I'm going to pretend everyone is a fighter
    # for now.
    (Class.fighter, 1) : 2,
    (Class.fighter, 2) : 2,
    (Class.fighter, 3) : 2,
    (Class.fighter, 4) : 2,
    (Class.fighter, 5) : 3,
    (Class.fighter, 6) : 3,
    (Class.fighter, 7) : 3,
    (Class.fighter, 8) : 3,
    (Class.fighter, 9) : 4,
    (Class.fighter, 10) : 4,
    (Class.fighter, 11) : 4,
    (Class.fighter, 12) : 4,
    (Class.fighter, 13) : 5,
    (Class.fighter, 14) : 5,
    (Class.fighter, 15) : 5,
    (Class.fighter, 16) : 5,
    (Class.fighter, 17) : 6,
    (Class.fighter, 18) : 6,
    (Class.fighter, 19) : 6,
    (Class.fighter, 20) : 6,
    }


def set_ability(entity, ability, score):
    # Set's the ability score and modifier for the entity.  Needs the entity,
    # ability (which is an enum from Ability), and and int for the score.
    modifier = floor((score - 10)/2)
    entity.abilities[ability] = (score, modifier)


def get_ability_modifier(entity, ability):
    # Returns the modifier associated with the ability.  Needs the entity and
    # the ability which is an enum from Ability.
    score, modifier = entity.abilities[ability]
    return modifier


def get_proficiency_modifier(entity, prof_mod):
    # Checks to see if the entity is proficient, then determines and returns the
    # proficiency value.  Needs an actual entity and a Proficiency enum value.
    modifier = 0
    if prof_mod in entity.proficiencies:
        #TODO: the static assignment of Class.fighter might need to change.
        # mentioned what's going on up above in "class Proficiency"
        modifier = proficiency_modifiers[(Class.fighter, entity.level)]
    return modifier


def get_weapon_in_hand(entity, hand=Body.right_arm):
    return entity.eq[hand]


def get_attack_bonus(entity, weapon, melee=True, ammo=None):
    attack_bonus = 0
    # get the ability modifier
    if melee:
        # check to see if the weapon is finesse and the entity would benefit from dex
        if weapon and Property.finesse in weapon.properties:
            str_mod = get_ability_modifier(entity, Ability.strength)
            dex_mod = get_ability_modifier(entity, Ability.dexterity)
            if dex_mod >= str_mod:
                ability = Ability.dexterity
        else:
            ability = Ability.strength
    else:
        ability = Ability.dexterity
    attack_bonus += get_ability_modifier(entity, ability)
        
    # get the proficiency modifier
    if weapon:
        attack_bonus += get_proficiency_modifier(entity, weapon.proficiency)

    # TODO: get any weapon/ammo/spell modifiers
    return attack_bonus
