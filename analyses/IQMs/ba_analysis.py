from pathlib import Path
import types
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bootstrap

# Output files' naming
OUTPUT_FIGURE_BASE = 15
OUTPUT_DATA_BASE = 7

COLUMN_DESCRIPTIONS = {
    "metric": "Name of the IQM or PC",
    "n": "Sample size",
    "bias": "Mean difference between nondefaced and defaced images",
    "loa_lower": "Lower limit of agreement (mean difference - 1.96 * standard deviation)",
    "loa_upper": "Upper limit of agreement (mean difference + 1.96 * standard deviation)",
    "ci_lower_param": "Lower bound of the parametric 95% confidence interval of the mean difference",
    "ci_upper_param": "Upper bound of the parametric 95% confidence interval of the mean difference",
    "ci_lower_non_param": "Lower bound of the non-parametric 95% confidence interval of the mean difference",
    "ci_upper_non_param": "Upper bound of the non-parametric 95% confidence interval of the mean difference",
}

repo_root = Path(__file__).parents[2]
"""Repository's root path."""

out_path = repo_root / "outputs" / "IQMs"
"""Output folder."""

out_path.mkdir(parents=True, exist_ok=True)


def bland_altman_plot_i(
    data1, data2, data_label, ax, fontsize, offsety=0, offsetx=1, plot_CI=False
):
    """
    Function to plot one Bland-Altman plot given two sets of data
    """

    sample_n = len(data1)
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between data1 and data2
    md = np.mean(diff)  # Mean of the difference
    sd = np.std(diff, axis=0)  # Standard deviation of the difference
    loa_upper = md + 1.96 * sd  # 95% limits of agreement
    loa_lower = md - 1.96 * sd

    sem = sd / np.sqrt(sample_n)  # Standard error of the mean
    ci_upper = md + 1.96 * sem  # 95% confidence interval
    ci_lower = md - 1.96 * sem

    ## Compute the non-parametric 95% confidence interval
    day = 220830
    time = 543417
    boot_results = bootstrap(
        (diff,),
        np.mean,
        n_resamples=10000,
        method="percentile",
        random_state=day + time,
    )
    ci_diff = boot_results.confidence_interval
    ci_lower_non_param = ci_diff.low
    ci_upper_non_param = ci_diff.high

    # Yellow background if the limit of agreement does not contain zero
    facecolor = (1.0, 1.0, 1.0, 1.0)
    if not (loa_lower <= 0 <= loa_upper):
        facecolor = (1, 1, 0.6, 0.2)

    if not (ci_lower <= 0 <= ci_upper) and not (
        ci_lower_non_param <= 0 <= ci_upper_non_param
    ):
        data_label += "*"

    ax.scatter(mean, diff, color="b")
    ax.set_title(data_label, fontsize=fontsize + 2)
    ax.axhline(md, color="gray", linestyle="-")
    ax.axhline(loa_upper, color="red", linestyle="--")
    ax.axhline(loa_lower, color="red", linestyle="--")
    if plot_CI:
        ax.axhline(ci_upper, color="blue", linestyle="--")
        ax.axhline(ci_lower, color="blue", linestyle="--")
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

    return (
        sample_n,
        md,
        loa_lower,
        loa_upper,
        ci_lower,
        ci_upper,
        ci_lower_non_param,
        ci_upper_non_param,
    )


