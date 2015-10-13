#!/usr/bin/python3.4

import unittest
import hashlib
import control.db.entity as db_ent

class entity_humanoid(unittest.TestCase):

    def setUp(self):
        self.living_ents, self.max_uid = db_ent.load_entities(
            "test/control/db/bob.txt")
        self.bob = self.living_ents["bob"]

    def test_load_bob(self):
        self.assertEqual(self.bob.name, "bob")
        self.assertEqual(self.bob.uid, 1)
        self.assertEqual(self.bob.symbol, "B")
        self.assertEqual(self.bob.cur_loc, (-2, 1))
        self.assertEqual(self.bob.cur_hp, 17)
        self.assertEqual(self.bob.max_hp, 10)
        self.assertEqual(self.bob.short_desc, "This is Bob.")
        self.assertEqual(self.bob.long_desc,
            "This is Bob. He's rugged looking.")
        self.assertEqual(self.bob.weight, 192.0)
        self.assertEqual(self.bob.volume, 0.0)
        self.assertEqual(self.bob.friction, 12.0)
        self.assertEqual(self.bob.cur_mp, 6)
        self.assertEqual(self.bob.max_mp, 10)
        self.assertEqual(self.bob.status_msgs, ["lost balance"])
        self.assertEqual(self.bob.vision_range, 6)
        self.assertEqual(self.bob.level, 2)
        self.assertEqual(self.bob.hit_dice, "2d4")
        self.assertEqual(self.bob.race, "human")
        self.assertEqual(self.bob.str, 15)
        self.assertEqual(self.bob.dex, 14)
        self.assertEqual(self.bob.wis, 12)
        self.assertEqual(self.bob.con, 13)
        self.assertEqual(self.bob.int, 14)
        self.assertEqual(self.bob.cha, 11)
        self.assertEqual(self.bob.ac, 16)
        self.assertEqual(self.bob.fortitude, 13)
        self.assertEqual(self.bob.reflex, 14)
        self.assertEqual(self.bob.will, 15)

    def determine_hash(self, file_name):
        m = hashlib.md5()
        with open(file_name, "rb") as f:
            for line in f.readlines():
                m.update(line)
        return m.digest()

    def test_save_bob(self):
        db_ent.save_entities(self.living_ents, "test/control/db/bob2.txt")
        bob_hash = self.determine_hash("test/control/db/bob.txt")
        bob2_hash = self.determine_hash("test/control/db/bob2.txt")
        self.assertEqual(bob_hash, bob2_hash)


if __name__ == '__main__':
    unittest.main()
