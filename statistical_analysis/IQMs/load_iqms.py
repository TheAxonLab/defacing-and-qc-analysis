# # Load IQMs from MRIQC output into a dataframe

import os
import json
import re
import pandas as pd
import numpy as np

SITE = {
    'HH': 0,
    'Guys': 1,
    'IOP': 2
}

randomization_path = "../../randomization/"
data_path = "/home/cprovins/data/IXI-randomized/"

#Load dictionary to map back anomymized id to participants' original identifier
with open(os.path.join(randomization_path,"IXI_blind_dict.json")) as json_file:
    blind_dict = json.load(json_file)
with open(os.path.join(randomization_path,"IXI_pos_dict.json")) as json_file:
    pos_dict = json.load(json_file)


def get_key(my_dict,val):
    """
    Get the key associated to the known value in a dictionary
    Parameters
    ----------
    my_dict : dictionary to search the value in 
    val : value to search
        Returns
    -------
    key : string associated to the value
    """
    for key, value in my_dict.items():
         if val == value:
             return key


## Load IQMs
iqms_df=pd.read_csv(os.path.join(data_path, 'derivatives', 'mriqc-23.1.0','group_T1w.tsv'),sep='\t')
#Drop non-IQMs columns
iqms_df.drop(labels=['size_x','size_y','size_z','spacing_x','spacing_y','spacing_z'], axis=1)

#Add columns that we need to populate
iqms_df['sub']=None
iqms_df['defaced']=None
iqms_df['site']=None

for i in iqms_df.index:
    pseudo = iqms_df['bids_name'][i]
    pseudo = pseudo.split('_')[0]
    #Extract number
    s = int(re.search(r'\d+', pseudo).group())

    #Retrieve participant's original identifier
    sub = get_key(blind_dict,s)
    iqms_df.at[i,'sub'] = sub.split('_')[0]

    #Retrieve defacing status
    iqms_df.at[i,'defaced'] = int(sub.split('_')[1]=='defaced')

    #Retrieve acquisition site
    print(os.path.join(data_path, pseudo, "anat", f"{pseudo}_T1w.json"))
    with open(os.path.join(data_path, pseudo, "anat", f"{pseudo}_T1w.json")) as json_file:
        sub_json = json.load(json_file)
        print(sub_json['InstitutionName'])
        print(SITE[sub_json['InstitutionName']])
        iqms_df.at[i,'site'] = SITE[sub_json['InstitutionName']]

# Repeated-measures MANOVA is only implemented in R
# Thus we save the dataframe so we can load it in R
iqms_df.to_csv('IXI_iqms_df.csv')
