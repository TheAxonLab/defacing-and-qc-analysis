# Code corresponding to finalized Registered Report: 'Removing facial features from structural MRI images biases visual quality assessment'

A critical step before data-sharing of human neuroimaging is removing facial features to protect individuals' privacy. However, not only does this process redact identifiable information about individuals, but it also removes non-identifiable information. This introduces undesired variability into downstream analysis and interpretation. This registered report investigated the degree to which the so-called defacing altered the quality assessment of T1-weighted images of the human brain from the openly available &ldquo;IXI dataset&rdquo;. The effect of defacing on manual quality assessment was investigated on a single-site subset of the dataset (N=185). By comparing two linear mixed-effects models, we determined that four trained human raters' perception of quality was significantly influenced by defacing by modeling their ratings on the same set of images in two conditions: &ldquo;nondefaced&rdquo; (i.e., preserving facial features) and &ldquo;defaced&rdquo;. In addition, we investigated these biases on automated quality assessments by applying repeated-measures, multivariate ANOVA (rm-MANOVA) on the image quality metrics extracted with MRIQC on the full IXI dataset (N=581; three acquisition sites). This study found that defacing altered the quality assessments by humans and showed that MRIQC's quality metrics were mostly insensitive to defacing.

## Contents

- `data/` contains the input data.
- `outputs/` contains the output data tables and figures.
- `pilot_study/` contains data, code and plots associated to the pilot study (doi:[10.31219/osf.io/t9ehk](https://doi.org/10.31219/osf.io/t9ehk)).
- `processing/` contains the code of the processing pipeline.
- `analyses` contains code to run statistical analyses. The folder is separated in two subfolders: the analysis of the IQMs computed automatically by MRIQC and the analysis of the quality scores assigned manually by raters that inspected the MRIQC visual report.


