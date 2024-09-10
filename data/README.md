## Scripts to handle data associated to the defacing pre-registration.

- `from_mongodb_to_dataframe.py` is the script to load the ratings from the mongo database into a dataframe.

- `augment_IXI_df.py` is the script to reconstruct the pairing to match the non-defaced image with its corresponding defaced image for each subject using the pairing dictionary that we saved when we performed the randomization.

- `IXI_ratings_df.tsv` contains the quality scores assigned by the 4 raters on the images of the IXI dataset, the list of artifacts detected, the optional associated comments and the time it took for assessment.

- `IXI_augmented_ratings_df.tsv` contains the same information as above but with the addition of the defacing status and the original subject ID before obfuscation and shuffling.

- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.

- `simulated_normal_ratings.rds` contains the ratings simulated with a normal distribution using the `simulate_data.R` code simulating a bias in favor of defaced images.

- `simulated_normal_nobias_ratings.rds` contains the ratings simulated with a normal distribution using the `simulate_data.R` code without implementing a bias. It is used to verify that the linear-mixed effect models do not find a defacing bias when none has been simulated in the data.
