about_plane = "Manipulates the Omnisim input file, created by the Nanoparticle Detector: \
changes plane in which nanoparticles are located - from xy to xz (or zx), \
and also allows for some other corrections as change project and device numbers, \
layer indices, baseline, and reversing values on the x-axis. \
\n \
\nInput: \
\nPython file (.py) with the following structure:\
\n  (...)\
\n  f.Exec(\"app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)\")\
\n  (...)\
\n \
\nOutput:\
\n  Python file (.py) with a \"_xz\" suffix."

about_truncate = "Program adjusts y-positions of the spheres in the input script for Omnisim,\
so they will appear as the truncated and flattened spheres in the baseline.\
It is done by applying the truncating and flattening factors, given in percent\
with some standard deviation.\
\n \
\n More info: http://www.ambrsoft.com/TrigoCalc/Sphere/Cap/SphereCap.htm \
\n \
\nInput:\
\n  Python file with the following structure:\
\n  (...)\
\n  f.Exec(\"app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)\")\
\n  (...)\
\n  Assumption: nanoparticles are placed in the \"zx\" or \"xz\" plane, so y value is to be adjusted.\
\nOutput:\
\n  File with a \"_truncx_flaty\" suffix, where x is the truncating factor and y is the flattening factor"

about_convert = "Program converts the .txt or .cht file with sensor data from OmniSim, to the corresponding .cht or .txt file.\
\n \
\nInput:\
\n  .txt/.cht file\
\nOutput:\
\n  .cht/.txt file"

about_combine = "Combines two (.cht or .txt) files containing field, absorbance or flux, e.g.\
\n  - subtract: E = E1 - E2 (e.g. absorbance - reference absorbance)\
\n  - unpolarize: |E| = sqrt(0.5|E_TE|^2 + 0.5|E_TM|^2) (e.g. EZ and HZ polarized fluxes)\
\n  - calculate absorbance: E = log10(E1/E2) (e.g. input flux / output flux)\
\n  - calculate transmitance: E = E2/E1 (e.g. output flux / input flux)\
\n \
\nInput:\
\n  Two files(.cht or .txt) from Omnisim (2D/1D). Files can be different type.\
\nOutput:\
\n  Output file will be the same type as the first file.\
\n  - subtract: first file name with suffix \"_s\" \
\n  - unpolarize: first file name with suffix \"_u\" (\"_ez\" or \"_hz\" are removed from filename.) \
\n  - calculate absorbance: first file name with prefix \"abs_\" \
\n  - calculate transmitance: first file name with suffix \"_t\" "

about_max = "Finds maxima of the absorption spectra given in the the *.txt or .cht files.\
\n \
\nInput: \
\n  All .cht and .txt files from current directory, containing sensor data from Omnisim.\
\n  For best results (e.g. automatic determination of variable names),\
\n  Omnisim should be run in FDTD Scanner mode, scanning for np_size, inglass, trunc etc.\
\nOutput:\
\n  abs-max-out file"

about_plot = "Plots data from the .cht or .txt file and saves it as the png file. \
\n \
\nInput:\
\n  .cht file from Omnisim\
\nOutput:\
\n  .png graphics file with a plot."