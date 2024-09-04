import unittest
import os
import sys
from sqlalchemy import Engine

# Ajoutez le répertoire parent au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '...')))

from galigeopy.org.org import Org

# TODO
CONF = {
    "user": "stihl",
    "password": "319d925e1d52075d1b8d432da90d75b631a0a47b",
    "host": "127.0.0.1",
    "port": 5433,
    "db": "galigeo"
}

class TestOrg(unittest.TestCase):
    def test_org(self):
        # Valid Org
        org = Org(**CONF)
        self.assertTrue(org.is_valid)
        self.assertIsNotNone(org.engine)
        self.assertIsInstance(org.engine, Engine)
        del org
        # Invalid
        org = Org(user="xxx", password="xxx")
        self.assertFalse(org.is_valid)
        del org

    def test_get_networks_list(self):
        # Valid Org
        org = Org(**CONF)
        self.assertTrue(org.is_valid)
        # Get networks list
        df = org.getNetworksList()
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
        del org