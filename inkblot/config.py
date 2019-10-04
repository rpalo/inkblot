from inkblot import yaml

DEFAULT_CONFIG = {
    "source_dir": "src",
    "build_dir": "output",
    "conversions": {
        ".md": [
            "md_to_html",
            "add_layout",
            "jinjafy",
        ],
        ".html": [
            "add_layout",
            "jinjafy",
        ],
        ".sass": [
            "jinjafy",
            "compile_sass",
        ]
    },
    "extra_conversions": {},
}

def config_from_file(path):
    text = path.read_text()
    config = dict()
    config.update(DEFAULT_CONFIG)
    config.update(yaml.loads(text))
    return config