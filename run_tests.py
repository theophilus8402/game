#!/usr/bin/python3.4

import unittest
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser("Unit tests.")
    parser.add_argument("-m", default="all", help="module")
    args = parser.parse_args()
    #print(args.m)

    mods = {
        "db": "test/control/db",
        "control": "test/control",
        "model": "test/model",
        "afflictions": "test/model/entity",
        "all": "test",
    }
    suite = unittest.TestLoader().discover(mods[args.m], top_level_dir='.')
    unittest.TextTestRunner(verbosity=2).run(suite)
