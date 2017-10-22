
from enum import Enum

DmgType = Enum("DmgType", [
    "slashing",
    "piercing",
    "bludgeoning",
    "fire",
    "cold",
    "poison",
    "acid",
    "psychic",
    "necrotic",
    "radiant",
    "lightning",
    "thunder",
    "healing",
    ])

class DmgInfo():

    def __init__(self):
        # _orig_dmg[DmgType] = dmg_amount
        self._orig_dmg = {}
        # _reductions = [(dmg_type, dmg_amt, reason)]
        self._reductions = []
        # _final[DmgType] = dmg_amount ... this is for final info
        self._final = {}
        self._block_info = {"item": None, "amt": 0}

    def add_dmg(self, dmg_type, amount):
        self._orig_dmg[dmg_type] = amount
        self._final[dmg_type] = amount

    def add_reduction(self, dmg_type, amount, reason):
        self._reductions.append((dmg_type, amount, reason))
        # see if it's a dmg reduction we care about
        if dmg_type in self._final.keys():
            # reduce the dmg
            self._final[dmg_type] -= amount
            # don't let the amount fall below for everything
            # TODO: may want to figure out a way for fire to be able to heal a
            #   lava monster
            if self._final[dmg_type] < 0:
                self._final[dmg_type] = 0

    def add_block(self, item, block_amt):
        self._block_info["item"] = item
        self._block_info["amt"] = block_amt

    @property
    def amt(self):
        return self._final

    @property
    def total(self):
        total = 0
        for dmg_type, amount in self._final.items():
            total += amount
        # For now, block dmg just reduces damage straight off the top
        total -= self._block_info["amt"] 
        return total if total >= 0 else 0

    def __repr__(self):
        dmg_strs = []
        for dmg_type, amt in self._final.items():
            dmg_strs.append("{}/-{}".format(amt, self._orig_dmg[dmg_type]-amt))
        return "<dmg: {}>".format(", ".join(dmg_strs))

