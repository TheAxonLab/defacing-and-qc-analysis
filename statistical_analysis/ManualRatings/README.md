## Statistical analysis associated to the defacing pre-registration.

Manual ratings
- `ContinuationRatioModel.ipynb` is the notebook to run continuation ratio model.
- `LinearMixedEffectRegression.ipynb` is the notebook to run linear mixed effect regression. We decided to switch to this model because the implementation of the continuation ratio model is not able to deal with missing values.
- In `VaryDatasetParameters.ipynb` I tried to change all dataset parameters to make the model defaced + (defaced|rater) converge to a non-singular solution without success.
- `MissingValues.ipynb` is the notebook to investigate the maximum of missing values that can be introduced before breaking convergence.
- `OrderedLogisticRegression.ipynb` is a notebook to run ordered logistic regression. It is a simpler model than mixed effect regression because it doesn't model between-rater variability. I used it to gain some understanding about logistic regression and continuation ratio assumption.
- `VisualizeRatings.ipnyb` is a notebook to visualize the distributions of ratings in the defaced vs original conditions. 
- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.

```python

```
