# Three seqid classes (manually chosen). RMSD clustering performed within each class, and centroids picked.
# EDIT: manually included two models made from Abl1 structures with structured N-term helix

import os
import shutil
import tempfile
import random
import numpy as np
import pandas as pd
import mdtraj as md
import msmbuilder.cluster
import seaborn as sns
import matplotlib as mpl

srcdir = '../../../data/models/ABL1_HUMAN_D0'

# draw colorbar
cmap = sns.plt.cm.coolwarm_r
norm = sns.mpl.colors.Normalize(vmin=0, vmax=100)
fig = sns.plt.figure(figsize=(2,8))
ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.9])
cb = sns.mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm)
cb.ax.tick_params(labelsize=25.)
cb.set_label('sequence identity (%)', fontsize=35.)
sns.plt.savefig('colorbar.png')


nmodels_per_class = 3

seqid_classes = [[0., 35.], [35., 55.], [55., 101.]][::-1]

traj = md.load(os.path.join(srcdir, 'traj-refine_implicit_md.xtc'), top=os.path.join(srcdir, 'traj-refine_implicit_md-topol.pdb'))

df = pd.read_csv(os.path.join(srcdir, 'traj-refine_implicit_md-data.csv'))

model_indices = []
seqids = []

for seqid_class in seqid_classes:
    seqid_class_df = df[df.seqid >= seqid_class[0]][df.seqid < seqid_class[1]]
    seqid_class_model_indices = list(seqid_class_df.index)
    seqid_class_traj = traj[seqid_class_model_indices]
    alpha_atom_indices = seqid_class_traj.topology.select_atom_indices('alpha')
    seqid_class_traj_alphas = seqid_class_traj.atom_slice(alpha_atom_indices)

    X = [seqid_class_traj_alphas]

    clusterer = msmbuilder.cluster.KMedoids(n_clusters=nmodels_per_class, metric='rmsd')
    clusterer.fit(X)

    seqid_class_cluster_indices = clusterer.cluster_ids_
    seqid_class_cluster_indices.sort()
    if seqid_class == [55., 101.]:
        # XXX manually selecting two 
        seqid_class_selected_model_indices = [11, 21]
        seqid_class_selected_model_indices.append(list(seqid_class_df.iloc[seqid_class_cluster_indices].index)[-1])
    else:
        seqid_class_selected_model_indices = list(seqid_class_df.iloc[seqid_class_cluster_indices].index)
    # seqid_class_cluster_seqids = list(seqid_class_df.iloc[seqid_class_cluster_indices].seqid.values)
    seqid_class_cluster_seqids = list(df.loc[seqid_class_selected_model_indices].seqid.values)
    model_indices += seqid_class_selected_model_indices
    seqids += seqid_class_cluster_seqids

seqids = np.array(seqids)

# model_indices = []
# seqids = []
# for seqid_class in seqid_classes:
#     df_class = df[df.seqid >= seqid_class[0]][df.seqid < seqid_class[1]]
#     selected_model_indices = random.sample(df_class.index, nmodels_per_class)
#     selected_models = df_class.loc[selected_model_indices].sort()
#     model_indices += list(selected_models.index)
#     seqids += list(selected_models.seqid.values)
#
# nmodels = len(model_indices)

nmodels = nmodels_per_class * len(seqid_classes)
with open('superposed-seqid_classes-clustered-data.txt', 'w') as data_txt_file:
    data_txt_file.write('Number of models selected: {0}\n'.format(nmodels))
    data_txt_file.write('\n'.join(['{:6d} {:6.1f}'.format(x[0], x[1]) for x in zip(model_indices, seqids)]) + '\n')

modelsdir = 'models'
if os.path.exists(modelsdir):
    shutil.rmtree(modelsdir)
    os.mkdir(modelsdir)
else:
    os.mkdir(modelsdir)

for m,f in enumerate(model_indices):
    frame = traj[f]
    frame.save_pdb(os.path.join(modelsdir, '{0}.pdb'.format(m)))


transparency_floats = 1. - seqids*0.01
transparency_text = '\n'.join(['set cartoon_transparency, {0}, {1}'.format(transparency_floats[m], m) for m in range(nmodels)])

colors = cmap(
    seqids/max(seqids)
    # (seqids-min(seqids))/max(seqids-min(seqids))
)

set_color_text = '\n'.join(['set_color color{0}, [{1}, {2}, {3}]'.format(m, colors[m][0], colors[m][1], colors[m][2]) for m in range(nmodels)])
color_text = '\n'.join(['color color{0}, {0}'.format(m) for m in range(nmodels)])

renderscripttext = """\
bg white
# set ray_opaque_background, off
# set ray_trace_mode, 0
# set ambient, 1
# set reflect, 0
set antialias, 1
set two_sided_lighting, on
set cartoon_fancy_helices, 1

hide
show cartoon

{0}

{1}

{2}

# color black

zoom all

# ray 1280,960
# png superposed.png
""".format(transparency_text, set_color_text, color_text)

with open('render.pml', 'w') as renderscriptfile:
    renderscriptfile.write(renderscripttext)
