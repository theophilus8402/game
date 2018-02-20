#!/usr/bin/python3.4

import unittest
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser("Unit tests.")
    parser.add_argument("-m", default="tests", help="Path to the module to be tested.")
    args = parser.parse_args()

    suite = unittest.TestLoader().discover(args.m, top_level_dir='.')
    unittest.TextTestRunner(verbosity=2).run(suite)
