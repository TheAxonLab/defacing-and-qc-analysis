# # Load IQMs from MRIQC output into a dataframe

import os
import json
import pandas as pd
import numpy as np

n_sub = 580  # nbr of subjects available in the dataset

randomization_path = "../../randomization/"

# For now generate random IQMs since we don't have the data yet
iqms_original = np.random.rand(n_sub, 62)
iqms_defaced = np.random.rand(n_sub, 62)

# Give letters as name
iqms_keys = [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97, 133)]

## Build dataframe
sub_id = np.arange(1, n_sub + 1)
sub_id = sub_id[..., np.newaxis]
i_o = np.hstack((sub_id, iqms_original, np.zeros((n_sub, 1))))
i_d = np.hstack((sub_id, iqms_defaced, np.ones((n_sub, 1))))
print(i_o.shape)
print(i_d.shape)
i_merge = np.vstack((i_o, i_d))
# Verify shape matches expectation
print(i_merge.shape)

# Simulate different site of acquisition.
# The number of images per site corresponds to the number of images per site in the IXI dataset
site1 = np.vstack((np.ones((185, 1)), np.ones((197, 1)) * 2, np.ones((198, 1)) * 3))
site = np.vstack((site1, site1))
print(site.shape)

iqms_df = pd.DataFrame(
    np.hstack((i_merge, site)), columns=["subject"] + iqms_keys + ["defaced"] + ["site"]
)

# Repeated-measures MANOVA is only implemented in R
# Thus we save the dataframe so we can load it in R
iqms_df.to_csv("iqms_df.csv")
