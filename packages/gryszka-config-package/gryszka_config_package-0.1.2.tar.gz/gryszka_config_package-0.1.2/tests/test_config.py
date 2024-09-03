import unittest
import yaml
import importlib.resources
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gryszka_config_package.main import read_something_from_yml


class TestConfig(unittest.TestCase):
    def test_config_loading(self):
        config_path = importlib.resources.files('gryszka_config_package') / 'config.yml'
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
            self.assertIn('database', config)
            self.assertEqual(config['database']['host'], 'localhost')
            self.assertEqual(config['database']['port'], 5432)
            self.assertEqual(config['database']['user'], 'admin')
            self.assertEqual(config['database']['password'], 'secret')

    def test_read_something_from_yml(self):
        config = read_something_from_yml()
        self.assertIn('database', config)
        self.assertEqual(config['database']['host'], 'localhost')
        self.assertEqual(config['database']['port'], 5432)
        self.assertEqual(config['database']['user'], 'admin')
        self.assertEqual(config['database']['password'], 'secret')

if __name__ == '__main__':
    unittest.main()