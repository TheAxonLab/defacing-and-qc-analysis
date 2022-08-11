import random

random.seed(10)
# Select randomly 140 subjects from the IXI dataset
randomlist = random.sample(range(1, 580), 140)
# Randomly select 130 subjects to use for the analysis 
subset = random.sample(randomlist, 130)
# Keep aside the 10 leftover subjects as replacements if any of 
# the 130 is excluded on the basis of failed reconstruction
subset_backup = [idx for idx in randomlist if idx not in subset]

# Randomly select 20 subjects that will be shown twice
subset_rep = random.sample(subset, 20)