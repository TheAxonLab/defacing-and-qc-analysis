## Script to handle data associated to the defacing pre-registration.

- `from_mongodb_to_dataframe.py` is the script to load the ratings from the mongo database into a dataframe.

- `augment_IXI_df.py` is the script to reconstruct the pairing to match the non-defaced image with its corresponding defaced image for each subject using the pairing dictionary that we saved when we performed the randomization.

- `IXI_ratings_df.csv` contains the quality scores assigned by the 4 raters on the images of the IXI dataset.

- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.

- `simulated_normal_ratings.rds` contains the ratings simulated with a normal distribution using the `simulate_data.R` code.
