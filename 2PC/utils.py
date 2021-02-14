import os
import yaml


def get_relative_path(path: str, rel_to: str) -> str:
    return os.path.join(os.path.dirname(rel_to), path)


def load_yaml(path: str):
    with open(path) as fd:
        config = yaml.load(fd, yaml.FullLoader)
        config["yaml_path"] = path
        return config


def load_config():
    return load_yaml(get_relative_path("config.yaml", __file__))
