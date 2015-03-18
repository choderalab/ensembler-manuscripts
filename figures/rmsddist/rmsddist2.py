import os
import ensembler
from copy import deepcopy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data_dir = os.path.join('..', '..', 'data')
targets = open(os.path.join(data_dir, 'TKs.txt')).read().splitlines()

models_target_dir = os.path.join(data_dir, 'models', targets[0])
rmsds_filepath = os.path.join(models_target_dir, 'rmsds.csv')
combined_dfs = pd.read_csv(rmsds_filepath, index_col=0)

for target in targets[1:]:
    models_target_dir = os.path.join(data_dir, 'models', target)
    rmsds_filepath = os.path.join(models_target_dir, 'rmsds.csv')
    combined_dfs = pd.concat([combined_dfs, pd.read_csv(rmsds_filepath, index_col=0)]).reset_index(drop=True)

df_has_model = combined_dfs[combined_dfs.has_model]

# seqid_mins = np.arange(0., 100., 100./3.)
# seqid_maxs = np.arange(100./3., 101., 100./3.)
# seqid_ranges = zip(seqid_mins, seqid_maxs)
seqid_ranges = [
    [0., 35.],
    [35., 55.],
    [55., 100.],
]

seqid_ranges_labels = deepcopy(seqid_ranges)

seqid_ranges[-1][-1] = 101.

# ========
# Plotting
# ========

sns.set_context('paper', font_scale=1.)
sns.set_style('white')
fig = sns.plt.figure(figsize=(3.5,2.625))

# palette = sns.blend_palette([sns.desaturate('royalblue', 0), 'royalblue'], 5)
palette = sns.color_palette('GnBu_d', n_colors=3)[::-1]

# sns.kdeplot(df_has_model.rmsd*10, label='0-100 ($n=$%d)' % len(df_has_model), color='red', bw=02.5)

for i, seqid_range in enumerate(seqid_ranges):
    df_seqid_bin = df_has_model[df_has_model.seqid >= seqid_range[0]][df_has_model.seqid < seqid_range[1]]
    print seqid_range, len(df_seqid_bin)
    label = '%.0f-%.0f ($n=$%d)' % (seqid_ranges_labels[i][0], seqid_ranges_labels[i][1], len(df_seqid_bin))

    # sns.distplot(df_seqid_bin.rmsd, label=labels[i], hist=False)
    sns.kdeplot(df_seqid_bin.rmsd*10, label=label, color=palette[i], bw=2.5, shade=True)

    # if i == 4:
    #     sns.rugplot(df_seqid_bin.rmsd*10, color=palette[i])

    # hgram = histogram(df_seqid_bin.rmsd, bins=np.arange(0.,6.,0.5), density=True)
    # x = hgram[1][:-1] + ((hgram[1][1] - hgram[1][0])/2.)
    # plot(x, hgram[0], label=seqid_range[0], color=colors[i])

ax = plt.gca()
plt.setp(ax, yticks=[])

legend = plt.legend(title='Sequence identity (%)', fontsize='xx-small')
plt.setp(legend.get_title(),fontsize='x-small')
plt.xlim(0,40)
plt.xlabel('RMSD ($\AA$)')
sns.despine(left=True)

plt.tight_layout()

plt.savefig('rmsddist2.png', dpi=300)

plt.close()

# Plot sequence identity distribution

# sns.set(style="white")
# sns.kdeplot(df_has_model.seqid)
# sns.despine(left=True)
# plt.setp(plt.gca(), yticks=[])
# plt.xlim(0,102)
# plt.savefig('seqid_dist.png')
