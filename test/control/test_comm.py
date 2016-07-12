#!/usr/bin/python3.4

import unittest
import sys

from control.comm import *

class StdIO(unittest.TestCase):

    def setUp(self):
        self.std_file_comm = Std_IO()

    def test_send_recv(self):
        self.assertEqual(self.std_file_comm.input_handle, sys.stdin)
        self.assertEqual(self.std_file_comm.output_handle, sys.stdout)
        # errr... I don't think I can really test it any more...



class AIIO(unittest.TestCase):

    def setUp(self):
        self.ai_comm = AI_IO(ai_name="Tim")

    def test_send(self):
        self.assertEqual(self.ai_comm.name, "Tim")

        self.assertEqual(self.ai_comm.read_from_server(), None)

        self.ai_comm.send("Howdy")
        self.assertEqual(self.ai_comm.read_from_server(), "Howdy\n")

        self.assertEqual(self.ai_comm.read_from_server(), None)

    def test_recv(self):
        readable, wable, exable = select([self.ai_comm.server_read_handle], [],[],.01)
        self.assertEqual(readable, [])

        self.ai_comm.send_msg_to_server("Hey Server")
        self.assertEqual(self.ai_comm.recv(), "Hey Server\n")

        readable, wable, exable = select([self.ai_comm.server_read_handle], [],[],.01)
        self.assertEqual(readable, [])

        #self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
