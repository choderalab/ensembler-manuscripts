import os
import subprocess

cwd = os.getcwd()

os.chdir('..')

dataset_dir = 'ensembler_dataset'

toplevel_filenames = [
    'templates-data.txt',
    'templates-data.csv',
    'targets-data.txt',
    'targets-data.csv',
    'targets-IDs.txt',
    'commands.sh',
]
toplevel_filepaths = [os.path.join(dataset_dir, fname) for fname in toplevel_filenames]

subprocess.check_output([
    'tar',
    'cvf',
    'ensembler_dataset-datafiles.tar',
] + toplevel_filepaths)

models_dir = os.path.join(dataset_dir, 'models')
targetids = os.listdir(models_dir)
targetids = sorted(targetids)

targets_to_tar = [[]]
tarsize = 0
for targetid in targetids:
    targetdir = os.path.join(models_dir, targetid)
    targetdir_size = sum([
        os.path.getsize(os.path.join(targetdir, f)) for f in os.listdir(targetdir)
    ])
    tarsize += targetdir_size
    if tarsize > 999999999:
        targets_to_tar.append([])
        tarsize = 0
    targets_to_tar[-1].append(targetid)

for targets in targets_to_tar:
    first_letters = targets[0].split('_')[0]
    last_letters = targets[-1].split('_')[0]
    tarfile = 'ensembler_dataset-models-{0}-{1}.tar'.format(first_letters, last_letters)
    targetdirs = [os.path.join(models_dir, targetid) for targetid in targets]

    subprocess.check_output([
        'tar',
        'cvf',
        tarfile,
    ] + targetdirs)

os.chdir(cwd)
