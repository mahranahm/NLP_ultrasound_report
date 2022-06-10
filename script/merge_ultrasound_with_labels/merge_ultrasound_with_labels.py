from script.merge_ultrasound_with_labels.utils import (
    get_ultrasound_features,
    get_ultrasound_labels,
    get_ultrasound_text_dict,
    merge_ultrasound_dataset,
    parse_args,
    write_merged_dataset_to_jsonl,
)


TEXT_TO_REMOVE = [
    "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION:",
    "PROTOCOLE RADIOLOGIQUE / RADIOLOGIST'S REPORT:",
    "IMPRESSION",
]


def main():
    # Get arguments
    (
        ultrasound_folder_input_path,
        labels_file_path,
        features_file_path,
        output_file_path,
    ) = parse_args()
    # Get dictionary of ultrasound text with ids as their key
    ultrasound_text_dict = get_ultrasound_text_dict(ultrasound_folder_input_path)
    # Get the labels
    ultrasound_labels_dict = get_ultrasound_labels(labels_file_path)
    # Get the features
    ultrasound_features_dict = get_ultrasound_features(features_file_path)
    # Merge the text, labels and features as a list of dictionaries
    merged_ultrasound_dataset_dicts = merge_ultrasound_dataset(
        ultrasound_text_dict, ultrasound_labels_dict, ultrasound_features_dict
    )
    # Write the merged dataset to a .jsonl file
    write_merged_dataset_to_jsonl(merged_ultrasound_dataset_dicts, output_file_path)


if __name__ == "__main__":
    main()
