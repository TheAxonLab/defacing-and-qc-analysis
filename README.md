# defacing-and-qc-analysis
Code associated to the Defacing pre-registration

- `bidsify` contains the code to reorganize the Nifti files of the IXI dataset to abide to BIDS specifications.
- `data` contains the code to simulate ratings, load the quality grades assigned using [Q'kay](https://github.com/nipreps/qkay.git) and reconstruct correpondence of ratings with variables necessary for the analysis, that is the defacing status and original subject ID. The dataframes resulting from running these code are also stored in this folder.
- `pilot_study` contains data, code and plots associated to the pilot study.
- `run_defacing` contains code to run defacing tools on nondefaced data.
- `randomization` contains the code to randomly select a subset of the IXI dataset for the manual ratings analysis and randomize participants identifier.
- `statistical_analysis` contains code to run statistical analyses. The folder is separated in two subfolders: the analysis of the IQMs computed automatically by MRIQC and the analysis of the quality scores assigned manually by raters that inspected the MRIQC visual report.


