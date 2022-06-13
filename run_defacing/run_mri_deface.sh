#!/bin/sh

data_path="/data/datasets/DefacingPilotData/"
save_path="/data/derivatives/defacing/DefacingPilotData/mri_deface/"

cd $data_path

for file in sub-CHUV*
do 
    T1_path="$data_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.nii.gz"
    T1_defaced_path="$save_path$file/ses-V1/anat/"
    #cp "$data_path$file/${file: -12}_sessions.json" "$save_path$file/${file: -12}_sessions.json"
    #cp "$data_path$file/${file: -12}_sessions.tsv" "$save_path$file/${file: -12}_sessions.tsv"
    #cp "$data_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.json" "$save_path$file/ses-V1/anat/${file: -12}_ses-V1_run-1_T1w.json"
    #mkdir -p $T1_defaced_path
    cd /data/code/DefacingProject
    #mv "$T1_defaced_path${file: -12}_ses-V1_run-1_T1w_mri_defaced.nii.gz" "$T1_defaced_path${file: -12}_ses-V1_run-1_T1w.nii.gz"
    ./mri_deface $T1_path talairach_mixed_with_skull.gca face.gca "$T1_defaced_path${file: -12}_ses-V1_run-1_T1w.nii.gz"
done