
import json

bonus_types = {"ab", "cmb", "cmd", "skill", "attack", "dmg"}
bonus_subtypes = {"str", "dex", "con", "int", "wis", "cha",
                    "acrobatics", "appraise", "bluff", "climb", "craft",
                    "diplomacy", "disable_device", "disguise", "escape_artist",
                    "fly", "handle_animal", "heal", "intimidate",
                    "knowledge_arcana", "knowledge_dungeoneering",
                    "knowledge_engineering", "knowledge_geography",
                    "knowledge_history", "knowledge_local", "knowledge_nature",
                    "knowledge_nobility", "knowledge_planes",
                    "knowledge_religion", "linguistics", "perception",
                    "perform", "profession", "ride", "sense_motive",
                    "sleight_of_hand", "spellcraft", "stealth", "survival",
                    "swim", "use_magic_device",
                }
bonus_reasons = {"base", "str_mod", "dex_mod", "con_mod", "int_mod",
                    "wis_mod", "cha_mod", "race"}

class Bonus():

    largest_bonus_id = -1

    def __init__(self, type, amt, reason, subtype=None, id=None,
                    test=None, ents=set()):

        if id != None:
            if Bonus.largest_bonus_id < id:
                Bonus.largest_bonus_id = id
            self.id = id
        else:
            Bonus.largest_bonus_id += 1
            self.id = Bonus.largest_bonus_id

        if type in bonus_types:
            self.type = type
        else:
            raise ValueError("{} is not a valid item in {}.".format(
                    type, "bonus_types"))

        if subtype and subtype not in bonus_subtypes:
            raise ValueError("{} is not a valid item in {}.".format(
                    subtype, "bonus_subtypes"))
        self.subtype = subtype

        self.amt = amt

        if reason in bonus_reasons:
            self.reason = reason
        else:
            raise ValueError("{} is not a valid item in {}.".format(
                    reason, "bonus_reasons"))

        self.test = test
        self.ents = ents

    def __repr__(self):
        if self.subtype:
            btype = "{}:{}".format(self.type, self.subtype)
        else:
            btype = self.type
        return "<{}: {} {} {}>".format(self.id, btype, self.amt, self.reason)


def get_bonuses(world, entity, type, subtype=None):
    bonuses = [bon for bon in world.bonuses if entity.id in bon.ents and
                                                bon.type == type]
    if subtype:
        bonuses = [bon for bon in bonuses if bon.subtype == subtype]
    return bonuses


def save_bonuses(bonuses, output_file):
    with open(output_file, "w") as f:
        #json.dump(bonuses, f, default=lambda b: b.__dict__,
        #            sort_keys=True, indent=4)
        json.dump(bonuses, f, sort_keys=True, indent=4)


def build_bonus_from_json(bonus_json):
    if isinstance(bonus_json, dict) and len(bonus_json) > 2:
        return Bonus(**bonus_json)
    return bonus_json

def load_bonuses(input_file):
    with open(input_file, "r") as f:
        bonuses = json.load(f, object_hook=build_bonus_from_json)
    return bonuses

