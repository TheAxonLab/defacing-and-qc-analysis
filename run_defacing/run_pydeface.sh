#!/bin/sh

data_path="/data/datasets/IXI-T1-BIDS"
defaced_path="/data/datasets/IXI-T1-defaced"

mkdir -p $defaced_path

cp "$data_path/dataset_description.json" "$defaced_path/dataset_description.json"
cp "$data_path/LICENSE" "$defaced_path/LICENSE"

cd $data_path

for file in sub-*
do
    mkdir -p "$defaced_path/$file/anat/"
    cp "$data_path/$file/anat/${file: -7}_T1w.json" "$defaced_path/$file/anat/${file: -7}_T1w.json" 
    pydeface --outfile "$defaced_path/$file/anat/${file: -7}_T1w.nii.gz" "$data_path/$file/anat/${file: -7}_T1w.nii.gz"
done