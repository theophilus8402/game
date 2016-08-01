#!/usr/bin/python3.4

import unittest

from model.entity.basic_entity import *
import play

class BasicEntity(unittest.TestCase):

    def setUp(self):
        # Bob's vol=12, weight=192
        # sword's vol=1, weight=6
        # shield's vol=3, weight=5
        self.bob = play.make_bob()
        self.sword = play.make_sword()
        self.shield = play.make_shield()

    def test_entity_get_volume_weight(self):
        self.assertEqual(entity_get_volume_weight(self.bob), (12, 192))
        self.assertEqual(entity_get_volume_weight(self.sword), (1, 6))
        self.assertEqual(entity_get_volume_weight(self.shield), (3, 5))
