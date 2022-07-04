## Statistical analysis associated to the defacing pre-registration.

- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.
- `VisualizeRatings.ipnyb` is a notebook to visualize the distributions of ratings in the defaced vs original conditions. 
- `OrderedLogisticRegression.ipynb` is a notebook to run ordered logistic regression. It is a simpler model than mixed effect regression because it doesn't model between-rater variability. I used it to gain some understanding about logistic regression and continuation ratio assumption.
- `ContinuationRatioModel.ipynb` is the notebook to run continuation ratio model.
- `LinearMixedEffectRegression.ipynb` is the notebook to run linear mixed effect regression. We decided to switch to this model because the implementation of the continuation ratio model is not able to deal with missing values. 
- `MissingValues.ipynb` is the notebook to investigate the maximum of missing values that can be introduced before breaking convergence.

Image quality metrics (IQMs)
- `MANOVAonIQMs` is the notebook to run the MANOVA on IQMs

