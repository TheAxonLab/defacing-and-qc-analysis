import json
import shutil
from pathlib import Path

# Define the directory where the subjects are stored
subjects_dir = Path('/home/cprovins/data/IXI-randomized/')
mriqc_dir = 'derivatives/mriqc-23.1.0/'
manual_subjects_dir = Path('/home/cprovins/data/IXI-manual-only/')
dest_mriqc_dir = manual_subjects_dir / mriqc_dir

dest_mriqc_dir.mkdir(parents=True, exist_ok=True)

# List to keep track of subject names with "InstitutionName" as "HH"
hh_subjects = []

# Iterate over all subjects
for subject_folder in subjects_dir.iterdir():
    if subject_folder.is_dir() and subject_folder.name.startswith("sub-"):
        json_file_path = subject_folder / 'anat' / f'{subject_folder.name}_T1w.json'
        if json_file_path.exists():
            # Open and read the JSON file
            with json_file_path.open('r') as json_file:
                try:
                    json_data = json.load(json_file)
                    institution_name = json_data.get('InstitutionName')
                    if institution_name == "HH":
                        hh_subjects.append(subject_folder.name)
                except json.JSONDecodeError as e:
                    print(f"Error reading JSON for subject {subject_folder.name}: {str(e)}")
        else:
            print(f"JSON file not found for subject {subject_folder.name}")

assert len(hh_subjects) == (185+40)*2, f"{len(hh_subjects)} subjects from Hammersmith Hospital were found, which is not the 450 we were expected."

# Copy subject folder and HTML report for subjects with "InstitutionName" as "HH"
for sub in hh_subjects:
    source_subject_dir = subjects_dir / mriqc_dir / sub
    dest_subject_dir = dest_mriqc_dir / sub
    shutil.copytree(source_subject_dir, dest_subject_dir)

    # Copy HTML report
    source_html_report = subjects_dir / mriqc_dir / f'{sub}_T1w.html'
    dest_html_report = dest_mriqc_dir / f'{sub}_T1w.html'
    shutil.copy(source_html_report, dest_html_report)

