import pathlib
import sys

from inkblot.inkblot import generate
from inkblot import config

def main():
    project_dir = pathlib.Path(sys.argv[1])
    if (project_dir / "config.yaml").exists():
        user_config = config.config_from_file(project_dir / "config.yaml")
    else:
        user_config = config.DEFAULT_CONFIG

    generate(pathlib.Path(project_dir), config=user_config)
