
import bonuses
import entities

from bonuses.ability_scores import *
from entities.weapons import *
from world import World

if __name__ == "__main__":

    bonus_file = "saved_bonuses.json"

    #game_bonuses = bonuses.load_bonuses(bonus_file)

    World.get_bonuses = bonuses.get_bonuses
    world = World("fun")

    tim = entities.Living("Tim")

    str_bonus = bonuses.Bonus("ab", 16, "base", subtype="str", ents={tim.id})
    dex_bonus = bonuses.Bonus("ab", 16, "base", subtype="dex", ents={tim.id})
    con_bonus = bonuses.Bonus("ab", 14, "base", subtype="con", ents={tim.id})
    int_bonus = bonuses.Bonus("ab", 11, "base", subtype="int", ents={tim.id})
    wis_bonus = bonuses.Bonus("ab", 13, "base", subtype="wis", ents={tim.id})
    cha_bonus = bonuses.Bonus("ab", 9, "base", subtype="cha", ents={tim.id})
    race_bonus = bonuses.Bonus("ab", 2, "race", subtype="str", ents={tim.id})

    world.bonuses.extend([str_bonus, dex_bonus, con_bonus,
                            int_bonus, wis_bonus, cha_bonus, race_bonus])

    tim.equip(longsword, "right_hand", both_hands=True)

    print(world.bonuses)

    #bonuses.save_bonuses(world.bonuses, bonus_file)

