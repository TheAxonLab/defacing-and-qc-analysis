
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from mriqc_learn.models.preprocess import SiteRobustScaler
from mriqc_learn.viz import metrics


repo_root = Path(__file__).parents[2]
"""Repository's root path."""

out_path = repo_root / "outputs" / "IQMs"
"""Output folder."""

out_path.mkdir(parents=True, exist_ok=True)

iqms_df = pd.read_csv(repo_root / "data" / "S2_Data.csv")
print(iqms_df.columns)
iqms_df = iqms_df.drop(columns=["sub","bids_name","defaced","qi_1", "summary_bg_p05", "summary_bg_mad", "summary_bg_median", "fber"])

# Harmonize between sites
scaled_iqms = SiteRobustScaler(unit_variance=True, groupby="site").fit_transform(iqms_df)
print(scaled_iqms.shape)

img, cbar = metrics.plot_corrmat(scaled_iqms.drop(columns="site").corr(), figsize=(14,14), sorted=True)
plt.savefig(out_path / 'S14_figure.png')

