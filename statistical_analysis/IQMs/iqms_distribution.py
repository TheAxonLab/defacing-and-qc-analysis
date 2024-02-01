import types
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def iqm_dist(
    data,
    data_label,
    ax,
    fontsize,
    offsety=0,
    offsetx=1,
    facecolor=(1.0, 1.0, 1.0, 1.0),
):
    """
    Function to plot one IQM distribution
    """
    
    sns.histplot(iqm, kde=False, bins=15, ax=ax)

    ax.set_title(data_label, fontsize=fontsize + 2)
    ax.tick_params(labelsize=fontsize - 2)
    ax.set_facecolor(facecolor)
    # Turn off individual x-labels and y-labels
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Scientific notation of y-axis
    ax.ticklabel_format(axis="y", style="scientific", scilimits=(-1, 1))

    # Manually offset text for visibility
    ax.yaxis.offsetText.set_fontsize(fontsize - 2)
    ty = ax.yaxis.get_offset_text()
    ty.set_x(offsety)

    # Scientific notation of xaxis
    ax.ticklabel_format(axis="x", style="scientific", scilimits=(-5, 5))
    ax.xaxis.offsetText.set_fontsize(fontsize - 2)

# Load IQMs
iqms_df = pd.read_csv("IXI_iqms_df.csv")

# Drop non-IQM columns
iqms_df = iqms_df.drop(
    columns=[
        "bids_name",
        "site",
        "Unnamed: 0",
        "sub",
        "defaced",
    ]
)

# Extract number of IQMs
n_iqm = len(iqms_df.keys())

# Build figure with subplots
fig, axs = plt.subplots(8, 8, sharex=False, sharey=False, figsize=(45, 45))
fig.suptitle("Histogram", fontsize=36, y=0.91)

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
        offsety=offsety[i],
        facecolor=facecolor[i],
    )

# Figure description

fig.text(
    0.5,
    0.085,
    "Image Quality Metrics (IQM) value",
    fontsize=32,
    ha="center",
)
fig.text(
    0.09,
    0.5,
    "Count",
    fontsize=32,
    va="center",
    rotation="vertical",
)

fig.text(
    0.09,
    0.03,
    "Figure S1. Distribution of the IQMs. The IQMs calculated from both defaced and non-defaced images were pooled together to draw the distributions.\n\
This plot shows that qi_1, summary_bg_p05 are problematically always zero, while summary_bg_mad, summary_bg_median are always 0 except for\n\
two images which correspond to the defaced and non-defaced image of the same subject. These observation led us to exclude those IQMs from our\n\
analysis. Further investigation is needed to understand why these IQMs seem to be erroneously computed.",
    fontsize=34,
    ha="left",
    wrap=True,
    fontweight="bold",
)

# Save figure
plt.savefig("IQMs_distribution.png", dpi=200)
