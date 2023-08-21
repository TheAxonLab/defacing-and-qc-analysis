import json
import random
from bids import BIDSLayout
from pathlib import Path

data_path = Path("/data/datasets/DefacingPilotData/original")
deface_path = Path("/data/derivatives/defacing/DefacingPilotData/pydeface/")
blind_path = Path("/data/datasets/DefacingPilotData/shuffled")

n_sub = 10  # nbr of subjects available in the dataset

layout = BIDSLayout(data_path)
sub_id = layout.get_subjects()
sub_id.sort()

blind_dict = dict()
pos_dict = dict()
shuffle_id = list(range(1, n_sub * 2 + 1))
random.shuffle(shuffle_id)
for i, s in enumerate(sub_id):
    blind_dict[f"{s}_non_defaced"] = shuffle_id[i]
    blind_dict[f"{s}_pydeface"] = shuffle_id[i + n_sub]
    pos_dict[f"{i}"] = s

    (blind_path / f"sub-{shuffle_id[i]:02d}" / "ses-V1" / "anat").mkdir(
        exist_ok=True, parents=True
    )

    Path(
        blind_path / f"sub-{shuffle_id[i]:02d}" / f"sub-{shuffle_id[i]}_sessions.json"
    ).symlink_to(data_path / f"sub-{s}" / f"sub-{s}_sessions.json")
    Path(
        blind_path / f"sub-{shuffle_id[i]:02d}" / f"sub-{shuffle_id[i]}_sessions.tsv"
    ).symlink_to(data_path / f"sub-{s}" / f"sub-{s}_sessions.tsv")

    Path(
        blind_path
        / f"sub-{shuffle_id[i]:02d}"
        / "ses-V1"
        / "anat"
        / f"sub-{shuffle_id[i]:02d}_ses-V1_run-1_T1w.json"
    ).symlink_to(
        data_path / f"sub-{s}" / "ses-V1" / "anat" / f"sub-{s}_ses-V1_run-1_T1w.json"
    )
    Path(
        blind_path
        / f"sub-{shuffle_id[i]:02d}"
        / "ses-V1"
        / "anat"
        / f"sub-{shuffle_id[i]:02d}_ses-V1_run-1_T1w.nii.gz"
    ).symlink_to(
        data_path / f"sub-{s}" / "ses-V1" / "anat" / f"sub-{s}_ses-V1_run-1_T1w.nii.gz"
    )

    (blind_path / f"sub-{shuffle_id[i + 10]:02d}" / "ses-V1" / "anat").mkdir(
        exist_ok=True, parents=True
    )

    Path(
        blind_path
        / f"sub-{shuffle_id[i + 10]:02d}"
        / f"sub-{shuffle_id[i + 10]:02d}_sessions.json"
    ).symlink_to(deface_path / f"sub-{s}" / f"sub-{s}_sessions.json")

    Path(
        blind_path
        / f"sub-{shuffle_id[i + 10]:02d}"
        / f"sub-{shuffle_id[i + 10]:02d}_sessions.tsv"
    ).symlink_to(deface_path / f"sub-{s}" / f"sub-{s}_sessions.tsv")

    Path(
        blind_path
        / f"sub-{shuffle_id[i + 10]:02d}"
        / "ses-V1"
        / "anat"
        / f"sub-{shuffle_id[i + 10]:02d}_ses-V1_run-1_T1w.json"
    ).symlink_to(
        deface_path
        / f"sub-{s}"
        / "ses-V1"
        / "anat"
        / f"sub-{s}_ses-V1_run-1_T1w_pydefaced.json"
    )
    Path(
        blind_path
        / f"sub-{shuffle_id[i + 10]:02d}"
        / "ses-V1"
        / "anat"
        / f"sub-{shuffle_id[i + 10]:02d}_ses-V1_run-1_T1w.nii.gz"
    ).symlink_to(
        deface_path
        / f"sub-{s}"
        / "ses-V1"
        / "anat"
        / f"sub-{s}_ses-V1_run-1_T1w_pydefaced.nii.gz"
    )

# Save dictionaries
Path("DefacingPilotData_blind_dict.json").write_text(json.dumps(blind_dict, indent=2))
Path("DefacingPilotData_pos_dict.json").write_text(json.dumps(pos_dict, indent=2))
