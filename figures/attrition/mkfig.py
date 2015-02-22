import pandas as pd
import seaborn as sns

counts = pd.read_csv('counts.csv', index_col=0)
    # 'all': [398970, 382568, 378839, 373513],
    # '0-35': [343393, 333564, 332055, 327250],
    # '35-55': [50643, 44602, 42907, 42431],
    # '55-100': [4934, 4402, 3877, 3832],

print counts

rates = pd.read_csv('rates.csv', index_col=0)
    # 'all': [1.0, 0.95888913953430077, 0.99025271324313591, 0.98594125736790561],
    # '0-35': [1.0, 0.9713768189800025, 0.9954761305176818, 0.98552950565418385],
    # '35-55': [1.0, 0.88071401773196689, 0.96199721985561182, 0.98890623907520914],
    # '55-100': [1.0, 0.89217673287393595, 0.880736029077692, 0.98839308743874132],

seqid_ranges = ['all', '0-35', '35-55', '55-101']
project_stages = ['templates', 'models', 'unique', 'implicit_refined']

ax = rates.plot()

# for seqid_range in seqid_ranges:
#     sns.plt.plot(rates[seqid_range], label=seqid_range)

# sns.plt.legend()

palette = ['k'] + sns.color_palette('GnBu_d', n_colors=3)[::-1]

for i, line in enumerate(ax.lines):
    sns.plt.setp(line, color=palette[i])

sns.plt.legend(loc='best')
sns.plt.ylim(0.85,1)
sns.plt.savefig('attrition_rates.png')
sns.plt.close()

# counts.plot()
# sns.plt.savefig('attrition_counts.png')
