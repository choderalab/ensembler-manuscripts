import os
import ensembler
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import lines
from copy import deepcopy
import matplotlib.pyplot as plt

# ====================
# Data
# ====================

data_dir = os.path.join('..', '..', 'data')
targets = open(os.path.join(data_dir, 'TKs.txt')).read().splitlines()

# Get data from rmsds.csv and validation file, and do left join on templateid

for target in targets:
    models_target_dir = os.path.join(data_dir, 'models', target)

    template_ids = []
    scores = []
    scores_filepath = os.path.join(models_target_dir, 'validation_scores_sorted-molprobity-refine_implicit_md')
    if not os.path.exists(scores_filepath):
        continue
    with open(scores_filepath) as scores_file:
        for line in scores_file.read().splitlines():
            words = line.split(' ')
            if len(words[1]) > 0:
                template_ids.append(words[0])
                scores.append(float(words[1]))
    molprobity_df = pd.DataFrame({'templateid': template_ids, 'molprobity_score': scores})

    rmsds_filepath = os.path.join(models_target_dir, 'rmsds.csv')
    rmsds_df = pd.read_csv(rmsds_filepath, index_col=0)
    target_df = pd.merge(left=rmsds_df, right=molprobity_df, how='inner', left_on='templateid', right_on='templateid')
    try:
        combined_dfs = pd.concat([combined_dfs, target_df]).reset_index(drop=True)
    except:
        combined_dfs = target_df

seqid_ranges = [
    [0., 35.],
    [35., 55.],
    [55., 100.],
]

seqid_ranges_labels = deepcopy(seqid_ranges)

seqid_ranges[-1][-1] = 101.

# ====================
# Plotting
# ====================

sns.set_context('paper', font_scale=1.)
sns.set_style('white')
fig = sns.plt.figure(figsize=(3.5,2.625))

palette = sns.color_palette('GnBu_d', n_colors=3)[::-1]

for i, seqid_range in enumerate(seqid_ranges):
    df_seqid_bin = combined_dfs[combined_dfs.seqid >= seqid_range[0]][combined_dfs.seqid < seqid_range[1]]
    print seqid_range, len(df_seqid_bin)
    label = '%.0f-%.0f ($n=$%d)' % (seqid_ranges_labels[i][0], seqid_ranges_labels[i][1], len(df_seqid_bin))

    sns.kdeplot(df_seqid_bin.molprobity_score, label=label, color=palette[i], shade=True)

ax = plt.gca()
plt.setp(ax, yticks=[])

legend = plt.legend(title='Sequence identity (%)', fontsize='xx-small', loc='upper left')
plt.setp(legend.get_title(),fontsize='x-small')
# plt.xlim(0,30)
plt.xlabel('MolProbity score')
sns.despine(left=True)

plt.tight_layout()

plt.savefig('molprobity_dist.pdf')
plt.savefig('molprobity_dist.png', dpi=300)

plt.close()

# # Plot sequence identity distribution
#
# sns.set(style="white")
# sns.kdeplot(df_has_model.seqid)
# sns.despine(left=True)
# plt.setp(plt.gca(), yticks=[])
# plt.xlim(0,102)
# plt.savefig('seqid_dist.png')

# Plot distribution without stratification

sns.set_context('paper', font_scale=1.)
sns.set_style('white')
fig = sns.plt.figure(figsize=(3.5,2.625))

sns.kdeplot(combined_dfs.molprobity_score, shade=True, color='k')

ax = plt.gca()
plt.setp(ax, yticks=[])

# plt.xlim(0,30)
plt.xlabel('MolProbity score')
sns.despine(left=True)

legend = plt.legend()
legend.set_visible(False)

plt.tight_layout()

plt.savefig('molprobity_dist-joint.png', dpi=300)
plt.savefig('molprobity_dist-joint.pdf')

