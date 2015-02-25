# Pick models across a wide range of sequence identities

import os
import shutil
import tempfile
import numpy as np
import pandas as pd
import mdtraj
import seaborn as sns

srcdir = '../../data/models/SRC_HUMAN_D0'

df = pd.read_csv(os.path.join(srcdir, 'modelstraj-data.csv'))

traj = mdtraj.load(os.path.join(srcdir, 'modelstraj.xtc'), top=os.path.join(srcdir, 'modelstraj-topol.pdb'))

nmodels = 20

modelsdir = 'models'
if os.path.exists(modelsdir):
    shutil.rmtree(modelsdir)
    os.mkdir(modelsdir)
else:
    os.mkdir(modelsdir)

# model_indices = np.arange(nmodels) * (len(traj) / nmodels)

desired_seqid_values = 100. - np.arange(0., 100., 100./nmodels)
model_indices = [np.abs(df.seqid.values-seqid_value).argmin() for seqid_value in desired_seqid_values]
model_indices = sorted(list(set(model_indices)))
nmodels = len(model_indices)
seqids = [df.seqid.values[m] for m in model_indices]

print 'Number of models selected:', nmodels
print '\n'.join(['{:6d} {:6.1f}'.format(x[0], x[1]) for x in zip(model_indices, seqids)])

for m,f in enumerate(model_indices):
    frame = traj[f]
    frame.save_pdb(os.path.join(modelsdir, '{0}.pdb'.format(m)))


# seqids = [df.seqid[f] for f in model_indices]
transparency_floats = [(1. - seqid*0.01) for seqid in seqids]
transparency_text = '\n'.join(['set cartoon_transparency, {0}, {1}'.format(transparency_floats[m], m) for m in range(nmodels)])

palette = sns.color_palette('Bluered', nmodels)[::-1]
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
