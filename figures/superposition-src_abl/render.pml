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

set cartoon_transparency, 0.0, 0
set cartoon_transparency, 0.008, 1
set cartoon_transparency, 0.323, 2
set cartoon_transparency, 0.559, 3
set cartoon_transparency, 0.583, 4
set cartoon_transparency, 0.74, 5
set cartoon_transparency, 0.764, 6
set cartoon_transparency, 0.777, 7

set_color color0, [0.142483668, 0.417301045913, 0.683352575583]
set_color color1, [0.323490981378, 0.614917362438, 0.785467140815]
set_color color2, [0.654901981354, 0.814379096031, 0.89411765337]
set_color color3, [0.883890818147, 0.928489046938, 0.953018072773]
set_color color4, [0.982006921488, 0.906189932543, 0.861591703752]
set_color color5, [0.96862745285, 0.717647075653, 0.600000023842]
set_color color6, [0.862283745233, 0.429527115004, 0.342714355857]
set_color color7, [0.711880063309, 0.121799310341, 0.181699351937]

color color0, 0
color color1, 1
color color2, 2
color color3, 3
color color4, 4
color color5, 5
color color6, 6
color color7, 7

# color black

zoom all

# ray 1280,960
# png superposed.png
