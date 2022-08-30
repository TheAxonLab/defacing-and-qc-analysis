"""Load IQMs from MRIQC output into a dataframe"""

import os
import json
import pandas as pd
import numpy as np

n_sub = 580 #nbr of subjects available in the dataset

randomization_path = "../../randomization/"
data_path = "/data/derivatives/mriqc/RoyalCarpetPlot/DefacingPilotData/shuffled"

#Load dictionary to map back anomymized id to participants' original identifier
with open(os.path.join(randomization_path,"DefacingPilotData_blind_dict.json")) as json_file:
    blind_dict = json.load(json_file)
with open(os.path.join(randomization_path,"DefacingPilotData_pos_dict.json")) as json_file:
    pos_dict = json.load(json_file)


def get_key(my_dict,val):
    """
    Get the key associated to the know value in a dictionary
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
iqms_original = np.zeros((n_sub,61))
iqms_defaced = np.zeros((n_sub,61))
sub_id = np.zeros((n_sub,1))
for s in range(0,n_sub*2):
    with open(os.path.join(data_path, 'sub-{}'.format(s), "ses-V1", "anat","sub-{}_ses-V1_run-1_T1w.json".format(s))) as json_file:
        iqms = json.load(json_file)
        iqms_keys = list(iqms.keys())
        #Drop non-IQMs keys
        iqms_keys.remove('bids_meta')
        iqms_keys.remove('provenance')
        iqms_keys.remove('size_x')
        iqms_keys.remove('size_y')
        iqms_keys.remove('size_z')
        iqms_keys.remove('spacing_x')
        iqms_keys.remove('spacing_y')
        iqms_keys.remove('spacing_z')

    #Retrieve participant's original identifier
    sub = get_key(blind_dict,s)
    pos = int(get_key(pos_dict,sub[0:8]))

    sub_id[pos]=sub

    if "non_deface" in sub:
        for i,key in enumerate(iqms_keys):
            iqms_original[pos,i] = iqms[key]
    elif "pydeface" in sub:
        for i,key in enumerate(iqms_keys):
            iqms_defaced[pos,i] = iqms[key]
    else:
        raise ValueError("{} is an invalid name".format(sub))


# +
#For now generate random IQMs since we don't have the data yet
iqms_original = np.random.rand(n_sub,62)
iqms_defaced = np.random.rand(n_sub,62)

#Give letters as name
iqms_keys = [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97, 133)]
# -

## Build dataframe
sub_id = np.arange(1, n_sub+1)
sub_id = sub_id[..., np.newaxis]
i_o = np.hstack((sub_id, iqms_original, np.zeros((n_sub,1))))
i_d = np.hstack((sub_id, iqms_defaced,np.ones((n_sub,1))))
print(i_o.shape)
print(i_d.shape)
i_merge = np.vstack((i_o,i_d))
#Verify shape matches expectation
print(i_merge.shape)

iqms_df = pd.DataFrame(i_merge, columns = ['subject'] + iqms_keys + ['defaced'])

# Repeated measure MANOVA is only implemented in R
# Thus we save the dataframe so we can load it in R
iqms_df.to_csv('iqms_df.csv')