def bland_altman_plot_pc(pc_df, savename, nrow, plot_CI=False):
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

    # List to aggregate bias-related statistics for each PC
    stats_pc = []

    # Generate one BA plot per PC
    for i, (key, pc_d) in enumerate(pc_defaced.items()):
        # BA plot
        pc_nd = pc_nondefaced[key]
        (
            sample_n,
            md,
            loa_lower,
            loa_upper,
            ci_lower,
            ci_upper,
            ci_lower_non_param,
            ci_upper_non_param,
        ) = bland_altman_plot_i(
            pc_nd, pc_d, key, axs[i // 3, i % 3], fontsize=32, plot_CI=plot_CI
        )
        assert loa_lower <= md <= loa_upper
        assert ci_lower <= md <= ci_upper
        assert ci_lower_non_param <= md <= ci_upper_non_param

        stats_pc.append(
            {
                "metric": key,
                "n": sample_n,
                "bias": md,
                "loa_lower": loa_lower,
                "loa_upper": loa_upper,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "ci_lower_non_param": ci_lower_non_param,
                "ci_upper_non_param": ci_upper_non_param,
            }
        )

    # Figure description

    fig.text(
        0.5,
        0.07,
        "Mean of principal component on nondefaced and defaced images",
        fontsize=38,
        ha="center",
    )
    fig.text(
        0.07,
        0.5,
        "PC on nondefaced image - PC on defaced image",
        fontsize=38,
        va="center",
        rotation="vertical",
    )

    # Save figure
    plt.savefig(savename, dpi=200)

    return stats_pc


## Bland-Altman plot for IQMs
# Load IQMs
iqms_df = pd.read_csv(repo_root / "data" / "S2_Data.csv")

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

# List to gather the statistical estimates namely the bias, 95% CI, and 95% LoA
stats = []

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

    # BA plot
    iqm_nd = iqms_nondefaced[key]
    (
        sample_n,
        md,
        loa_lower,
        loa_upper,
        ci_lower,
        ci_upper,
        ci_lower_non_param,
        ci_upper_non_param,
    ) = bland_altman_plot_i(
        iqm_nd,
        iqm_d,
        key,
        axs[i // 8, i % 8],
        fontsize=22,
        offsety=offsety[i],
        offsetx=offsetx[i],
    )
    assert loa_lower <= md <= loa_upper
    assert ci_lower <= md <= ci_upper
    assert ci_lower_non_param <= md <= ci_upper_non_param

    stats.append(
        {
            "metric": key,
            "n": sample_n,
            "bias": md,
            "loa_lower": loa_lower,
            "loa_upper": loa_upper,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "ci_lower_non_param": ci_lower_non_param,
            "ci_upper_non_param": ci_upper_non_param,
        }
    )

# Convert statistics to dataframe
stats_df = pd.DataFrame(stats)
##  Save statistics
stats_df.to_csv(out_path / f"S{OUTPUT_DATA_BASE}_Data.tsv", index=False, sep="\t")

# Figure description

fig.text(
    0.5,
    0.085,
    "Mean of IQM on nondefaced and defaced images",
    fontsize=32,
    ha="center",
)
fig.text(
    0.09,
    0.5,
    "IQM on nondefaced image - IQM on defaced image",
    fontsize=32,
    va="center",
    rotation="vertical",
)


""" fig.text(
    0.09,
    0.01,
    "Figure S2. Bland-Altman plots for all non-excluded IQMs. Only the entropy-focus criterion (efc) IQM presents a significant bias between the defaced and nondefaced image (highlighted in yellow).\n\
The bias is visualized by the dashed grey line and is computed as the mean of the differences. A bias is considered significant when the 95%\nconfidence interval does \
not contain the zero-difference line. \
The 95% confidence interval is indicated by the dashed red line and is computed as bias±1.96*SD. \
The zero-difference line represents the ideal condition where the IQM value would be identical between the image with and without\nface.",
    fontsize=34,
    ha="left",
    wrap=True,
    fontweight="bold",
) """

# Save figure
plt.savefig(out_path / f"S{OUTPUT_FIGURE_BASE}_figure.png")

## Bland-Altman plot for principal components
nrows = {
    "S3_Data": 3,
    "S4_Data": 3,
    "S5_Data": 4,
}


for i, src_name in enumerate(nrows.keys()):
    pc_df = pd.read_csv(repo_root / "data" / f"{src_name}.csv")
    stats_pc = bland_altman_plot_pc(
        pc_df,
        str(out_path / f"S{i + OUTPUT_FIGURE_BASE + 1}_figure.png"),
        nrows[src_name],
        plot_CI=False,
    )
    stats_pc_df = pd.DataFrame(stats_pc)
    stats_pc_df.to_csv(out_path / f"S{i + OUTPUT_DATA_BASE + 1}_Data.tsv", index=False, sep="\t")

# Create a sidecar JSON to explain the column names inside stats_df
column_descriptions = {k: {"Description": v} for k, v in COLUMN_DESCRIPTIONS.items()}
(out_path / f"S{'+'.join([str(OUTPUT_DATA_BASE + i) for i in range(4)])}_Data.json").write_text(json.dumps(column_descriptions, indent=2))
