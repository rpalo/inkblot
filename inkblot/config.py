from inkblot import yaml

DEFAULT_CONFIG = {
    "source_dir": "src",
    "build_dir": "output",
}

def config_from_file(path):
    text = path.read_text()
    config = dict()
    config.update(DEFAULT_CONFIG)
    config.update(yaml.loads(text))
    return config