## Statistical analysis associated to the defacing pre-registration.

Image quality metrics (IQMs)
- Because we wanted to test our statistical models before looking at the data, we implemented a code `generate_random_iqms.py` that randomly draws two sets of 62 IQMs from a uniform distribution, one set corresponding to the IQMs computed from the non-defaced images, one set corresponding to the IQMs computed from the defaced images. Note that no statistical dependence has been simulated between the IQMs computed from the non-defaced versus defaced images. This code also assembles the IQMs in the dataframe needed to run the analysis in R.
- `load_iqms.py` is a script to load the IQMs computed on the IXI dataset in the dataframe needed to run the analysis in R
- `AnalysisIQMs` is the notebook to run the repeated measures MANOVA on the IQMs and the comparison of the covariance matrices.
- `correlation_plot` is the notebook to plot the clustered IQMs correlation matrix.

