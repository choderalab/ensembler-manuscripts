# Randomly pick models from each of three sequence identity classes

import os
import shutil
import tempfile
import random
import numpy as np
import pandas as pd
import mdtraj
import seaborn as sns

srcdir = '../../../data/models/SRC_HUMAN_D0'

nmodels_per_class = 3

df = pd.read_csv(os.path.join(srcdir, 'traj-refine_implicit_md-data.csv'))

traj = mdtraj.load(os.path.join(srcdir, 'traj-refine_implicit_md.xtc'), top=os.path.join(srcdir, 'traj-refine_implicit_md-topol.pdb'))

modelsdir = 'models'
if os.path.exists(modelsdir):
    shutil.rmtree(modelsdir)
    os.mkdir(modelsdir)
else:
    os.mkdir(modelsdir)

seqid_classes = [[0., 35.], [35., 55.], [55., 101.]][::-1]
model_indices = []
seqids = []
for seqid_class in seqid_classes:
    df_class = df[df.seqid >= seqid_class[0]][df.seqid < seqid_class[1]]
    selected_model_indices = random.sample(df_class.index, nmodels_per_class)
    selected_models = df_class.loc[selected_model_indices].sort()
    model_indices += list(selected_models.index)
    seqids += list(selected_models.seqid.values)

nmodels = len(model_indices)

print 'Number of models selected:', nmodels
print '\n'.join(['{:6d} {:6.1f}'.format(x[0], x[1]) for x in zip(model_indices, seqids)])

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
