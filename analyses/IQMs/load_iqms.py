# # Load IQMs from MRIQC output into a dataframe

import json
import re
import pandas as pd
from pathlib import Path

SITE = {
    'HH': 0,
    'Guys': 1,
    'IOP': 2
}

randomization_path = Path("../../randomization/")
data_path = Path("/home/cprovins/data/IXI-randomized/")

#Load dictionary to map back anonymized id to participants' original identifier
with open(randomization_path / "IXI_blind_dict.json") as json_file:
    blind_dict = json.load(json_file)

## Load IQMs
iqms_df=pd.read_csv(data_path / 'derivatives' / 'mriqc-23.1.0'/ 'group_T1w.tsv',sep='\t')
#Drop non-IQMs columns
iqms_df = iqms_df.drop(labels=['size_x','size_y','size_z','spacing_x','spacing_y','spacing_z'], axis=1)

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
    sub = blind_dict[str(s)]
    iqms_df.at[i,'sub'] = sub.split('_')[0]

    #Retrieve defacing status
    iqms_df.at[i,'defaced'] = int(sub.split('_')[1]=='defaced')

    #Retrieve acquisition site
    with open(data_path / pseudo / "anat" / f"{pseudo}_T1w.json") as json_file:
        sub_json = json.load(json_file)
        iqms_df.at[i,'site'] = SITE[sub_json['InstitutionName']]

# Repeated-measures MANOVA is only implemented in R
# Thus we save the dataframe so we can load it in R
iqms_df.to_csv('S2_Data.csv')
