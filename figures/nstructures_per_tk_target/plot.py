import pandas as pd
import seaborn as sns

tks = open('../../data/TKs.txt').read().splitlines()

df = pd.read_csv('../../data/templates_general_data/templates-data.csv')

template_ids = list(df['Ensembler template id'])

template_target_ids = ['_'.join(template_id.split('_')[0:3]) for template_id in template_ids]

counts = [0] * len(tks)

for t, tk in enumerate(tks):
    counts[t] += template_target_ids.count(tk)

data = zip(tks, counts)
data = sorted(data, key=lambda x: x[1], reverse=True)

tks, counts = zip(*data)
tks = ['{} {}'.format(tk.split('_')[0], tk[-1]) for tk in tks]

# ===
# plot
# ===

sns.set_context('paper', font_scale=1)
sns.set_style('whitegrid')
ax1 = sns.barplot(x=tks, y=counts, color='gray')

ax1.grid(False)

for label in ax1.get_xticklabels():
    label.set_fontsize(5)
    label.set_rotation(90)

sns.plt.tight_layout()

sns.plt.savefig('nstructures_per_tk_target.pdf')
