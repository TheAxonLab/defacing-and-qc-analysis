import os
import json
import random
from bids import BIDSLayout
from shutil import copyfile

#Set the random seed for replicability
day = 230402
time = 343620
random.seed(day + time)

#Extract the subject ID and number of subjects
data_path = "/data/datasets/IXI-T1-BIDS"
blind_path = "/data/datasets/IXI-T1-shuffled"

layout = BIDSLayout(data_path)
sub_id = layout.get_subjects()
sub_id.sort()
n_sub = len(sub_id)

blind_dict = dict()
pos_dict = dict()

#Create new dataset folder and copy basic dataset info
os.makedirs(blind_path)
copyfile(os.path.join(data_path, "dataset_description.json"), \
        os.path.join(blind_path, "dataset_description.json"))
copyfile(os.path.join(data_path, "LICENSE"), \
        os.path.join(blind_path, "LICENSE"))

#Randomly shuffle subject ID for both defaced and non-defaced
shuffle_id = list(range(0,n_sub*2))
random.shuffle(shuffle_id)
for i,s in enumerate(sub_id):
    blind_dict[f'{s}_non_defaced'] = shuffle_id[i]
    blind_dict[f'{s}_defaced'] = shuffle_id[i+n_sub]
    pos_dict[f'{i}'] = s

    sub_path = os.path.join(data_path, f'sub-{s}', "anat")
    new_sub_path_nd = os.path.join(blind_path, f'sub-{shuffle_id[i]}', "anat")
    new_sub_path_d = os.path.join(blind_path,f'sub-{shuffle_id[i+n_sub]}','anat')

    #Copy non-defaced data
    #Create subject directory under new dataset with its shuffled ID
    os.makedirs(new_sub_path_nd)
    #Copy json file
    copyfile(os.path.join(sub_path, f"sub-{s}_T1w.json"), \
        os.path.join(new_sub_path_nd, f"sub-{shuffle_id[i]}_T1w.json"))
    #Copy nifti
    copyfile(os.path.join(sub_path, f"sub-{s}_T1w.nii.gz"), \
        os.path.join(new_sub_path_nd, f"sub-{shuffle_id[i]}_T1w.nii.gz"))

    #Copy defaced data under a different subject ID
    #Create subject directory under new dataset with its shuffled ID
    os.makedirs(new_sub_path_d)
    #Copy json file
    copyfile(os.path.join(sub_path, f"sub-{s}_T1w.json"), \
        os.path.join(new_sub_path_d, f"sub-{shuffle_id[i+n_sub]}_T1w.json"))
    #Copy nifti
    copyfile(os.path.join(sub_path, f"sub-{s}_T1w_defaced.nii.gz"), \
        os.path.join(new_sub_path_d, f"sub-{shuffle_id[i+n_sub]}_T1w.nii.gz"))


# blind_dict_file = open("IXI-T1_blind_dict.json", "w")
# blind_dict_file = json.dump(blind_dict, blind_dict_file)

pos_dict_file = open("IXI-T1_pos_dict.json", "w")
pos_dict_file = json.dump(pos_dict, pos_dict_file)
