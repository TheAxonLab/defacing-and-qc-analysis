# Code and data specific to the pilot study
- `ManualRatings` contains the manual quality scores assigned to the pilot data.
- `blind_sub_id.py` contains the code we used to randomize participant identifiers of the pilot data. The pairing to match the non-defaced image with its corresponding defaced image for each subject is stored in the dictionaries `DefacingPilotData_blind_dict.json` and `DefacingPilotData_pos_dict.json`.
- `correlation_plot.py` contains the code to plot the correlation matrix of the IQMs extracted from the ABIDE dataset. We presented this plot as a proof of concept in the Stage 1 pre-registration, but replaced it with the correlation between IQMs from the IXI dataset in the Stage 2 manuscript.
- `run_pydeface.sh` is the script to run defacing using the tool PyDeface on the pilot data.
- `dim_reduction_ABIDE.ipynb` is the test ground to experiment with dimensionality reduction of the IQMs.
- `statistical_analysis.ipynb` is the notebook that we use to run the statistical analysis in python for our pilot study.
