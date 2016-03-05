#!/usr/bin/python3.4

import unittest
import model.entity
from model.entity.status_effects import *
import play

class util(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.sword = play.make_sword()
        self.shield = play.make_shield()

    def test_add_remove_status_effect(self):
        self.assertEqual(self.bob.status_effects, set())

        add_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis})

        remove_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, set())

        add_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis})
        add_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis})

        remove_status_effect(self.bob, Afflictions.broken_left_leg)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis})

        add_status_effect(self.bob, Afflictions.silenced)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis, 
            Afflictions.silenced})

        remove_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, {Afflictions.silenced})

        remove_status_effect(self.bob, Afflictions.silenced)
        self.assertEqual(self.bob.status_effects, set())


    def test_check_health(self):
        # make sure everything is healthy
        for part in Body:
            self.assertEqual(check_health(self.bob, {part}), None)

        add_status_effect(self.bob, Afflictions.broken_left_leg)
        self.assertEqual(check_health(self.bob, {Body.left_leg}),
            Afflictions.broken_left_leg)
        self.assertEqual(check_health(self.bob, {Body.right_leg}), None)
        remove_status_effect(self.bob, Afflictions.broken_left_leg)
        self.assertEqual(check_health(self.bob, {Body.left_leg}), None)
        self.assertEqual(check_health(self.bob, {Body.mouth}), None)

        # this seems kind of like a hokey test, but it does test stuff, right?
        for aff in afflictions_map:
            afflicted_parts = afflictions_map[aff]

            add_status_effect(self.bob, aff)
            for part in Body:
                if part in afflicted_parts:
                    self.assertEqual(check_health(self.bob, {part}), aff)
                else:
                    self.assertEqual(check_health(self.bob, {part}), None)
            remove_status_effect(self.bob, aff)
