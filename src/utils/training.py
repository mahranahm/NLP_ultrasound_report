from typing import List, Tuple, Union

import numpy as np
import numpy.typing as npt
from nltk.corpus import stopwords
from sklearn import base
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def get_components_from_dataset(
    dataset: List[dict],
) -> Tuple[npt.NDArray[np.object0], npt.NDArray[np.int64], npt.NDArray[np.object0]]:
    """
    Get text, labels and features as numpy arrays from the dataset.
    """
    # Get the texts
    texts = np.array([elt["text"] for elt in dataset], dtype=object)
    # Get the labels
    labels = np.array([int(elt["label"]) for elt in dataset], dtype=np.int64)
    # Get the features
    features = np.array([elt["features"] for elt in dataset], dtype=object)
    return texts, labels, features


def get_split_dataset_index(
    dataset: List[dict], train_test_ratio_split: float = 0.9, seed: int = 42
) -> Tuple[npt.NDArray[np.int64], npt.NDArray[np.int64]]:
    # List of indices
    indices = np.arange(len(dataset))
    train_index, test_index = train_test_split(
        indices, train_size=train_test_ratio_split, random_state=seed
    )
    return train_index, test_index


def get_train_and_test_set(
    dataset: List[dict], train_test_ratio_split: float = 0.8, seed: int = 42
) -> Tuple[dict, dict]:
    """
    Get the components from the dataset and split them into
    train and test.
    """
    texts, labels, features = get_components_from_dataset(dataset)
    train_index, test_index = get_split_dataset_index(
        dataset, train_test_ratio_split, seed
    )
    texts_train, labels_train, features_train = (
        texts[train_index],
        labels[train_index],
        features[train_index],
    )
    texts_test, labels_test, features_test = (
        texts[test_index],
        labels[test_index],
        features[test_index],
    )
    training_set = {
        "texts": texts_train,
        "labels": labels_train,
        "features": features_train,
    }
    test_set = {
        "texts": texts_test,
        "labels": labels_test,
        "features": features_test,
    }
    return training_set, test_set


def create_vectorizer(
    vectorizer_type: str,
    remove_stopwords: bool = True,
    ngram_range: tuple = (1, 1),
    binary: bool = False,
) -> Union[CountVectorizer, TfidfVectorizer]:
    stop_words = None if not remove_stopwords else stopwords.words("english")
    ngram_range = (
        tuple(ngram_range) if not isinstance(ngram_range, tuple) else ngram_range
    )
    if vectorizer_type == "count":
        vectorizer = CountVectorizer(
            lowercase=False,
            preprocessor=lambda x: x,
            tokenizer=lambda x: x,
            stop_words=stop_words,
            ngram_range=ngram_range,
            binary=binary,
        )
    elif vectorizer_type == "tfidf":
        vectorizer = TfidfVectorizer(
            lowercase=False,
            preprocessor=lambda x: x,
            tokenizer=lambda x: x,
            stop_words=stop_words,
            ngram_range=ngram_range,
        )
    else:
        raise ValueError(f"Unsupported vectorizer type: {vectorizer_type}")

    return vectorizer


def create_model(model_type: str, **model_params) -> base.ClassifierMixin:
    if model_type == "logistic":
        model = LogisticRegression(**model_params)
    elif model_type == "svm":
        model = SVC(**model_params)
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier(**model_params)
    elif model_type == "random_forest":
        model = RandomForestClassifier(**model_params)
    elif model_type == "gradient_boosting":
        model = GradientBoostingClassifier(**model_params)
    elif model_type == "mlp":
        model = MLPClassifier(**model_params)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    return model


def create_classifier(
    vectorizer: Union[CountVectorizer, TfidfVectorizer],
    model: base.ClassifierMixin,
) -> Pipeline:
    return Pipeline([("vectorizer", vectorizer), ("model", model)])


def train_classifier(
    classifier: Pipeline,
    X_train: npt.NDArray[np.float64],
    y_train: npt.NDArray[np.int64],
) -> None:
    classifier.fit(X_train, y_train)


from src.utils.preprocessing import dataset

texts, labels, features = get_components_from_dataset(dataset)

train_index, test_index = get_split_dataset_index(dataset, train_test_ratio_split=0.99)

texts_train, labels_train = (texts[train_index], labels[train_index])

vectorizer = create_vectorizer(vectorizer_type="count")

model = create_model(model_type="svm")

classifier = create_classifier(vectorizer, model)

train_classifier(classifier, texts_train, labels_train)

print(classifier.score(texts_train, labels_train))
