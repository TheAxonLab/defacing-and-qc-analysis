## Datasets

- `S1_Data.tsv` contains the same information as above but with the addition of the defacing status and the original subject ID before obfuscation and shuffling. It is the result of running `augment_IXI_df.py` with `IXI_ratings_df.tsv` as input.

- `S2_Data.tsv` is the table of IQMs used in the automated QC analyses.

- `S3-5_Data.tsv` are the components extracted from IQMs in the corresponding analyses.

- `IXI_ratings_df.tsv` contains the quality scores assigned by the 4 raters on the images of the IXI dataset, the list of artifacts detected, the optional associated comments and the time it took for assessment.

- `simulated_normal_ratings.rds` contains the ratings simulated with a normal distribution using the `simulate_data.R` code, which simulates a bias in favor of defaced images.

- `simulated_normal_nobias_ratings.rds` contains the ratings simulated with a normal distribution using the `simulate_data.R` code without implementing a bias. It is used to verify that the linear-mixed effect models do not find a defacing bias when none has been simulated in the data.
