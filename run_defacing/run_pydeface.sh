#!/bin/sh

data_path="/data/datasets/IXI"

cd $data_path

for file in sub-*
do
    pydeface "$data_path/$file/anat/${file: -7}_T1w.nii.gz"
done