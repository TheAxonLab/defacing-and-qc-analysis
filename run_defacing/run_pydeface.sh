#!/bin/sh

data_path="/data/datasets/DefacingPilotData/"
save_path="/data/derivatives/defacing/DefacingPilotData/pydeface/"

cd $data_path

for file in sub-CHUV*
do 
    T1_path="$data_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.nii.gz"
    T1_defaced_path="$save_path$file/ses-V1/anat/"
    mv "$T1_defaced_path${file: -12}_ses-V1_run-1_T1w_pydeface.json" "$T1_defaced_path${file: -12}_ses-V1_run-1_T1w_pydefaced.json" 
    #cp "$data_path$file/${file: -12}_sessions.json" "$save_path$file/${file: -12}_sessions.json"
    #cp "$data_path$file/${file: -12}_sessions.tsv" "$save_path$file/${file: -12}_sessions.tsv"
    #cp "$data_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.json" "$save_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.json"
    #mkdir -p $T1_defaced_path
    #pydeface --outfile "$data_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w_pydeface.nii.gz" $T1_path
done