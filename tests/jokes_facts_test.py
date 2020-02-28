import unittest
from skills.fun_facts import fun_facts_helper
from skills.jokes import jokes_helper


class TestJokesFacts(unittest.TestCase):

    def jokes_test(self):

        jokes = jokes_helper()
        self.assertTrue(jokes)

    def facts_test(self):

        facts = fun_facts_helper()
        self.assertTrue(facts)
