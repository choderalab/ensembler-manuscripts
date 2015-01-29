load aligned0.pdb, ref
load templates/structures-resolved/EGFR_HUMAN_D0_3LZB_D.pdb, resolved
load templates/structures-modeled-loops/EGFR_HUMAN_D0_3LZB_D.pdb, loopmodeled

select loops=(loopmodeled & i;38-43+147-164+236-238)
select notloops=(loopmodeled & ! i;38-43+147-164+236-238)

align resolved, ref
align notloops, ref

bg white
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
color red, loops

bg white

zoom all

show cartoon, resolved
ray 640,480
png EGFR_HUMAN_D0_3LZB_D-resolved.png

show cartoon, loopmodeled
hide cartoon, resolved
ray 640,480
png EGFR_HUMAN_D0_3LZB_D-loopmodeled.png
