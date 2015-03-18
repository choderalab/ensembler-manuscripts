import os
import ensembler
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import lines

# ====================
# Data
# ====================

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

# ====================
# Plotting
# ====================

sns.set_context('paper', font_scale=1.)
sns.set_style('white')
fig = sns.plt.figure(figsize=(3.5,2.625))

ax1 = sns.plt.axes()

palette = sns.color_palette('deep', 2)

sns.kdeplot(df_has_model.seqid, bw=1., ax=ax1, color='black', shade=True)
# ax1.set_ylabel('probability density')
ax1.legend_.remove()
ax1.set_xlabel('sequence identity (%)')
ax1.set_xlim(100,0)
sns.plt.setp(ax1, yticks=[])

ax2 = ax1.twinx().twiny()
sns.kdeplot(100.-df_has_model.seqid[::100], bw=1., cumulative=True, ax=ax2, color='black', linestyle='--')
ax2.set_ylabel('CDF')
ax2.legend_.remove()

ax2.set_xlim(0,100)
sns.plt.setp(ax2, xticks=[])

ax2.text(-3.5, 0.45, 'probability density', rotation='vertical', ha='center', va='center', fontsize='x-small')
ax2.text(112.0, 0.45, 'CDF', rotation='vertical', ha='center', va='center', fontsize='x-small')
x1  = [-3.5, -3.5]
y1  = [0.78, 0.88]
line1 = lines.Line2D(x1, y1, color='k')
line1.set_clip_on(False)
x2  = [111.2, 111.2]
y2  = [0.54, 0.69]
line2 = lines.Line2D(x2, y2, color='k', linestyle='--')
line2.set_clip_on(False)
ax2.add_line(line1)
ax2.add_line(line2)

sns.plt.tight_layout()
sns.plt.savefig('seqid_dist.pdf')
# sns.plt.savefig('seqid_dist.png', dpi=300)
