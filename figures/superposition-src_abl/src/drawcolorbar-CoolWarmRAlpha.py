import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# data = np.random.uniform(0,100, [1000,1000])
data = np.array([np.linspace(100,0,101)] * 13).T

# fig = plt.figure(figsize=(1.5,4))
# ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.9])

plt.imshow(data)

coolwarm_r = plt.cm.coolwarm_r

coolwarm_r_alpha_dict = coolwarm_r._segmentdata.copy()

coolwarm_r_alpha_dict['alpha'] = [
    (0.0, 0.0, 0.0),
    (1.0, 1.0, 1.0)
]

coolwarm_r_alpha = LinearSegmentedColormap('coolwarm_r_alpha', coolwarm_r_alpha_dict)
plt.register_cmap(cmap=coolwarm_r_alpha)


# cmap = sns.plt.cm.coolwarm_r
# norm = sns.mpl.colors.Normalize(vmin=0, vmax=100)
# fig = sns.plt.figure(figsize=(1.5,4))
# ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.9])
# cb = sns.mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm)
# cb.ax.tick_params(labelsize=20)
# cb.set_label('sequence identity (%)', fontsize=27.)
# cbar = plt.colorbar()
plt.set_cmap('coolwarm_r_alpha')
# cbar.solids.set_edgecolor('face')

ax1 = plt.gca()
ax1.set_xticks([])
# yticklocs, yticklabels = plt.yticks()
yticklocs = np.array([0.,   20.,   40.,   60.,   80.,  100.])
yticklabels = ['100', '80', '60', '40', '20', '0']
plt.yticks(yticklocs, yticklabels)
ax1.yaxis.tick_right()
plt.setp(ax1.get_yticklabels(), fontsize=28.)

plt.ylabel('sequence identity (%)', fontsize=28.)
ax1.yaxis.set_label_position('right')

# plt.colorbar()

plt.savefig('colorbar-CoolWarmRAlpha.png', dpi=300)
