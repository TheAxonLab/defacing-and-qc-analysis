## Statistical analyses (image quality metrics, IQMs)

- `analysis_iqms.ipynb` is the notebook to run the repeated-measures MANOVA (rm-MANOVA) on the IQMs. Before running rm-MANOVA, the IQMs are standardized and their dimensionality is reduced using PCA. This notebook also presents violinplots and lineplots showing the evolution of the IQMs between the non-defaced and the defaced conditions. The potential influence of defacing on the IQMs reliability is also investigated.
- `ba_analysis.py` is the script to generate the Bland-Altman plot comparing IQMs before and after defacing. The Bland-Altman plot comparing the principal components befre and after defacing is also generated with this code.
- `correlation_plot.py` is the code to plot the clustered IQMs correlation matrix.
- Because we wanted to test our statistical models before looking at the data, we implemented a code `generate_random_iqms.py` that randomly draws two sets of 62 IQMs from a uniform distribution, one set corresponding to the IQMs computed from the non-defaced images, one set corresponding to the IQMs computed from the defaced images. Note that no statistical dependence has been simulated between the IQMs computed from the non-defaced versus defaced images. This code also assembles the IQMs in the dataframe needed to run the analysis in R. The dataframe is saved under `random_iqms_df.csv`.
- `iqms_distribution.py` is the script to plot the overall IQMs distributions. The goal with this figure is to show that some IQMs are problematically always zero.
- `load_iqms.py` is a script to load the IQMs computed on the IXI dataset in the dataframe needed to run the analysis in R. The dataframe is saved in `S2_Data.csv`. 


