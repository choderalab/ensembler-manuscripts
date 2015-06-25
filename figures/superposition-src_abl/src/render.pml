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
set cartoon_transparency, 0.319, 2
set cartoon_transparency, 0.559, 3
set cartoon_transparency, 0.576, 4
set cartoon_transparency, 0.579, 5
set cartoon_transparency, 0.677, 6
set cartoon_transparency, 0.74, 7
set cartoon_transparency, 0.76, 8

set_color color0, [0.0, 0.0, 1.0]
set_color color1, [0.0078431372549, 0.0, 0.992156862745]
set_color color2, [0.317647058824, 0.0, 0.682352941176]
set_color color3, [0.560784313725, 0.0, 0.439215686275]
set_color color4, [0.576470588235, 0.0, 0.423529411765]
set_color color5, [0.580392156863, 0.0, 0.419607843137]
set_color color6, [0.678431372549, 0.0, 0.321568627451]
set_color color7, [0.741176470588, 0.0, 0.258823529412]
set_color color8, [0.760784313725, 0.0, 0.239215686275]

color color0, 0
color color1, 1
color color2, 2
color color3, 3
color color4, 4
color color5, 5
color color6, 6
color color7, 7
color color8, 8

# color black

zoom all

# ray 1280,960
# png superposed-seqid_classes-clustered-one_fig-BlueRedAlpha.png
