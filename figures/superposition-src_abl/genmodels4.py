# Three seqid classes (manually chosen). RMSD clustering performed within each class, and centroids picked.

import os
import shutil
import tempfile
import random
import numpy as np
import pandas as pd
import mdtraj as md
import msmbuilder.cluster
import seaborn as sns

srcdir = '../../data/models/SRC_HUMAN_D0'

nmodels_per_class = 3

seqid_classes = [[0., 35.], [35., 55.], [55., 101.]][::-1]

traj = md.load(os.path.join(srcdir, 'modelstraj.xtc'), top=os.path.join(srcdir, 'modelstraj-topol.pdb'))

df = pd.read_csv(os.path.join(srcdir, 'modelstraj-data.csv'))

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
    seqid_class_selected_model_indices = list(seqid_class_df.iloc[seqid_class_cluster_indices].index)
    seqid_class_cluster_seqids = list(seqid_class_df.iloc[seqid_class_cluster_indices].seqid.values)
    model_indices += seqid_class_selected_model_indices
    seqids += seqid_class_cluster_seqids

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
print 'Number of models selected:', nmodels
print '\n'.join(['{:6d} {:6.1f}'.format(x[0], x[1]) for x in zip(model_indices, seqids)])

modelsdir = 'models'
if os.path.exists(modelsdir):
    shutil.rmtree(modelsdir)
    os.mkdir(modelsdir)
else:
    os.mkdir(modelsdir)

for m,f in enumerate(model_indices):
    frame = traj[f]
    frame.save_pdb(os.path.join(modelsdir, '{0}.pdb'.format(m)))


# seqids = [df.seqid[f] for f in model_indices]
transparency_floats = [(1. - seqid*0.01) for seqid in seqids]
transparency_text = '\n'.join(['set cartoon_transparency, {0}, {1}'.format(transparency_floats[m], m) for m in range(nmodels)])

palette = sns.color_palette('RdBu', nmodels)[::-1]
set_color_text = '\n'.join(['set_color color{0}, [{1}, {2}, {3}]'.format(m, palette[m][0], palette[m][1], palette[m][2]) for m in range(nmodels)])
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

{1}

{2}

# color black

zoom all

# ray 1280,960
# png superposed.png
""".format(transparency_text, set_color_text, color_text)

with open('render.pml', 'w') as renderscriptfile:
    renderscriptfile.write(renderscripttext)
