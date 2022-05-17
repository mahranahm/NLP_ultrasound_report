from pathlib import Path

REPO_DIRECTORY = Path(__file__).parent.parent

SRC_DIRECTORY = REPO_DIRECTORY / "src"

CONFIG_SCHEMA_DIRECTORY = SRC_DIRECTORY / "configs" / "schemas"

LOG_CONFIG_PATH = REPO_DIRECTORY / "configs" / "logging.conf"

RANDOM_SEED = 42
