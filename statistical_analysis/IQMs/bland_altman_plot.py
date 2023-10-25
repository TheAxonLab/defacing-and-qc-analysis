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
    md = 0  # np.mean(diff)                   # Mean of the difference
    sd = np.std(diff, axis=0)  # Standard deviation of the difference

    ax.scatter(mean, diff, color="b")
    ax.set_title(data_label, fontsize=fontsize + 2)
    ax.axhline(md, color="gray", linestyle="--")
    ax.axhline(md + 1.96 * sd, color="red", linestyle="--")
    ax.axhline(md - 1.96 * sd, color="red", linestyle="--")
    ax.tick_params(labelsize=fontsize - 2)
    ax.set_facecolor(facecolor)

    # Scientific notation of yaxis
    ax.ticklabel_format(axis="y", style="scientific", scilimits=(-1, 1))
    ax.yaxis.offsetText.set_fontsize(fontsize - 2)
    ty = ax.yaxis.get_offset_text()
    ty.set_x(offsety)
    ax.ticklabel_format(axis="x", style="scientific", scilimits=(-5, 5))
    ax.xaxis.offsetText.set_fontsize(fontsize - 2)
    # Scientific notation of xaxis
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
    columns=["bids_name", "site", "Unnamed: 0", "sub", "defaced"]
)
iqms_nondefaced = iqms_nondefaced.drop(
    columns=["bids_name", "site", "Unnamed: 0", "sub", "defaced"]
)

# Extract number of IQMs
n_iqm = len(iqms_defaced.keys())

# Build figure with subplots
fig, axs = plt.subplots(8, 8, sharex=False, sharey=False, figsize=(45, 45))
fig.suptitle("Bland-Altman Plot", fontsize=36, y=0.91)
axs[7, 5].set_axis_off()
axs[7, 6].set_axis_off()
axs[7, 7].set_axis_off()

# Variables to help tweek the plot manually for readability
offsety = np.zeros((n_iqm, 1))
offsetx = np.ones((n_iqm, 1))
facecolor = [axs[0, 0].get_facecolor() for i in range(n_iqm)]

# Generate one BA plot per IQM
for i, (key, iqm_d) in enumerate(iqms_defaced.items()):

    # Manually shift labels for readability
    if i in [
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        53,
        57,
        58,
        59,
    ]:
        offsety[i] = -0.15
    if i == 29:
        offsety[i] = -0.18
    if i == 52:
        offsety[i] = -0.21
        offsetx[i] = 1.05

    # Manually highlight IQM that seem biased
    if i in [
        0,
        1,
        2,
        7,
        8,
        10,
        11,
        13,
        15,
        16,
        19,
        20,
        21,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        37,
        38,
        41,
        42,
        43,
        44,
        46,
        47,
        48,
        50,
        51,
        55,
        56,
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
        offsetx=[i],
        facecolor=facecolor[i],
    )

# Figure description
fig.text(
    0.5, 0.2, "Mean of IQM on non-defaced and defaced images", fontsize=32, ha="center"
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
    0.03,
    "Fig.2 IQMs vary after defacing. Many of the IQMs are biased by the facial features removal \
(cf plots highlighted in yellow). The grey line on the\nBland-Altman plots lies at 0 and represents the ideal condition\
 where the IQM value would be identical between the image with and without face.\nThis means that if the points are \
concentrated above or below the grey line, the IQM is biased by defacing. The red lines correspond to the 95%\nconfidence\
 interval centered around the zero-difference reference line, specifically 0±1.96*SD.",
    fontsize=34,
    ha="left",
    wrap=True,
    fontweight="bold",
)

# Save figure
plt.savefig("BlandAltman61IQMs.pdf", dpi=200)
