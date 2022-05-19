from script.preproc_and_train.utils import (
    get_dataset,
    get_trained_classifier,
    log_results,
    parse_args,
    preprocess_dataset,
)
from src import LOG_CONFIG_PATH
from src.utils.config import read_config
from src.utils.logging import get_logger

from src.utils.training import (
    get_train_and_test_set,
)

logger = get_logger(log_config_path=LOG_CONFIG_PATH, diplayed_logger_name=__file__)

PROJECT_NAME = "preproc_and_train"


def main():
    # Get the config path
    config_path = parse_args()
    # Read config (all config checks are made in this call)
    config = read_config(config_path)
    # Get the dataset
    dataset = get_dataset(config)
    # Pre-process the dataset
    dataset = preprocess_dataset(dataset, config)
    # Get train and test set
    train_set, test_set = get_train_and_test_set(dataset)
    # TODO: Train (do one iteration for now,
    # then generalize to when you need to do a search)
    classifier = get_trained_classifier(train_set, config)
    # Log results for visualization and analysis
    log_results(
        classifier, test_set, project_name=PROJECT_NAME, config_path=config_path
    )


if __name__ == "__main__":
    main()
