from ensembler.tools.rendering import RenderOnGrid

targets = [
    'ALK_HUMAN_D0',
    'EGFR_HUMAN_D0',
    'SRC_HUMAN_D0',
    'ABL2_HUMAN_D0',
]

templates = [
    'AAK1_HUMAN_D0_4WSQ_A',
    'ABL1_HUMAN_D0_1OPL_A',
    'ABL1_MOUSE_D0_1FPU_A',
    'ACVR1_HUMAN_D0_3H9R_A',
    'ACVL1_HUMAN_D0_3MY0_A',
    'ARBK1_BOVIN_D0_1OMW_A',
    'AKT1_HUMAN_D0_3CQU_A',
    'ALK_HUMAN_D0_2XB7_A',
]

r = RenderOnGrid(nrows=4, ncols=8)

for target in targets:
    for template in templates:
        # label = ' / '.join([target, template])
        label = None
        r.add_model(target, template, label=label)

r.render('tiled.png')
