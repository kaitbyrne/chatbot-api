import unittest
import requests
from skills.github_connect import *


class TestGithubConnect(unittest.TestCase):

    g = Github("fc9ff48b320a896ee44c15241007da0cc49f5138")
    user = g.get_user()

    def test_api_call(self):

        self.assertEqual(self.user.login, "kaitbyrne")
        self.assertEqual(self.user.bio, "Test bio for project")

    def repo_test(self):

        repos = github_helper('projects')
        self.assertTrue(repos)

    def notification_test(self):

        notifications = github_helper('notifications')
        self.assertTrue(notifications)
