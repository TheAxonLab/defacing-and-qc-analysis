## Statistical analyses (Manual ratings)

- The folder `simulation/` contains the code pertaining to exploratory analysis on simulated manual ratings. We used simulations to build and test the models as well as determine the study design at the time of pre-registration.

- `anova_analysis.ipynb` is the notebook run repeated-measures ANOVA and check its assumptions.

- `ba_analysis.ipynb` is the notebook containing the Bland-Altman analysis (BA plots).

- `lme_analysis.ipynb` is the notebook to fit linear mixed-effects models to the ratings and use a likelihood ratio test to compare those models fit. The overall goal is to assess the defacing influence in case the assumptions of rm-ANOVA are violated.

- `find_subset_manual_ratings.py` is used to extract from the MRIQC derivatives of the IXI dataset only the reports of subjects that were acquired at the Hammersmith Hospital. Those reports are copied under a separate folder called "IXI-manual-only".



