import os
import shutil
import pandas as pd


def mk_models_data_file(traj_csv_filepath, rmsd_csv_filepath, output_csv_filepath):
    traj_df = pd.read_csv(traj_csv_filepath)
    rmsd_df = pd.read_csv(rmsd_csv_filepath)
    merged_df = pd.merge(traj_df, rmsd_df, on='templateid')
    merged_df.set_index('templateid', inplace=True)
    merged_df.rename(columns={'seqid_x': 'seqid'}, inplace=True)
    merged_df.to_csv(output_csv_filepath, columns=['seqid', 'rmsd'], index_label='templateid')
    return merged_df


if __name__ == '__main__':
    targetids = open('TKs.txt').read().splitlines()

    shutil.copy('targets_general_data/targets-data.txt', '../dataset-for-publication/')
    shutil.copy('targets_general_data/targets-data.csv', '../dataset-for-publication/')
    shutil.copy('TKs.txt', '../dataset-for-publication/targets-IDs.txt')
    shutil.copy('templates_general_data/templates-data.txt', '../dataset-for-publication/')
    shutil.copy('templates_general_data/templates-data.csv', '../dataset-for-publication/')

    if not os.path.exists('../dataset-for-publication/models'):
        os.mkdir('../dataset-for-publication/models')

    for targetid in targetids:
        src_dir = os.path.join('models', targetid)
        dest_dir = os.path.join('../dataset-for-publication', 'models', targetid)
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        src_filenames = [
            'topol-renumbered-implicit.pdb',
            'traj-refine_implicit_md.xtc',
        ]
        dest_filenames = [
            'topology.pdb',
            'models.xtc',
        ]

        for src_filename, dest_filename in zip(src_filenames, dest_filenames):
            shutil.copy(
                os.path.join(
                    src_dir,
                    src_filename
                ),
                os.path.join(
                    dest_dir,
                    dest_filename
                )
            )

        merged_df = mk_models_data_file(
            os.path.join(src_dir, 'traj-refine_implicit_md-data.csv'),
            os.path.join(src_dir, 'rmsds.csv'),
            os.path.join(dest_dir, 'models-data.csv'),
        )
