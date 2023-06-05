"""Reorganize the NIfTi files from the IXI dataset to conform to BIDS specifications

Before running this script, please download the T1w images and 
the demographic information at https://brain-development.org/ixi-dataset/."""

import os
import shutil
import json
import pandas as pd
import numpy as np
from os.path import join

#Create output dataset folder if doesn't exist
input_path = join('/data','datasets','IXI-T1')
output_path = join('/data','datasets','IXI-T1-BIDS')
if not os.path.isdir(output_path):
    os.mkdir(output_path)

    #Copy and convert demographic information to tsv file
    subinfo_xls = join(input_path,'IXI.xls')
    subinfo_tsv = join(output_path,'participants.tsv')
    #Read excel file into a dataframe
    data_xlsx = pd.read_excel(subinfo_xls, 'Table', index_col=None)
    #Replace all columns having spaces with underscores
    data_xlsx.columns = [c.replace(' ', '_') for c in data_xlsx.columns]
    #Replace all fields having line breaks with space
    df = data_xlsx.replace('\n', ' ',regex=True)
    df = df.replace(np.nan, "n/a", regex=True)
    #Reformat subject ID column to abide to BIDS specification
    df = df.rename(columns={'IXI_ID': 'participant_id'})
    #Add "sub-" in front of each subject ID
    df['participant_id'] = df['participant_id'].apply(lambda x: f'sub-{x}')
    
    #Write dataframe into tsv
    df.to_csv(subinfo_tsv, sep='\t', encoding='utf-8',  index=False, line_terminator='\r\n')

    #Create mandatory dataset_description.json
    data_dict = {
        'Name' : "IXI dataset",
        "BIDSVersion": "1.8.0",
        "License": "CC BY-SA 3.0"}
    data_json = json.dumps(data_dict)

    #Copy hand-written participants.json
    shutil.copy(join('/data','code','DefacingProject','bidsify','participants.json'), 
                join(output_path,'participants.json'))

    #Write json to file
    f = open(join(output_path,'dataset_description.json'), "x")
    f.write(data_json)
    f.close()

#Iterate over all the subjects in the input dataset folder
for sub in os.listdir(input_path):
    if sub.endswith(".nii.gz"):
        #Extract the subject number from filename
        sub_nbr = sub[3:6]
        sub_path = join(output_path, f'sub-{sub_nbr}')

        #Create subfolder for the subject
        if not os.path.isdir(sub_path):
            os.mkdir(sub_path)
            #Create anat subfolder
            anat_path = join(sub_path, 'anat')
            os.mkdir(anat_path)
            #Copy Nifti and adapt name
            file_path = join(anat_path, f'sub-{sub_nbr}_T1w.nii.gz')
            shutil.copy(join(input_path,sub), file_path)

            #Create a json file to encode acquisition site
            #Extract acquisition site from file name
            acq_site = sub.split('-')[1]
            sub_dict = {'InstitutionName' : acq_site}
            sub_json = json.dumps(sub_dict)

            #Write json to file
            f = open(join(anat_path,f'sub-{sub_nbr}_T1w.json'), "x")
            sub_json = json.dumps(sub_dict, f)

        

