import os
import shutil
import tempfile
import numpy as np
import pandas as pd
import mdtraj
import seaborn as sns

srcdir = '../../../data/models/SRC_HUMAN_D0'

df = pd.read_csv(os.path.join(srcdir, 'traj-refine_implicit_md-data.csv'))

traj = mdtraj.load(os.path.join(srcdir, 'traj-refine_implicit_md.xtc'), top=os.path.join(srcdir, 'traj-refine_implicit_md-topol.pdb'))

inactive_structure = mdtraj.load('2SRC.pdb')
active_structure = mdtraj.load('1Y57.pdb')

# K295 = 29
# E310 = 44
# R409 = 143
residue_labels = ['K295', 'E310', 'R409']
# traj_resids = [29, 44, 143]
# ref_structure_residue_ids = [295, 310, 409]
traj_residue_selections = [
    'residue 29 and (name NZ or name CD or name CE)',
    'residue 44 and (name "OE1" or name CD or name "OE2")',
    'residue 143 and (name "NH1" or name CZ or name "NH2")',
]
traj_residue_indices = [28, 43, 142]   # 0-based
ref_residue_selections = [
    'residue 295 and (name NZ or name CD or name CE)',
    'residue 310 and (name "OE1" or name CD or name "OE2")',
    'residue 409 and (name "NH1" or name CZ or name "NH2")',
]
inactive_structure_residue_indices = [211, 226, 325]   # 0-based
active_structure_residue_indices = [213, 228, 327]   # 0-based

traj_residue_pair_indices = np.array([[28, 43], [43, 142]])
inactive_structure_residue_pair_indices = np.array([[211, 226], [226, 325]])
active_structure_residue_pair_indices = np.array([[213, 228], [228, 327]])


pairs = [('K295', 'E310'), ('E310', 'R409')]

pairs_dict = {pair: {'indices_traj': traj_residue_pair_indices[x]} for x, pair in enumerate(pairs)}

contacts = mdtraj.compute_contacts(traj, contacts=traj_residue_pair_indices)[0].T

inactive_structure_contacts = mdtraj.compute_contacts(inactive_structure, contacts=inactive_structure_residue_pair_indices)[0].T
active_structure_contacts = mdtraj.compute_contacts(active_structure, contacts=active_structure_residue_pair_indices)[0].T


# plot

seqids = df.seqid

# ax_models = sns.plt.scatter(pairs_dict[pairs[0]]['distances'][::-1], pairs_dict[pairs[1]]['distances'][::-1], c=seqids[::-1], cmap=sns.plt.cm.coolwarm_r, marker='o', alpha=0.7, vmin=0, vmax=100)
ax_models = sns.plt.scatter(contacts[0][::-1], contacts[1][::-1], c=seqids[::-1], cmap=sns.plt.cm.coolwarm_r, marker='o', alpha=0.7, vmin=0, vmax=100)
cb = sns.plt.colorbar(ax_models, label='sequence identity (%)')
cb.solids.set_edgecolor("face")   # makes sure colorbar is smooth

sns.plt.scatter(active_structure_contacts[0], active_structure_contacts[1], facecolor='g', marker='*', s=200., linewidth=1., label='1Y57 (SRC, active)')
sns.plt.scatter(inactive_structure_contacts[0], inactive_structure_contacts[1], facecolor='r', marker='*', s=200., linewidth=1., label='2SRC (SRC, inactive)')

sns.plt.xlabel('-'.join(pairs[0]) + ' (nm)')
sns.plt.ylabel('-'.join(pairs[1]) + ' (nm)')
sns.plt.legend()
sns.plt.xlim(0,5)
sns.plt.ylim(0,5)
sns.plt.axes().set_aspect('equal')

sns.plt.savefig('distances.png')
