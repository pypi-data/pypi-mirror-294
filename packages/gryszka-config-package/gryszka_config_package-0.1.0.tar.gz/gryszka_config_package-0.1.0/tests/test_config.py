import unittest
import yaml
import importlib.resources
import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestConfig(unittest.TestCase):
    def test_config_loading(self):
        with importlib.resources.open_text('gryszka_config_package', 'config.yml') as f:
            config = yaml.safe_load(f)
            self.assertIn('database', config)
            self.assertEqual(config['database']['host'], 'localhost')
            self.assertEqual(config['database']['port'], 5432)
            self.assertEqual(config['database']['user'], 'admin')
            self.assertEqual(config['database']['password'], 'secret')

if __name__ == '__main__':
    unittest.main()