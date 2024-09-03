import yaml
import importlib.resources
import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def read_something_from_yml():
    config_path = importlib.resources.files('gryszka_config_package') / 'config.yml'
    with config_path.open('r') as f:
        config = yaml.safe_load(f)
        return config