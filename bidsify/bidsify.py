#!/usr/bin/env python
"""
Reorganize the NIfTi files from the IXI dataset to conform
to the BIDS specification.

Before running this script, please download the T1w images and
the demographic information at https://brain-development.org/ixi-dataset/.
"""

import shutil
import json
import pandas as pd
import numpy as np
from pathlib import Path

# Create output dataset folder if doesn't exist
datasets_path = Path("/data/datasets")
input_path = datasets_path / "IXI" / "sourcedata"
output_path = datasets_path / "IXI"
subinfo_xls = input_path / "IXI.xls"
subinfo_tsv = output_path / "participants.tsv"

if not subinfo_tsv.exists():  # Convert phenotypical information
    # Read excel file into a dataframe
    data_xlsx = pd.read_excel(subinfo_xls, "Table", index_col=None)
    # Replace all columns having spaces with underscores
    data_xlsx.columns = [c.replace(" ", "_") for c in data_xlsx.columns]
    # Replace all fields having line breaks with space
    df = data_xlsx.replace("\n", " ", regex=True)
    df = df.replace(np.nan, "n/a", regex=True)
    # Reformat subject ID column to abide to BIDS specification
    df = df.rename(columns={"IXI_ID": "participant_id"})
    # Add "sub-" in front of each subject ID
    df["participant_id"] = df["participant_id"].apply(lambda x: f"sub-{x}")

    # Write dataframe into tsv
    df.to_csv(
        subinfo_tsv, sep="\t", encoding="utf-8", index=False, line_terminator="\r\n"
    )

    # Create mandatory dataset_description.json
    data_dict = {
        "Name": "IXI dataset",
        "SourceDatasets": [{"URL": "https://brain-development.org/ixi-dataset/"}],
        "BIDSVersion": "1.8.0",
        "License": "CC BY-SA 3.0",
    }
    data_json = json.dumps(data_dict, indent=2)

    # Write out the JSON file
    (output_path / "dataset_description.json").write_text(data_json)

    # Copy hand-written participants.json
    shutil.copy(Path("./participants.json"), output_path / "participants.json")

# Iterate over all the subjects in the input dataset folder
for sub in input_path.glob("*.nii.gz"):
    # Extract the subject number from filename
    sub_nbr = sub.name[3:6]
    sub_path = output_path / f"sub-{sub_nbr}"

    # Create BIDS tree for the subject
    (sub_path / "anat").mkdir(exist_ok=True, parents=True)

    # Copy Nifti and adapt name
    file_path = sub_path / "anat" / f"sub-{sub_nbr}_T1w.nii.gz"
    file_path.symlink_to(sub)

    # Create a JSON to record acquisition site
    acq_site = sub.name.split("-")[1]
    sub_dict = {"InstitutionName": acq_site}
    (sub_path / "anat" / f"sub-{sub_nbr}_T1w.json").write_text(
        json.dumps(sub_dict, indent=2)
    )
