import types
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def bland_altman_plot_i(
    data1,
    data2,
    data_label,
    ax,
    fontsize,
    offsety=0,
    offsetx=1,
    facecolor=(1.0, 1.0, 1.0, 1.0),
):
    """
    Function to plot one Bland-Altman plot given two sets of data
    """
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between data1 and data2
    md = np.mean(diff)  # Mean of the difference
    sd = np.std(diff, axis=0)  # Standard deviation of the difference

    ax.scatter(mean, diff, color="b")
    ax.set_title(data_label, fontsize=fontsize + 2)
    ax.axhline(md, color="gray", linestyle="--")
    ax.axhline(md + 1.96 * sd, color="red", linestyle="--")
    ax.axhline(md - 1.96 * sd, color="red", linestyle="--")
    ax.tick_params(labelsize=fontsize - 2)
    ax.set_facecolor(facecolor)

    # Scientific notation of y-axis
    ax.ticklabel_format(axis="y", style="scientific", scilimits=(-1, 1))

    # Manually offset text for visibility
    ax.yaxis.offsetText.set_fontsize(fontsize - 2)
    ty = ax.yaxis.get_offset_text()
    ty.set_x(offsety)

    # Scientific notation of xaxis
    ax.ticklabel_format(axis="x", style="scientific", scilimits=(-5, 5))

    # Manually offset text for visibility
    ax.xaxis.offsetText.set_fontsize(fontsize - 2)
    pad = plt.rcParams["xtick.major.size"] + plt.rcParams["xtick.major.pad"]

    def bottom_offset(self, bboxes, bboxes2):
        bottom = self.axes.bbox.ymin
        self.offsetText.set(va="top", ha="left")
        oy = bottom - pad * self.figure.dpi / 72.0
        self.offsetText.set_position((1, oy))

    ax.xaxis._update_offset_text_position = types.MethodType(bottom_offset, ax.xaxis)


# Load IQMs
iqms_df = pd.read_csv("IXI_iqms_df.csv")

# Separate IQMs from defaced and nondefaced images in two dataframes
iqms_defaced = iqms_df[iqms_df["defaced"] == 1]
iqms_nondefaced = iqms_df[iqms_df["defaced"] == 0]

# Reorder the dataframes so the subjects' order match
iqms_defaced = iqms_defaced.sort_values("sub")
iqms_nondefaced = iqms_nondefaced.sort_values("sub")

# Reset the index to start from 0
iqms_defaced = iqms_defaced.reset_index(drop=True)
iqms_nondefaced = iqms_nondefaced.reset_index(drop=True)

# Drop non-IQM columns
iqms_defaced = iqms_defaced.drop(
    columns=[
        "bids_name",
        "site",
        "Unnamed: 0",
        "sub",
        "defaced",
    ]
)
iqms_nondefaced = iqms_nondefaced.drop(
    columns=[
        "bids_name",
        "site",
        "Unnamed: 0",
        "sub",
        "defaced",
    ]
)

# Extract number of IQMs
n_iqm = len(iqms_defaced.keys())

# Build figure with subplots
fig, axs = plt.subplots(8, 8, sharex=False, sharey=False, figsize=(45, 45))
fig.suptitle("Bland-Altman Plot", fontsize=36, y=0.91)

# Hide the unpopulated plots
axs[7, 6].set_axis_off()
axs[7, 7].set_axis_off()

# Variables to help tweak the plot manually for readability
offsety = np.zeros((n_iqm, 1))
offsetx = np.ones((n_iqm, 1))
facecolor = [axs[0, 0].get_facecolor() for i in range(n_iqm)]

# Generate one BA plot per IQM
for i, (key, iqm_d) in enumerate(iqms_defaced.items()):

    # Manually shift labels for readability
    if i in [
        27,
        28,
        30,
        31,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        44,
        45,
        47,
        48,
        49,
        50,
        52,
        53,
        54,
        55,
        56,
        58,
        59,
        60,
    ]:
        offsety[i] = -0.15
    if i == 29:
        offsety[i] = -0.20
    if i == 60:
        offsetx[i] = 1.05

    # Manually highlight IQM that seem biased
    if i in [
        2,
    ]:
        facecolor[i] = (1, 1, 0.6, 0.2)

    # BA plot
    iqm_nd = iqms_nondefaced[key]
    bland_altman_plot_i(
        iqm_nd,
        iqm_d,
        key,
        axs[i // 8, i % 8],
        fontsize=22,
        offsety=offsety[i],
        offsetx=offsetx[i],
        facecolor=facecolor[i],
    )

# Figure description

fig.text(
    0.5,
    0.085,
    "Mean of IQM on non-defaced and defaced images",
    fontsize=32,
    ha="center",
)
fig.text(
    0.09,
    0.5,
    "IQM on non-defaced image - IQM on defaced image",
    fontsize=32,
    va="center",
    rotation="vertical",
)

fig.text(
    0.09,
    0.01,
    "Fig.2 Only the entropy-focus criterion (efc) IQM presents a significance bias between the defaced and non-defaced image (highlighted in yellow).\n\
The bias is visualized by the dashed grey line and is computed as the mean of the differences. A bias is considered significant when the 95%\nconfidence interval does \
not contain the zero-difference line. \
The 95% confidence interval is indicated by the dashed red line and is computed as bias±1.96*SD. \
The zero-difference line represents the ideal condition where the IQM value would be identical between the image with and without\nface. \
Additionally, the fact that qi_1, summary_p05, summary_bd_mad, summary_bg_median are problematically almost always 0 is also visible on\n\
this plot. This led us to exclude those IQMs from our analysis.",
    fontsize=34,
    ha="left",
    wrap=True,
    fontweight="bold",
)

# Save figure
plt.savefig("BlandAltman61IQMs.pdf", dpi=200)
