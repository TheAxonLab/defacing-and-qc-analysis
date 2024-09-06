import json
import random
from bids import BIDSLayout
from pathlib import Path


def copy_sub(input_path, output_path, s, id_nd, id_d):
    """
    Copy the nondefaced and the defaced image from a single individual
    under two different randomized IDs

    Parameters
    ----------
    input_path: path to the input data
    output_path: path to the output folder
    s: original subject ID
    id_nd: new subject ID for the nondefaced image
    id_d: new subject ID for the defaced image
    """
    sub_path = input_path / f"sub-{s}" / "anat"
    new_sub_path_nd = output_path / f"sub-{id_nd:04d}" / "anat"
    new_sub_path_d = output_path / f"sub-{id_d:04d}" / "anat"

    # Copy non-defaced data
    # Create subject directory under new dataset with its shuffled ID
    new_sub_path_nd.mkdir(exist_ok=True, parents=True)
    # Copy json file
    Path(new_sub_path_nd / f"sub-{id_nd:04d}_T1w.json").symlink_to(
        sub_path / f"sub-{s}_T1w.json"
    )
    # Copy nifti
    Path(new_sub_path_nd / f"sub-{id_nd:04d}_T1w.nii.gz").symlink_to(
        sub_path / f"sub-{s}_T1w.nii.gz"
    )

    # Copy defaced data under a different subject ID
    # Create subject directory under new dataset with its shuffled ID
    new_sub_path_d.mkdir(exist_ok=True, parents=True)
    # Copy json file
    Path(new_sub_path_d / f"sub-{id_d:04d}_T1w.json").symlink_to(
        sub_path / f"sub-{s}_T1w.json"
    )
    # Copy nifti
    Path(new_sub_path_d / f"sub-{id_d:04d}_T1w.nii.gz").symlink_to(
        sub_path / f"sub-{s}_T1w_defaced.nii.gz"
    )


# Set the random seed for replicability
day = 230402
time = 343620
random.seed(day + time)

# Extract the subject ID and number of subjects
data_path = Path("/data/datasets")
input_path = data_path / "IXI"
output_path = data_path / "IXI-randomized"

layout = BIDSLayout(input_path)
sub_id = layout.get_subjects()
sub_id.sort()
n_sub = len(sub_id)

# Extract participants from Hammersmith Hospital
hh_sub = []
for subject_folder in input_path.iterdir():
    if subject_folder.is_dir() and subject_folder.name.startswith("sub-"):
        json_file_path = subject_folder / "anat" / f"{subject_folder.name}_T1w.json"
        if json_file_path.exists():
            # Open and read the JSON file
            with json_file_path.open("r") as json_file:
                try:
                    json_data = json.load(json_file)
                    institution_name = json_data.get("InstitutionName")
                    if institution_name == "HH":
                        hh_sub.append(subject_folder.name.replace("sub-", "", 1))
                except json.JSONDecodeError as e:
                    print(
                        f"Error reading JSON for subject {subject_folder.name}: {str(e)}"
                    )
        else:
            print(f"JSON file not found for subject {subject_folder.name}")

# Randomly select 40 subjects from the Hammersmith Hospital site that will be shown twice in both conditions
n_rep = 40
subset_rep = random.sample(hh_sub, n_rep)

blind_dict = dict()

# Create new dataset folder and copy basic dataset info
output_path.mkdir(exist_ok=True, parents=True)
Path(output_path / "dataset_description.json").symlink_to(
    input_path / "dataset_description.json"
)
Path(output_path / "LICENSE").symlink_to(input_path / "LICENSE")

# Randomly shuffle subject ID for both defaced and non-defaced
shuffle_id = list(range(1, (n_sub + n_rep) * 2 + 1))
random.shuffle(shuffle_id)

j = 0
for i, s in enumerate(sub_id):
    blind_dict[shuffle_id[i]] = f"{s}_non_defaced"
    blind_dict[shuffle_id[i + n_sub]] = f"{s}_defaced"

    # Copy the defaced and nondefaced images under two different IDs
    copy_sub(input_path, output_path, s, shuffle_id[i], shuffle_id[i + n_sub])

    # If the subject is part of the list of subject to repeat twice
    # copy the subject once again under another subject ID
    if s in subset_rep:
        blind_dict[shuffle_id[n_sub * 2 + j]] = f"{s}_non_defaced"
        blind_dict[shuffle_id[n_sub * 2 + j + n_rep]] = f"{s}_defaced"

        # Copy the defaced and nondefaced images under two different IDs
        copy_sub(
            input_path,
            output_path,
            s,
            shuffle_id[n_sub * 2 + j],
            shuffle_id[n_sub * 2 + j + n_rep],
        )

        # Increment counter of repeated subjects
        j += 1

# Save dictionaries
Path("IXI_blind_dict.json").write_text(json.dumps(blind_dict, indent=2))
