import seaborn as sns

# draw colorbar
cmap = sns.plt.cm.coolwarm_r
norm = sns.mpl.colors.Normalize(vmin=0, vmax=100)
fig = sns.plt.figure(figsize=(1.5,4))
ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.9])
cb = sns.mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm)
cb.ax.tick_params(labelsize=20)
cb.set_label('sequence identity (%)', fontsize=27.)
sns.plt.savefig('colorbar.png', dpi=300)
