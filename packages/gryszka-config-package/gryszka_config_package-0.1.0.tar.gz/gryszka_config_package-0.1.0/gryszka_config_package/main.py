import yaml
import importlib.resources
import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with importlib.resources.open_text('gryszka_config_package', 'config.yml') as f:
    config = yaml.safe_load(f)

print(config)