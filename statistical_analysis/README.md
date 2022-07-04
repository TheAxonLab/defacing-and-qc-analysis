## Statistical analysis associated to the defacing pre-registration.


- `simulate_data.R` is a script to simulate raters manually assigning quality grades to subjects in original and defaced conditions. The simulated data have a positive bias towards defaced ratings.
- `VisualizeRatings.ipnyb` is a notebook to visualize the distributions of ratings in the defaced vs original conditions. 
- `OrderedLogisticRegression.ipynb` is a notebook to run ordered logistic regression. It is a simpler model than mixed effect regression because it doesn't model between-rater variability. I used it to gain some understanding about logistic regression and continuation ratio assumption.
- `MixedEffectRegression.ipynb` is the notebook to run mixed effect regression. This is the final analysis on which inference about the existence of a bias linked to defacing will be based.

