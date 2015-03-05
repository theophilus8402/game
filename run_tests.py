#!/usr/bin/python3.4

#import control.roll
import unittest
#import test.testRoll

#roll(num_die, sides, modifier)
#class test.roll.TestSequenceFunctions(unittest.TestCase)

if __name__ == '__main__':
    #stuff = test.roll.TestSequenceFunctions()
    #unittest.main()

    #loader = unittest.TestLoader()
    #loader.discover("test")
    #loader.loadTestsFromModule("test.testRoll")

    suite = unittest.TestLoader().discover('test', top_level_dir='.')
    #suite = unittest.TestLoader().loadTestsFromModule("test")
    unittest.TextTestRunner(verbosity=2).run(suite)
