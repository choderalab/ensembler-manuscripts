import os
import numpy as np
import pandas as pd

targetids = open('../../data/TKs.txt').read().splitlines()

seqid_ranges = ['all', '0-35', '35-55', '55-101']
project_stages = ['templates', 'models', 'unique', 'implicit_refined']

counts = {}
rates = {}

for seqid_range in seqid_ranges:
    if seqid_range == 'all':
        counts_filename = 'counts.csv'
    else:
        counts_filename = 'counts-seqid{0}.csv'.format(seqid_range)

    # print 'Working on target', targetids[0]
    counts_path = os.path.join('../../data/models', targetids[0], counts_filename)
    df = pd.read_csv(counts_path)

    for targetid in targetids[1:]:
        # print 'Working on target', targetid
        counts_path = os.path.join('../../data/models', targetid, counts_filename)
        new_df = pd.read_csv(counts_path)
        df += new_df

    counts[seqid_range] = [
        df.templates.values[0],
        df.models.values[0],
        df.unique_models.values[0],
        df.implicit_refined.values[0],
    ]

    rates[seqid_range] = [
        1.0,
        counts[seqid_range][1] / np.float64(counts[seqid_range][0]),
        counts[seqid_range][2] / np.float64(counts[seqid_range][1]),
        counts[seqid_range][3] / np.float64(counts[seqid_range][2]),
    ]

counts = pd.DataFrame(counts, index=project_stages, columns=seqid_ranges)
counts.to_csv('counts.csv')
print counts.to_string()

rates = pd.DataFrame(rates, index=project_stages, columns=seqid_ranges)
rates.to_csv('rates.csv')
print rates.to_string(float_format='{:.3f}'.format)
