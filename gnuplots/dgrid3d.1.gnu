# set terminal pngcairo  background "#ffffff" enhanced font "arial,8" fontscale 1.0 size 450, 320 
# set output 'dgrid3d.1.png'
unset key
set view 60, 75, 1, 1
set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set title "The Valley of the Gnu" 
splot "gnu-valley" u 1:2:3 w linesp
