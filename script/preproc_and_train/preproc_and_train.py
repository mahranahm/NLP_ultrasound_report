import argparse
import re
from pathlib import Path
from typing import List
from src.utils.evaluation import get_metrics

import wandb
from sklearn.pipeline import Pipeline
from src import LOG_CONFIG_PATH, RANDOM_SEED
from src.utils.config import read_config
from src.utils.json import read_jsonlines
from src.utils.logging import get_logger
from src.utils.preprocessing import (lowercase_dataset,
                                     remove_patterns_from_text,
                                     split_measure_text, tokenize_dataset)
from src.utils.training import (create_classifier, create_model,
                                create_vectorizer, get_train_and_test_set,
                                train_classifier)

logger = get_logger(log_config_path=LOG_CONFIG_PATH, diplayed_logger_name=__file__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess and train a model with the ultrasound text files and labels."
    )
    parser.add_argument(
        "-c",
        "--config_path",
        help="The path to the preproc and train config file (should be .yml).",
        required=True,
    )
    args = parser.parse_args()
    config_path = Path(args.config_path)

    return config_path


def get_dataset(config: dict) -> List[dict]:
    dataset_config = config["dataset"]
    return read_jsonlines(file_path=dataset_config["path"])


def preprocess_dataset(dataset: List[dict], config: dict) -> List[dict]:
    """
    Preprocess the dataset. The resulting text field will become a list
    of tokens.
    """
    # Get the preprocessing part of the config
    preprocessing_config = config["preprocessing"]
    # Removal of patterns
    patterns = [
        re.compile(pattern) for pattern in preprocessing_config["patterns_to_remove"]
    ]
    dataset = remove_patterns_from_text(dataset, patterns)
    # Lowercasing
    if preprocessing_config["lowercase"]:
        dataset = lowercase_dataset(dataset)
    # Splitting of text that consists of measurements
    if preprocessing_config["split_measure_text"]:
        dataset = split_measure_text(dataset)
    # Tokenization
    dataset = tokenize_dataset(
        dataset, tokenizer_type=preprocessing_config["tokenizer_type"]
    )
    return dataset


def get_trained_classifier(train_set: dict, config: dict) -> Pipeline:
    """
    NOTE: The use of features is still uncertain.
    """
    # Get the training part of the config
    training_config = config["training"]
    vectorizer_config = training_config["vectorizer"]
    model_config = training_config["model"]
    # Create vectorizer
    vectorizer = create_vectorizer(
        vectorizer_type=vectorizer_config["vectorizer_type"],
        remove_stopwords=vectorizer_config["remove_stopwords"],
        ngram_range=vectorizer_config["ngram_range"],
        binary=vectorizer_config["binary"],
    )
    # Create model
    model = create_model(
        model_type=model_config["model_type"], **model_config["model_params"]
    )
    # Create classifier
    classifier = create_classifier(vectorizer, model)
    # Fit classifier
    train_classifier(
        classifier, X_train=train_set["texts"], y_train=train_set["labels"]
    )
    return classifier


def main():
    # Log to wandb
    wandb.init(project="preproc_and_train", entity="ultrasound")
    # Get the config path
    config_path = parse_args()
    # Read config (all config checks are made in this call)
    config = read_config(config_path)
    wandb.config = config
    # Get the dataset
    dataset = get_dataset(config)
    # Pre-process the dataset
    dataset = preprocess_dataset(dataset, config)
    # Get train and test set
    train_set, test_set = get_train_and_test_set(
        dataset, train_test_ratio_split=0.8, seed=RANDOM_SEED
    )
    # TODO: Train (do one iteration for now,
    # then generalize to when you need to do a search)
    classifier = get_trained_classifier(train_set, config)
    # TODO: Metrics, error analysis
    get_metrics(classifier, test_set)




if __name__ == "__main__":
    main()
