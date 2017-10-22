
from .base_spells import spell_map,SpellName
from model.util import RollInfo
from model.entity.damage import DmgInfo,DmgType

def cure_light_wounds(caster, target):

    # heal the target!
    results = RollInfo(1, 8, flat_bonus=1)
    heal_info = DmgInfo()
    heal_info.add_dmg(DmgType.healing, results.total)
    target.apply_damage(heal_info)

    return heal_info

spell_map[SpellName.cure_light_wounds] = cure_light_wounds


