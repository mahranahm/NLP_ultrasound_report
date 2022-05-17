from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from src import LOG_CONFIG_PATH
from src.utils.logging import get_logger

logger = get_logger(log_config_path=LOG_CONFIG_PATH, diplayed_logger_name=__file__)


def get_metrics(classifier: Pipeline, test_set: dict) -> None:
    """
    Get the metrics for the classifier on the test set.
    """
    y_true = test_set["labels"]
    y_pred = classifier.predict(test_set["texts"])
    logger.info(confusion_matrix(y_true=y_true, y_pred=y_pred))
