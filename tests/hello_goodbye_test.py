import unittest
from skills.hello import hello_helper
from skills.goodbye import goodbye_helper


class TestDateTime(unittest.TestCase):

    def date_test(self):

        hello = hello_helper()
        self.assertTrue(hello)

    def time_test(self):

        goodbye = goodbye_helper()
        self.assertTrue(goodbye)
