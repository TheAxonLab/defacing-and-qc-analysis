# Processing the original data

- `from_mongodb_to_dataframe.py` is the script to load the ratings from the mongo database into a dataframe.

- `augment_IXI_df.py` is the script to reconstruct the pairing to match the non-defaced image with its corresponding defaced image for each subject using the pairing dictionary that we saved when we performed the randomization.