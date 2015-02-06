targets=(ALK_HUMAN_D0 EGFR_HUMAN_D0 SRC_HUMAN_D0 ABL2_HUMAN_D0)
# templates=(AAK1_HUMAN_D0_4WSQ_A ABL1_HUMAN_D0_1OPL_A ABL1_MOUSE_D0_1FPU_A ACVR1_HUMAN_D0_3H9R_A ACVL1_HUMAN_D0_3MY0_A AKT1_HUMAN_D0_3CQU_A AKT2_HUMAN_D0_1GZK_A ALK_HUMAN_D0_2XB7_A)
# templates=(AAK1_HUMAN_D0_4WSQ_A ABL1_HUMAN_D0_1OPL_A ABL1_MOUSE_D0_1FPU_A ACVR1_HUMAN_D0_3H9R_A ACVL1_HUMAN_D0_3MY0_A AKT1_HUMAN_D0_3CQU_A ARBK1_BOVIN_D0_1OMW_A ALK_HUMAN_D0_2XB7_A)
templates=(ARBK1_BOVIN_D0_1OMW_A)

for target in "${targets[@]}"
do
    for template in "${templates[@]}"
    do
        scp -r parton@hal.cbio.mskcc.org:/cbio/jclab/projects/parton/kinome-ensembler/models/$target/$template $target/
    done
done

