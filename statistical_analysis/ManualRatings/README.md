## Statistical analysis associated to the defacing pre-registration.

Manual ratings

- The folder `simulation` contains the code pertaining to simulating manual ratings. We used simulations to build and test the models as well as determine the study design at the time of pre-registration.

- `ANOVA.ipynb` is the notebook to run repeated-measures ANOVA and check its assumptions.

- `find_subset_manual_ratings.py` is used to extract from the MRIQC derivatives of the IXI dataset only the reports of subjects that were acquired at the Hammersmith Hospital and copy those subjects under "IXI-manual-only"

- `LinearMixedEffectModels.ipynb` is the alternative notebook we will use in case one of the assumption of the repeated-measures ANOVA is violated.

- `VisualizeIXIRatings.ipnyb` is a notebook to explore the ratings assigned to the IXI dataset by 4 human raters.

- `VisualizeSimulatedRatings.ipnyb` is a notebook to visualize the distributions of simulated ratings, including categorical ratings.
