## Statistical analysis associated to the defacing pre-registration.

Manual ratings

The reason this folder contains so many notebooks is that we had to rethink our statistical analysis several times before finding one that suits our data configuration. Here is a quick recap of our journey: The manual ratings in our original design were ordinal variables, that is categorical variables with a clear ordering of the categories. Thus we started by considering the continuation ratio model (CRM). To help us build and understand the CRM, we played with the similar but simpler model : ordered logistic regression. The problem however is that the CRM cannot handle missing values, which is part of our design. Thus, we decided to change the design of the future manual ratings collection. The goal was to be able to consider linear mixed effect regression by making the manual ratings more continuous. Yet, we were not able to find a configuration under which the linear mixed effect regression was reliably converging to a non-singular solution, despite playing with all possible parameters (e.g number of raters, number of images rated per rater, dataset size). Thus we finally settled for a repeated measure ANOVA. 

- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.

- `ContinuationRatioModel.ipynb` is the notebook to run continuation ratio model.
- `OrderedLogisticRegression.ipynb` is a notebook to run ordered logistic regression. It is a simpler model than the continuation ratio model because it doesn't model between-rater variability. I used it to gain some understanding about logistic regression and continuation ratio assumption.

- `LinearMixedEffectRegression.ipynb` is the notebook to run linear mixed effect regression. We decided to switch to this model because the implementation of the continuation ratio model is not able to deal with missing values.
- In `VaryDatasetParameters.ipynb` I tried to change all dataset parameters to make the linear mixed effect model defaced + (defaced|rater) converge to a non-singular solution without success.
- `MissingValues.ipynb` is the notebook to investigate the maximum of missing values that can be introduced before breaking convergence.
- `VisualizeRatings.ipnyb` is a notebook to visualize the distributions of ratings in the defaced vs original conditions. 

- `ANOVA.ipynb` is the notebook to run repeated measure ANOVA and check its assumptions.
- In `VaryDatasetParameters_ANOVA.ipynb` I performed a sensitivity analysis to verify how many ratings do we need for the model to detect a significant effect of defacing.
