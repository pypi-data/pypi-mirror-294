import unittest
import os
import sys

# Ajoutez le répertoire parent au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from galigeopy.galigeopy import check
from tests.org.test_org import TestOrg

class TestGaligeopy(unittest.TestCase):
    def test_check(self):
        self.assertTrue(check())


if __name__ == '__main__':
    unittest.main()