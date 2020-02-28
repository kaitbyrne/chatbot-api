import unittest
from time import gmtime
from skills.date_time import time_helper
from skills.date_time import date_helper


class TestDateTime(unittest.TestCase):

    def date_test(self):

        date = date_helper()
        self.assertAlmostEqual(date, gmtime())

    def time_test(self):

        time = time_helper()
        self.assertAlmostEqual(time, gmtime())
