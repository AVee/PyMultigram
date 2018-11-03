'''
Created on 2 Nov 2018

@author: AVee
'''
import unittest
from pyrogram.client.client import Client
from pymultigram.multigram import MultiHandler

class Test(unittest.TestCase):

    def testSetClients(self):
        client1 = Client("Test 1")  # Normal user
        client2 = Client("Test 2")  # Normal user
        client3 = Client("123456789:ABCDEFGHIJKLMNOPQRSTUVW1234567890ab") # Bot
        client4 = Client("987654321:ABCDEFGHIJKLMNOPQRSTUVW1234567890ab") # Bot
        client5 = Client("876543210:ABCDEFGHIJKLMNOPQRSTUVW1234567890ab") # Bot

        handler = MultiHandler()
        handler.set_clients([client1, client2, client3, client4, client5])
        
        assert(handler._clients.__len__() == 5)
        assert(handler._bots.__len__() == 3)
        assert(handler._users.__len__() == 2)

        handler2 = MultiHandler()
        handler2.set_clients([client3, client5])
        assert(handler2._clients.__len__() == 2)
        assert(handler2._bots.__len__() == 2)
        assert(handler2._users.__len__() == 0)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSetClients']
    unittest.main()