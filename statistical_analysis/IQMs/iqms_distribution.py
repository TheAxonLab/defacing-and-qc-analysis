from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


repo_root = Path(__file__).parents[2]
"""Repository's root path."""

out_path = repo_root / "outputs" / "IQMs"
"""Output folder."""

out_path.mkdir(parents=True, exist_ok=True)


def iqm_dist(
    data,
    data_label,
    ax,
    fontsize,
    bins=50,
    facecolor=(1.0, 1.0, 1.0, 1.0),
):
    """
    Function to plot one IQM distribution
    """
    
    sns.histplot(data, kde=False, ax=ax, stat='probability', bins=bins)

    ax.set_title(data_label, fontsize=fontsize + 2)
    ax.tick_params(labelsize=fontsize - 2)
    ax.set_facecolor(facecolor)
    # Turn off individual x-labels and y-labels
    ax.set_xlabel('')
    ax.set_ylabel('')

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Scientific notation of y-axis
    # ax.ticklabel_format(axis="y", style="scientific", scilimits=(-1, 1))

    # # Manually offset text for visibility
    # ax.yaxis.offsetText.set_fontsize(fontsize - 2)
    # ty = ax.yaxis.get_offset_text()
    # ty.set_x(offsety)

    # # Scientific notation of xaxis
    # ax.ticklabel_format(axis="x", style="scientific", scilimits=(-5, 5))
    # ax.xaxis.offsetText.set_fontsize(fontsize - 2)

# Load IQMs
iqms_df = pd.read_csv(repo_root / "data" / "S2_Data.csv")

# Drop non-IQM columns
iqms_df = iqms_df.drop(
    columns=[
        "bids_name",
        "site",
        "sub",
        "defaced",
    ]
)

# Extract number of IQMs
n_iqm = len(iqms_df.keys())

# Build figure with subplots
fig, axs = plt.subplots(8, 8, sharex=False, sharey=False, figsize=(45, 45))
# fig.suptitle("Histogram", fontsize=36, y=0.91)

# Hide the unpopulated plots
axs[7, 6].set_axis_off()
axs[7, 7].set_axis_off()

# Variables to help tweak the plot manually for readability
offsety = np.zeros((n_iqm, 1))
offsetx = np.ones((n_iqm, 1))
facecolor = [axs[0, 0].get_facecolor() for i in range(n_iqm)]

# Generate one BA plot per IQM
for i, (key, iqm) in enumerate(iqms_df.items()):

    # Manually shift labels for readability
    if i in [
        27,
        28,
        30,
        31,
        32,
        33,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        43,
        44,
        45,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        62,
        63,
    ]:
        offsety[i] = -0.15
    if i == 29:
        offsety[i] = -0.20

    # Manually highlight IQM that seem biased
    if i in [
        13,27,29,31
    ]:
        facecolor[i] = (1.0, 0.5, 0.5, 0.5)

    # Plot distributions
    iqm_dist(
        iqm,
        key,
        ax = axs[i // 8, i % 8],
        fontsize=22,
        # offsety=offsety[i],
        facecolor=facecolor[i],
    )

# Save figure
plt.savefig(out_path / "S12_figure.png", dpi=200, bbox_inches='tight')
