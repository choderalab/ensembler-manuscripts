import os
import ensembler
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

seqid_mins = np.arange(0., 100., 20.)
seqid_maxs = np.arange(20., 101., 20.)
seqid_ranges = zip(seqid_mins, seqid_maxs)

seqid_maxs[-1] = 101.

sns.set(style="white")

# palette = sns.blend_palette([sns.desaturate('royalblue', 0), 'royalblue'], 5)
palette = sns.color_palette('GnBu_d', n_colors=5)[::-1]

sns.kdeplot(df_has_model.rmsd*10, label='0-100 ($n=$%d)' % len(df_has_model), color='red', bw=02.5)

for i, seqid_range in enumerate(seqid_ranges):
    df_seqid_bin = df_has_model[df_has_model.seqid >= seqid_range[0]][df_has_model.seqid < seqid_range[1]]
    print seqid_range, len(df_seqid_bin)
    label = '%.0f-%.0f ($n=$%d)' % (seqid_range[0], seqid_range[1], len(df_seqid_bin))

    # sns.distplot(df_seqid_bin.rmsd, label=labels[i], hist=False)
    sns.kdeplot(df_seqid_bin.rmsd*10, label=label, color=palette[i], bw=2.5)

    # if i == 4:
    #     sns.rugplot(df_seqid_bin.rmsd*10, color=palette[i])

    # hgram = histogram(df_seqid_bin.rmsd, bins=np.arange(0.,6.,0.5), density=True)
    # x = hgram[1][:-1] + ((hgram[1][1] - hgram[1][0])/2.)
    # plot(x, hgram[0], label=seqid_range[0], color=colors[i])

ax = plt.gca()
plt.setp(ax, yticks=[])

plt.legend(title='Sequence identity (%)')
plt.xlim(0,40)
plt.xlabel('RMSD ($\AA$)')
sns.despine(left=True)
plt.savefig('rmsddist.png')

plt.close()

# Plot sequence identity distribution

fig, ax1 = plt.subplots()

palette = sns.color_palette('deep', 2)

sns.set(style="white")
sns.kdeplot(df_has_model.seqid, bw=1., ax=ax1, color=palette[0])
ax1.set_ylabel('probability density', color=palette[0])
ax1.legend_.remove()
ax1.set_xlabel('sequence identity (%)')
ax2 = ax1.twinx()
sns.kdeplot(df_has_model.seqid, bw=1., cumulative=True, ax=ax2, color=palette[1])
ax2.set_ylabel('cumulative probability density', color=palette[1])
ax2.legend_.remove()
# sns.despine(left=True)
# plt.setp(plt.gca(), yticks=[])
plt.xlim(0,100)
plt.savefig('seqid_dist.png')
