load aligned0.pdb, ref
load models/ABL1_HUMAN_D0/ABL1_HUMAN_D0_1OPL_A/explicit-refined.pdb.gz, solvated

align solvated, ref

select water=(solvated & resname; HOH)

bg white
# set ray_opaque_background, off
set ray_trace_mode, 0
set ambient, 1
set reflect, 0
set antialias, 1
set two_sided_lighting, on
set cartoon_fancy_helices, 1
set_color dblue, [0.204, 0.298, 0.384]

hide
color deepteal, ss h
color dblue, ss s
color grey, ss l+''
color teal, water


bg white

zoom all

show cartoon
ray 640,480
png solvated-nowater.png
show lines, water
ray 640,480
png solvated.png
