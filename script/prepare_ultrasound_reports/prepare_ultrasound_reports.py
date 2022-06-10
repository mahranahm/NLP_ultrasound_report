from script.prepare_ultrasound_reports.utils import (
    get_ultrasound_text_bodies,
    get_ultrasound_text_file_paths,
    parse_args,
    write_ultrasound_text_bodies,
)

# Constants, to be updated as more data is added
EXCLUDED_FILES = ["132 U.txt"]
BODY_BEGIN_MARKERS = "RENSEIGNEMENT CLINIQUE / CLINICAL INFORMATION"
BODY_END_MARKERS = ["Case dictated by", "Electronically signed by", "Dossier/MRN:"]
BODY_BETWEEN_START_MARKERS = [
    "Hôpital de Montréal pour Enfants / Montreal Children's Hospital"
]
BODY_BETWEEN_END_MARKERS = ["Rapport/Report"]


def main():
    # Parse the command line arguments
    ultrasound_folder_input_path, output_folder_path = parse_args()
    # Collect the ultrasound text file paths
    ultrasound_text_file_paths = get_ultrasound_text_file_paths(
        ultrasound_folder_input_path, excluded_files=EXCLUDED_FILES
    )
    # Get the ultrasound text file bodies
    ultrasound_text_bodies = get_ultrasound_text_bodies(
        ultrasound_text_file_paths,
        body_begin_markers=BODY_BEGIN_MARKERS,
        body_end_markers=BODY_END_MARKERS,
        body_between_start_markers=BODY_BETWEEN_START_MARKERS,
        body_between_end_markers=BODY_BETWEEN_END_MARKERS,
    )
    # Write the ultrasound text bodies to the output folder
    write_ultrasound_text_bodies(
        ultrasound_text_bodies, output_folder_path, ultrasound_text_file_paths
    )


if __name__ == "__main__":
    main()
