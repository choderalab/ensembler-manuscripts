import os
import ensembler
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import lines

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

# Plot sequence identity distribution

sns.set(style="white")
fig, ax1 = plt.subplots()

palette = sns.color_palette('deep', 2)

sns.kdeplot(df_has_model.seqid, bw=1., ax=ax1, color='black', shade=True)
# ax1.set_ylabel('probability density')
ax1.legend_.remove()
ax1.set_xlabel('sequence identity (%)')
ax1.set_xlim(100,0)
plt.setp(ax1, yticks=[])

ax2 = ax1.twinx().twiny()
sns.kdeplot(100.-df_has_model.seqid[::100], bw=1., cumulative=True, ax=ax2, color='black', linestyle='--')
ax2.set_ylabel('CDF')
ax2.legend_.remove()

ax2.set_xlim(0,100)
plt.setp(ax2, xticks=[])

x1  = [-3.0, -3.0]
y1  = [0.68, 0.78]
line1 = lines.Line2D(x1, y1, color='k')
line1.set_clip_on(False)
x2  = [107.0, 107.0]
y2  = [0.57, 0.67]
line2 = lines.Line2D(x2, y2, color='k', linestyle='--')
line2.set_clip_on(False)
ax2.add_line(line1)
ax2.add_line(line2)
ax2.text(-3., 0.5, 'probability density', rotation='vertical', ha='center', va='center')
ax2.text(107.5, 0.5, 'CDF', rotation='vertical', ha='center', va='center')

# plt.tight_layout()
plt.savefig('seqid_dist.png')
