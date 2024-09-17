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
    md = np.mean(diff)                   # Mean of the difference
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

def bland_altman_plot_pc(pc_df, savename, nrow):
    ## Bland-Altman plot for principal components

    # Separate PCs from defaced and nondefaced images in two dataframes
    pc_defaced = pc_df[pc_df["defaced"] == 1]
    pc_nondefaced = pc_df[pc_df["defaced"] == 0]

    # Reorder the dataframes so the subjects' order match
    pc_defaced = pc_defaced.sort_values("sub")
    pc_nondefaced = pc_nondefaced.sort_values("sub")

    # Reset the index to start from 0
    pc_defaced = pc_defaced.reset_index(drop=True)
    pc_nondefaced = pc_nondefaced.reset_index(drop=True)

    # Drop non-PCs columns
    pc_defaced = pc_defaced.drop(
        columns=[
            "site",
            "Unnamed: 0",
            "sub",
            "defaced",
        ]
    )
    pc_nondefaced = pc_nondefaced.drop(
        columns=[
            "site",
            "Unnamed: 0",
            "sub",
            "defaced",
        ]
    )

    # Build figure with subplots
    fig, axs = plt.subplots(nrow, 3, sharex=False, sharey=False, figsize=(45, 45))
    fig.suptitle("Bland-Altman Plot", fontsize=36, y=0.91)

    # Generate one BA plot per PC
    for i, (key, pc_d) in enumerate(pc_defaced.items()):

        # BA plot
        pc_nd = pc_nondefaced[key]
        bland_altman_plot_i(
            pc_nd,
            pc_d,
            key,
            axs[i // 3, i % 3],
            fontsize=32,
        )

    # Figure description

    fig.text(
        0.5,
        0.07,
        "Mean of principal component on non-defaced and defaced images",
        fontsize=38,
        ha="center",
    )
    fig.text(
        0.07,
        0.5,
        "PC on non-defaced image - PC on defaced image",
        fontsize=38,
        va="center",
        rotation="vertical",
    )

    # Save figure
    plt.savefig(savename, dpi=200)

## Bland-Altman plot for IQMs
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
        "qi_1",
        "summary_bg_p05",
        "summary_bg_mad",
        "summary_bg_median",
    ]
)
iqms_nondefaced = iqms_nondefaced.drop(
    columns=[
        "bids_name",
        "site",
        "Unnamed: 0",
        "sub",
        "defaced",
        "qi_1",
        "summary_bg_p05",
        "summary_bg_mad",
        "summary_bg_median",
    ]
)

# Extract number of IQMs
n_iqm = len(iqms_defaced.keys())

# Build figure with subplots
fig, axs = plt.subplots(8, 8, sharex=False, sharey=False, figsize=(45, 45))
fig.suptitle("Bland-Altman Plot for IQMs", fontsize=36, y=0.91)
axs[7, 2].set_axis_off()
axs[7, 3].set_axis_off()
axs[7, 4].set_axis_off()
axs[7, 5].set_axis_off()
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
        25,
        26,
        32,
        33,
        34,
        35,
        36,
        37,
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
        50,
        51,
        52,
        53,
        54,
        55,
        56,
    ]:
        offsety[i] = -0.15
    if i == 29:
        offsety[i] = -0.18
    if i in [30, 31]:
        offsety[i] = -0.15
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
    "Figure S2. Bland-Altman plots for all non-excluded IQMs. Only the entropy-focus criterion (efc) IQM presents a significant bias between the defaced and non-defaced image (highlighted in yellow).\n\
The bias is visualized by the dashed grey line and is computed as the mean of the differences. A bias is considered significant when the 95%\nconfidence interval does \
not contain the zero-difference line. \
The 95% confidence interval is indicated by the dashed red line and is computed as bias±1.96*SD. \
The zero-difference line represents the ideal condition where the IQM value would be identical between the image with and without\nface.",
    fontsize=34,
    ha="left",
    wrap=True,
    fontweight="bold",
)

# Save figure
plt.savefig("BlandAltman58IQMs.png", dpi=200)

## Bland-Altman plot for principal components

# Load principal components (PCs)
pc_df = pd.read_csv("IXI_projected_iqms_df_1std_1pca.csv")
bland_altman_plot_pc(pc_df, "BlandAltmanPC_1std_1pca.png", 3)


pc_df = pd.read_csv("IXI_projected_iqms_df_std_site_1pca.csv")
bland_altman_plot_pc(pc_df, "BlandAltmanPC_std_site_1pca.png", 3)

pc_df = pd.read_csv("IXI_projected_iqms_df_std_pca_site.csv")
bland_altman_plot_pc(pc_df, "BlandAltmanPC_std_pca_site.png", 4)
