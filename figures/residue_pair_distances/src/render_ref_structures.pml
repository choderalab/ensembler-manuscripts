# This file loads a pymol input macro that compares the structures used in
# Shukla...Pande, Nat. Comm. (2014)  
# The main aim is to look at inactive vs. actove of Src with the following PDBs:
# 1Y57 - SH3, SH2 and kinase domains; apo; (semi-)active extended conformation; Y530 not phosphorylated; ATP-competitive inhibitor
# 2SRC - Human Src residues 86-836, containing SH2, SH3, Kinase domain, and C-terminal tail; AMP-PNP

# load PDBs

load 1Y57.pdb, 1Y57_transparent
load 2SRC.pdb, 2SRC_transparent
load 1Y57.pdb
load 2SRC.pdb
load 2SRC.pdb, 1Y57_ANP_structure

set cartoon_transparency, 0.4, 1Y57_transparent
set cartoon_transparency, 0.4, 2SRC_transparent

# Each of these already only consists of just Chain A, but there are SH3-SH2 domains in both structures

# align two structures

# define and color relevant motifs
# Kinase Domain
# (POL means polymer)
select 1Y57_kin=(1Y57 & POL & i;258-522)
select 2SRC_kin=(2SRC & POL & i;258-522)
select 1Y57_transparent_kin=(1Y57_transparent & POL & i;258-522)
select 2SRC_transparent_kin=(2SRC_transparent & POL & i;258-522)
# select 1Y57_transparent_kin=(1Y57_transparent & POL & i;258-522 & ! i;303-316+409-424+293-296)
# select 2SRC_transparent_kin=(2SRC_transparent & POL & i;258-522 & ! i;303-316+408-424+293-296)
# color gray70, 1Y57_kin
# color gray30, 2SRC_kin
# ligands
select 1Y57_MPZ=(1Y57 & resname MPZ)
select 2SRC_ANP=(2SRC & resname ANP)
select 1Y57_ANP=(1Y57_ANP_structure & resname ANP)
# color palecyan, 1Y57_MPZ
# color tv_blue, 2SRC_ANP

# DFG
select 1Y57_DFG=(1Y57_kin & i;404-406)
select 2SRC_DFG=(2SRC_kin & i;404-406)
# color limon, 1Y57_DFG
# color forest, 2SRC_DFG

# P-Loop (LGGGQYGEVY or LGQGCFGEVW) 
# P for Purple
select 1Y57_Ploop=(1Y57_kin& POL & i;273-282)
select 2SRC_Ploop=(2SRC_kin& POL & i;273-282)
# color violet, 1Y57_Ploop
# color deeppurple, 2SRC_Ploop
# C-Helix (EVEEFLKEAAVMKEI or MSPEAFLQEAEQVMKKL)
select 1Y57_CHelix=(1Y57_kin & POL & i;302-317)
select 2SRC_CHelix=(2SRC_kin & POL & i;302-317)
# color paleyellow, 1Y57_CHelix
# color brightorange, 2SRC_CHelix
# A-Loop (LSRLMTGDTYTAHAGAKFP or LARLIEDNEYTARQGAKFP)
# Note A loop not resolved in this structure
select 1Y57_Aloop=(1Y57_kin & POL & i;407-425)
select 2SRC_Aloop=(2SRC_kin & POL & i;407-425)
# color salmon, 1Y57_Aloop
# color firebrick, 2SRC_Aloop

# SH3_SH2 Domain
select 1Y57_SH2SH3=(1Y57 & POL & i;84-258)
select 2SRC_SH2SH3=(2SRC & POL & i;84-258)
# C-term loop
select 2SRC_Cterm=(2SRC & POL & i;522-533)

# ANP alignment selections
select 1Y57_ANP_structure_align_region=(1Y57_ANP_structure & POL & i;388-394)
select 1Y57_transparent_ANP_align_region=(1Y57_transparent & POL & i;388-394)

# align two structures
align 1Y57_kin, 2SRC_kin
align 1Y57_transparent_kin, 1Y57_kin
align 1Y57_transparent_kin, 2SRC_kin
align 1Y57_ANP_structure_align_region, 1Y57_transparent_ANP_align_region




color green, 2SRC_ANP or 1Y57_ANP
util.cnc("2SRC_ANP or 1Y57_ANP")




color gray, 1Y57_transparent_kin
color gray, 2SRC_transparent_kin

color lightblue, 1Y57_Aloop or 2SRC_Aloop
color palegreen, 1Y57_CHelix or 2SRC_CHelix

select 1Y57_K295_strand=(1Y57_kin & i;292-297)
select 2SRC_K295_strand=(2SRC_kin & i;292-297)
color paleyellow, 1Y57_K295_strand or 2SRC_K295_strand

select 1Y57_selected_resis=(1Y57_kin & i;295+310+409 & ! name;C+N+O)
select 2SRC_selected_resis=(2SRC_kin & i;295+310+409 & ! name;C+N+O)
util.cnc("2SRC_selected_resis")
util.cnc("1Y57_selected_resis")


select 1Y57_K295_tip=(1Y57_kin & i;295 & name;NZ)
select 1Y57_E310_tip=(1Y57_kin & i;310 & name;OE1)
select 2SRC_K295_tip=(2SRC_kin & i;295 & name;NZ)
select 2SRC_E310_tip=(2SRC_kin & i;310 & name;OE1)
select 2SRC_R409_tip=(2SRC_kin & i;409 & name;NH2)
select 2SRC_ANP_contact_oxygen=(2SRC & resname;ANP & name;O2A)

distance dist1, 1Y57_K295_tip, 1Y57_E310_tip
distance dist2, 2SRC_E310_tip, 2SRC_R409_tip
distance dist3, 2SRC_K295_tip, 2SRC_ANP_contact_oxygen
hide labels, dist1
hide labels, dist2
hide labels, dist3
color black, dist1
color black, dist2
color black, dist3



# rotate to relevant view point
rotate y, 80
rotate z, -100
rotate y, 50
rotate x, 60
center 2SRC_CHelix or 2SRC_K295_strand or 2SRC_DFG or 2SRC_ANP
# zoom 2SRC_CHelix or 2SRC_K295_strand or 2SRC_Aloop or 2SRC_ANP, -4
zoom 2SRC_kin

bg_color white
# set ray_shadows, 0
# set orthoscopic, on
# set ray_opaque_background, off
clip far, 4
# clip near, 20

# unset specular
# set ray_trace_gain, 0
# set ray_trace_mode, 3
# set ray_trace_color, black
# unset depth_cue


# set representations and render

hide all
show cartoon, 1Y57_transparent_kin

show cartoon, 1Y57_Aloop
show cartoon, 1Y57_CHelix
show sticks, 1Y57_ANP
show cartoon, 1Y57_K295_strand
show sticks, 1Y57_selected_resis
show dashes, dist1

ray 1280,960
png active.png

hide all
show cartoon, 2SRC_transparent_kin
show cartoon, 2SRC_Aloop
show cartoon, 2SRC_CHelix
show sticks, 2SRC_ANP
show cartoon, 2SRC_K295_strand
show sticks, 2SRC_selected_resis
show dashes, dist2
show dashes, dist3

ray 1280,960
png inactive.png
