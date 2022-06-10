from typing import List, Union
import numpy as np
import numpy.typing as npt
from sklearn.metrics import classification_report, confusion_matrix
import plotly.graph_objs as go
import wandb
import pandas as pd


def get_classification_report_visualization(
    y_true: npt.NDArray[np.int64], y_pred: npt.NDArray[np.int64], digits=5
) -> dict[str, wandb.Table]:
    # Get the classification report as a dictionary from sklearn
    classification_report_dict = classification_report(
        y_true, y_pred, digits=digits, output_dict=True
    )
    # Separate accuracy from the rest of the report
    accuracy = classification_report_dict["accuracy"]
    del classification_report_dict["accuracy"]
    accuracy_table = wandb.Table(columns=["accuracy_score"], data=[[accuracy]])
    # Convert dictionary to pandas dataframe
    classification_report_df = pd.DataFrame(classification_report_dict).T
    # Insert the row name as a column since wandb doesn't have row names
    classification_report_df.insert(0, "class", classification_report_df.index)
    classification_report_table = wandb.Table(dataframe=classification_report_df)
    return {
        "accuracy_score": accuracy_table,
        "classification_report": classification_report_table,
    }


def get_confusion_matrix_visualization(
    y_true: npt.NDArray[np.int64], y_pred: npt.NDArray[np.int64]
) -> dict[str, go.Figure]:
    # Part of this code is taken from:
    # https://colab.research.google.com/drive/1k89TDv8ybckgfVByUIhY6peBjtNGBH-k?usp=sharing#scrollTo=RO1MSGLeAzWp
    labels = np.sort(np.unique(y_true))

    confmatrix = confusion_matrix(y_pred, y_true)
    confdiag = np.eye(len(confmatrix)) * confmatrix
    np.fill_diagonal(confmatrix, 0)

    confmatrix = confmatrix.astype("float")
    n_confused = np.sum(confmatrix)
    confmatrix[confmatrix == 0] = np.nan
    confmatrix = go.Heatmap(
        {
            "coloraxis": "coloraxis1",
            "x": labels,
            "y": labels,
            "z": confmatrix,
            "hoverongaps": False,
            "hovertemplate": "Predicted %{y}<br>Instead of %{x}<br>On %{z} examples<extra></extra>",
        }
    )

    confdiag = confdiag.astype("float")
    n_right = np.sum(confdiag)
    confdiag[confdiag == 0] = np.nan
    confdiag = go.Heatmap(
        {
            "coloraxis": "coloraxis2",
            "x": labels,
            "y": labels,
            "z": confdiag,
            "hoverongaps": False,
            "hovertemplate": "Predicted %{y} right<br>On %{z} examples<extra></extra>",
        }
    )

    fig = go.Figure((confdiag, confmatrix))
    transparent = "rgba(0, 0, 0, 0)"
    n_total = n_right + n_confused
    fig.update_layout(
        {
            "coloraxis1": {
                "colorscale": [
                    [0, transparent],
                    [0, "rgba(180, 0, 0, 0.05)"],
                    [1, f"rgba(180, 0, 0, {max(0.2, (n_confused/n_total) ** 0.5)})"],
                ],
                "showscale": False,
            }
        }
    )
    fig.update_layout(
        {
            "coloraxis2": {
                "colorscale": [
                    [0, transparent],
                    [0, f"rgba(0, 180, 0, {min(0.8, (n_right/n_total) ** 2)})"],
                    [1, "rgba(0, 180, 0, 1)"],
                ],
                "showscale": False,
            }
        }
    )

    xaxis = {
        "title": {"text": "y_true"},
        "tickvals": labels,
        "ticktext": [f"{label}" for label in labels],
        "tickmode": "array",
    }
    yaxis = {
        "title": {"text": "y_pred"},
        "tickvals": labels,
        "ticktext": [f"{label}" for label in labels],
        "tickmode": "array",
    }

    fig.update_layout(
        title={"text": "Confusion matrix", "x": 0.5},
        paper_bgcolor=transparent,
        plot_bgcolor=transparent,
        xaxis=xaxis,
        yaxis=yaxis,
    )

    return {"confusion_matrix": wandb.data_types.Plotly(fig)}


def _convert_list_to_text(input_list: np.ndarray) -> List[str]:
    return [" ".join(inner_list) for inner_list in input_list]


def _fill_list(
    input_list: Union[list, np.array], desired_length: int, list_filler: str = ""
) -> List[str]:
    if len(input_list) > desired_length:
        raise ValueError(
            f"Cannot fill input_list to desired length of {desired_length} "
            + f"because it already has length {len(input_list)}"
        )
    if isinstance(input_list, np.ndarray):
        input_list = input_list.tolist()
    return input_list + [list_filler] * (desired_length - len(input_list))


def get_confused_examples_visualization(
    x: npt.NDArray[np.object0],
    y_true: npt.NDArray[np.int64],
    y_pred: npt.NDArray[np.int64],
    max_confused_examples=3,
) -> dict[str, wandb.data_types.Plotly]:
    # Get examples of correct and incorrect examples
    # for each class
    labels = np.sort(np.unique(y_true))
    correct_prediction_examples = []
    incorrect_prediction_examples = []
    for true_label in labels:
        for predicted_label in labels:
            if true_label == predicted_label:
                correct_prediction_examples.append(
                    {
                        "class": f"{true_label}",
                        "examples": _convert_list_to_text(
                            x[(y_pred == y_true) & (y_true == true_label)][
                                :max_confused_examples
                            ]
                        ),
                    }
                )
            else:
                incorrect_prediction_examples.append(
                    {
                        "true_class": f"{true_label}",
                        "predicted_class": f"{predicted_label}",
                        "examples": _convert_list_to_text(
                            x[(y_true == true_label) & (y_pred == predicted_label)][
                                :max_confused_examples
                            ]
                        ),
                    }
                )
    # Format the results for wandb
    # Single table for the correct predictions
    correct_prediction_columns = ["Class"] + [
        f"Example {i}" for i in range(1, max_confused_examples + 1)
    ]
    correct_prediction_data = [
        [
            correct_prediction_example["class"],
            *_fill_list(correct_prediction_example["examples"], max_confused_examples),
        ]
        for correct_prediction_example in correct_prediction_examples
    ]
    correct_prediction_table = {
        "Correct predictions": wandb.Table(
            columns=correct_prediction_columns, data=correct_prediction_data
        )
    }
    # One table for each true class for the confused examples
    incorrect_prediction_columns = ["Predicted Class"] + [
        f"Example {i}" for i in range(1, max_confused_examples + 1)
    ]
    incorrect_prediction_data = {}
    for incorrect_prediction_example in incorrect_prediction_examples:
        true_class = incorrect_prediction_example["true_class"]
        predicted_label = incorrect_prediction_example["predicted_class"]
        examples = incorrect_prediction_example["examples"]
        if true_class not in incorrect_prediction_data:
            incorrect_prediction_data[true_class] = []
        incorrect_prediction_data[true_class].append(
            [predicted_label, *_fill_list(examples, max_confused_examples)]
        )
    incorrect_prediction_tables = {
        f"Incorrect predictions for true class = {true_class}": wandb.Table(
            columns=incorrect_prediction_columns, data=data
        )
        for true_class, data in incorrect_prediction_data.items()
    }
    return {**correct_prediction_table, **incorrect_prediction_tables}


def get_data_for_logging(visualization_dict: dict) -> dict:
    return {
        key: value.data
        for key, value in visualization_dict.items()
        if hasattr(value, "data")
    }
