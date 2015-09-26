
import model.util

def show_ac(entity):
    ac = entity.ac
    dex, dex_mod = entity.attrib["dex"]
    size_mod = model.util.size_modifiers[entity.size]
    print("Total: {}  Base: {}  Armour: {}  Shield: {}".format(ac["total"],
        ac["base"], ac["armour"], ac["shield"]))
    print("Dex_Mod: {}  Size_Mod: {}  Misc: {}".format(dex_mod, size_mod,
        ac["misc"]))
