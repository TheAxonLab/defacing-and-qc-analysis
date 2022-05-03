
import os
import json
import random
from bids import BIDSLayout
from shutil import copyfile
from IPython.core.debugger import set_trace

data_path = "/data/datasets/DefacingPilotData/original"
deface_path = "/data/derivatives/defacing/DefacingPilotData/pydeface/"
blind_path = "/data/datasets/DefacingPilotData/shuffled"

layout = BIDSLayout(data_path)
sub_id = layout.get_subjects()
sub_id.sort()

blind_dict = dict()
pos_dict = dict()
shuffle_id = list(range(0,20))
random.shuffle(shuffle_id)
for i,s in enumerate(sub_id):
    blind_dict['{}_non_defaced'.format(s)] = shuffle_id[i]
    blind_dict['{}_pydeface'.format(s)] = shuffle_id[i+10]
    pos_dict['{}'.format(i)] = s

    """os.makedirs(os.path.join(blind_path,'sub-{}'.format(shuffle_id[i]),'ses-V1','anat'))
    copyfile(os.path.join(data_path, 'sub-{}'.format(s), "sub-{}_sessions.json".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i]), "sub-{}_sessions.json".format(shuffle_id[i])))
    copyfile(os.path.join(data_path, 'sub-{}'.format(s), "sub-{}_sessions.tsv".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i]), "sub-{}_sessions.tsv".format(shuffle_id[i])))
    copyfile(os.path.join(data_path, 'sub-{}'.format(s), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.json".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i]), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.json".format(shuffle_id[i])))
    copyfile(os.path.join(data_path, 'sub-{}'.format(s), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.nii.gz".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i]), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.nii.gz".format(shuffle_id[i])))

    os.makedirs(os.path.join(blind_path,'sub-{}'.format(shuffle_id[i+10]),'ses-V1','anat'))
    copyfile(os.path.join(deface_path, 'sub-{}'.format(s), "sub-{}_sessions.json".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i+10]), "sub-{}_sessions.json".format(shuffle_id[i+10])))
    copyfile(os.path.join(deface_path, 'sub-{}'.format(s), "sub-{}_sessions.tsv".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i+10]), "sub-{}_sessions.tsv".format(shuffle_id[i+10])))
    copyfile(os.path.join(deface_path, 'sub-{}'.format(s), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w_pydefaced.json".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i+10]), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.json".format(shuffle_id[i+10])))
    copyfile(os.path.join(deface_path, 'sub-{}'.format(s), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w_pydefaced.nii.gz".format(s)), \
        os.path.join(blind_path, 'sub-{}'.format(shuffle_id[i+10]), "ses-V1", "anat", "sub-{}_ses-V1_run-1_T1w.nii.gz".format(shuffle_id[i+10])))"""
    

#blind_dict_file = open("DefacingPilotData_blind_dict.json", "w")
#blind_dict_file = json.dump(blind_dict, blind_dict_file)

pos_dict_file = open("DefacingPilotData_pos_dict.json", "w")
pos_dict_file = json.dump(pos_dict, pos_dict_file)