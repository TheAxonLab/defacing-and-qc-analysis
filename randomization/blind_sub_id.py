import os
import json
import random
from bids import BIDSLayout
from shutil import copyfile
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
    os.makedirs(new_sub_path_nd)
    # Copy json file
    copyfile(
        sub_path / f"sub-{s}_T1w.json",
        new_sub_path_nd / f"sub-{id_nd:04d}_T1w.json",
    )
    # Copy nifti
    copyfile(
        sub_path / f"sub-{s}_T1w.nii.gz",
        new_sub_path_nd / f"sub-{id_nd:04d}_T1w.nii.gz",
    )

    # Copy defaced data under a different subject ID
    # Create subject directory under new dataset with its shuffled ID
    os.makedirs(new_sub_path_d)
    # Copy json file
    copyfile(
        sub_path / f"sub-{s}_T1w.json", new_sub_path_d / f"sub-{id_d:04d}_T1w.json"
    )
    # Copy nifti
    copyfile(
        sub_path / f"sub-{s}_T1w_defaced.nii.gz",
        new_sub_path_d / f"sub-{id_d:04d}_T1w.nii.gz",
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

# Randomly select 40 subjects that will be shown twice in both conditions
n_rep = 40
subset_rep = random.sample(sub_id, n_rep)

blind_dict = dict()
pos_dict = dict()

# Create new dataset folder and copy basic dataset info
os.makedirs(output_path, exist_ok=True)
copyfile(
    input_path / "dataset_description.json", output_path / "dataset_description.json"
)
copyfile(input_path / "LICENSE", output_path / "LICENSE")

# Randomly shuffle subject ID for both defaced and non-defaced
shuffle_id = list(range(1, (n_sub + n_rep) * 2 + 1))
random.shuffle(shuffle_id)

j=0
for i, s in enumerate(sub_id):
    blind_dict[f"{s}_non_defaced"] = shuffle_id[i]
    blind_dict[f"{s}_defaced"] = shuffle_id[i + n_sub]
    pos_dict[f"{i}"] = s

    # Copy the defaced and nondefaced images under two different IDs
    copy_sub(input_path, output_path, s, shuffle_id[i], shuffle_id[i + n_sub])

    # If the subject is part of the list of subject to repeat twice
    # copy the subject once again under another subject ID
    if s in subset_rep:
        blind_dict[f"{s}_non_defaced"] = shuffle_id[n_sub * 2 + j]
        blind_dict[f"{s}_defaced"] = shuffle_id[n_sub * 2 + j + n_rep]
        pos_dict[f"{i}"] = s

        # Copy the defaced and nondefaced images under two different IDs
        copy_sub(
            input_path,
            output_path,
            s,
            shuffle_id[n_sub * 2 + j],
            shuffle_id[n_sub * 2 + j + n_rep],
        )

        #Increment counter of repeated subjects
        j+=1


blind_dict_file = open("IXI_blind_dict.json", "w")
blind_dict_file = json.dump(blind_dict, blind_dict_file)

pos_dict_file = open("IXI_pos_dict.json", "w")
pos_dict_file = json.dump(pos_dict, pos_dict_file)
