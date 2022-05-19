import numpy as np
import numpy.typing as npt
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from src import LOG_CONFIG_PATH
from src.utils.logging import get_logger

logger = get_logger(log_config_path=LOG_CONFIG_PATH, diplayed_logger_name=__file__)


def get_prediction(classifier: Pipeline, dataset: dict) -> npt.NDArray[np.int64]:
    """
    Get the prediction for the classifier on the dataset.
    """
    y_pred = classifier.predict(dataset["texts"])
    return y_pred


def get_confusion_matrix(
    y_true: npt.NDArray[np.int64], y_pred: npt.NDArray[np.int64]
) -> None:
    """
    Get the confusion matrix for the set of true and predict labels.
    """
    return confusion_matrix(y_true=y_true, y_pred=y_pred)
