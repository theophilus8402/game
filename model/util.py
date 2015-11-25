from math import sqrt

fighter_bab = [[0], [1], [2], [3], [4], [5], [6, 1], [7, 2], [8, 3], [9, 4],
    [10, 5], [11, 6, 1], [12, 7, 2], [13, 8, 3], [14, 9, 4], [15, 10, 5],
    [16, 11, 6, 1], [17, 12, 7, 2], [18, 13, 8, 3], [19, 14, 9, 4],
    [20, 15, 10, 5]]

cleric_bab = [[0], [0], [1], [2], [3], [3], [4], [5], [6, 1], [6, 1],
    [7, 2], [8, 3], [9, 4], [9, 4], [10, 5], [11, 6, 1], [12, 7, 2],
    [12, 7, 2], [13, 8, 3], [14, 9, 4], [15, 10, 5]]

wizard_bab = [[0], [0], [1], [1], [2], [2], [3], [3], [4], [4], [5], [5],
    [6, 1], [6, 1], [7, 2], [7, 2], [8, 3], [8, 3], [9, 4], [9, 4], [10, 5]]


base_attack_bonus = {
    "fighter": fighter_bab,
    "barbarian": fighter_bab,
    "paladin": fighter_bab,
    "ranger": fighter_bab,
    "cleric": cleric_bab,
    "druid": cleric_bab,
    "rogue": cleric_bab,
    "bard": cleric_bab,
    "monk": cleric_bab,
    "wizard": wizard_bab,
    "sorcerer": wizard_bab }

def get_bab(class_name, level):
    return base_attack_bonus[class_name][level]

barbarian_base_save_bonus = {
    "fort": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "ref": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "will": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
}

bard_base_save_bonus = {
    "fort": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "ref": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "will:": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12]
}

cleric_base_save_bonus = {
    "fort:": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "ref": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "will:": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12]
}

monk_base_save_bonus = {
    "fort": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "ref": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "will": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
}

rogue_base_save_bonus = {
    "fort": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "ref": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
    "will": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
}

sorcerer_base_save_bonus = {
    "fort": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "ref": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    "will": [0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
        11, 12],
}

base_save_bonus = {
    "barbarian": barbarian_base_save_bonus,
    "bard": bard_base_save_bonus,
    "cleric": cleric_base_save_bonus,
    "druid": cleric_base_save_bonus,
    "fighter": barbarian_base_save_bonus,
    "monk": monk_base_save_bonus,
    "paladin": barbarian_base_save_bonus,
    "ranger": barbarian_base_save_bonus,
    "rogue": rogue_base_save_bonus,
    "sorcerer": sorcerer_base_save_bonus,
    "wizard": sorcerer_base_save_bonus,
}

def get_base_save_bonus(class_name, save_type, level):
    return base_save_bonus[class_name][save_type][level]

level_xps = {
    1: 0,
    2: 1000,
    3: 3000,
    4: 6000,
    5: 10000,
    6: 15000,
    7: 21000,
    8: 28000,
    9: 36000,
    10: 45000,
    11: 55000,
    12: 66000,
    13: 78000,
    14: 91000,
    15: 105000,
    16: 120000,
    17: 136000,
    18: 153000,
    19: 171000,
    20: 190000,
}

def check_level_up(cur_level, current_xp):
    """
    Returns True if current_xp is above the next level up's cap.
        i.e. cur_level: 1, current_xp: 1100 would return True
    """
    return current_xp >= level_xps[cur_level + 1]

def get_class_skill_max_ranks(level):
    class_skill_max_ranks = [0]
    class_skill_max_ranks.extend([n for n in range(4, 24)])
    if level >= len(class_skill_max_ranks):
        # we've gone over our level limit, so we're going to return
        #   the highest number
        level = len(class_skill_max_ranks) - 1
    return class_skill_max_ranks[level]

def get_cross_class_skill_max_ranks(level):
    cross_max_ranks = [0]
    cross_max_ranks.extend([n/2 for n in range(4, 24, 1)])
    if level >= len(cross_max_ranks):
        # we've gone over our level limit, so we're going to return
        #   the highest number
        level = len(cross_max_ranks) - 1
    return cross_max_ranks[level]

def check_new_feat_for_level(level):
    new_feat_per_level = {
        1: True,
        3: True,
        6: True,
        9: True,
        12: True,
        15: True,
        18: True,
    }
    return getattr(new_feat_per_leve, level, False)

def check_for_new_attrib(level):
    if level == 0:
        level = 1
    return (level % 4) == 0

size_modifiers = {"colossal": -8, "gargantuan": -4, "huge": -2, "large": -1,
            "medium": 0, "small": 1, "tiny": 2, "diminutive": 4, "fine": 8}

def find_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    squared_distance = (x2 - x1)**2 + (y2 - y1)**2
    return sqrt(squared_distance)
