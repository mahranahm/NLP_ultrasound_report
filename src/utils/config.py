import importlib
import os
from pathlib import Path
from src import CONFIG_SCHEMA_DIRECTORY

import yaml
from schema import SchemaError

# All configs are expected to have a schema key-value pair.
SCHEMA_KEY = "schema"
# Relative paths to make importlib work
RELATIVE_SCHEMA_PACKAGE = "src.configs.schemas"


def read_config(config_file_path: Path) -> dict:
    """
    Reads the config file (expect .yml), validates it and returns it as a dictionary.
    """
    assert config_file_path.suffix == ".yml", "Config file must be a .yml file."
    with open(config_file_path, "r") as f:
        config = yaml.safe_load(f)
    assert SCHEMA_KEY in config, "Config file must have a schema key."
    # Use importmodule to dynamically load the correct schema object
    try:
        schema_module = importlib.import_module(
            f".{config['schema']}", package=RELATIVE_SCHEMA_PACKAGE
        )
    except Exception:
        raise ValueError(
            f"Cannot import module {config['schema']}. "
            + f"Only {[elt for elt in os.listdir(CONFIG_SCHEMA_DIRECTORY) if elt.endswith('.py')]} available."
        )
    # Get the schema object from the schema module, will return an error if the schema is not found
    try:
        config_schema = schema_module.config_schema
    except AttributeError as e:
        raise e
    # Validate the config
    try:
        config_schema.validate(config)
    except SchemaError as e:
        raise e
    return config
