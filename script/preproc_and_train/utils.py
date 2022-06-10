import argparse
import re
from pathlib import Path
from typing import List

import wandb
from sklearn.pipeline import Pipeline
from src import LOG_CONFIG_PATH, WANDB_ENTITY_NAME
from src.utils.json import read_jsonlines
from src.utils.logging import get_logger
from src.utils.preprocessing import (
    lowercase_dataset,
    remove_patterns_from_text,
    split_measure_text,
    tokenize_dataset,
)
from src.utils.training import (
    create_classifier,
    create_model,
    create_vectorizer,
    train_classifier,
)
from src.utils.wandb_visualization import (
    get_classification_report_visualization,
    get_confused_examples_visualization,
    get_confusion_matrix_visualization,
    get_data_for_logging,
)

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


def log_results(
    classifier: Pipeline, test_set: dict, project_name: str, config_path: Path
) -> None:
    # TODO: Make directory for each run with logs and model saves (for later when using torch
    # and doing hp search)
    # Log to wandb
    wandb.init(project=project_name, entity=WANDB_ENTITY_NAME)
    # Save the config path
    wandb.save(str(config_path), policy="end")
    # Get the test set predictions
    y_true = test_set["labels"]
    y_pred = classifier.predict(test_set["texts"])
    # Classification report
    classification_report_visualization = get_classification_report_visualization(
        y_true=y_true, y_pred=y_pred
    )
    logger.info(get_data_for_logging(classification_report_visualization))
    wandb.log(classification_report_visualization, commit=False)
    # Confusion matrix
    confusion_matrix_visualization = get_confusion_matrix_visualization(y_true, y_pred)
    logger.info(get_data_for_logging(confusion_matrix_visualization))
    wandb.log(confusion_matrix_visualization, commit=False)
    # Correct and incorrect predictions
    confused_examples_visualization = get_confused_examples_visualization(
        x=test_set["texts"], y_true=y_true, y_pred=y_pred
    )
    logger.info(get_data_for_logging(confused_examples_visualization))
    wandb.log(confused_examples_visualization)
    wandb.finish()
