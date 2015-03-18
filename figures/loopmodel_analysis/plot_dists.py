import pandas as pd
import seaborn as sns

df = pd.read_csv('loopmodel_data.csv')

successful = df[df.no_missing_residues == False][df.successful == True]
unsuccessful = df[df.no_missing_residues == False][df.successful == False]

# ====
# plot
# ====

sns.set_context('paper', font_scale=1)
sns.plt.figure(figsize=(3.5, 2.625))

sns.distplot(successful.nmissing_resis, hist=False, kde=True, rug=True, label='successful',
    rug_kws={'height': 0.002},
)
sns.distplot(unsuccessful.nmissing_resis, hist=False, kde=True, rug=True, label='unsuccessful', color='red',
    # kde_kws={'bw': 2.5},
    rug_kws={'height': 0.001},
)

# sns.violinplot([successful.nmissing_resis, unsuccessful.nmissing_resis], inner='points',
#     inner_kws={'markersize': 5, 'marker': 'o'},
#     alpha=0.5,
# )
# sns.violinplot([successful.nmissing_resis, unsuccessful.nmissing_resis], inner='stick',
#     inner_kws={'width': 5},
#     alpha=0.5,
# )

ax = sns.plt.gca()
sns.plt.setp(ax, yticks=[])
sns.plt.xlim(0,120)
sns.plt.xlabel('Number of missing residues')

sns.plt.tight_layout()

sns.plt.savefig('nmissing_resis_distributions.png', dpi=300)
