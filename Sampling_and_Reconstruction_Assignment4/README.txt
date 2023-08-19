CS661A: BIG DATA VISUAL ANALYTICS


HOW TO RUN  THE CODE:
========================

PRE-REQUISITES: You should have installed the following python libraries on your system.
1.vtk
2.numpy
3.random
4.time
5.scipy

STEPS TO PERFORM:
=================

STEP1: OPEN this folder(directory) in  TERMINAL.

STEP1: Run the file "bigdata.py" through command : "python bigdata.py" for windows and "python3 bigdata.py" for linux without quotes.

STEP2: It will pop up: "Enter the sampling percentage %:"

STEP3: Then,Enter the sampling percentage either : 1, 3 or 5

STEP4: It will pop up : "Enter the method for reconstruction:"

STEP5: Then,Enter any method either "nearest" or "linear" without quotes.

STEP6: It will generate two files, first named "sampled.vtp" and second one "reconstructed_volume.vti"(it will depend on method)

STEP7. You can view these files in PARAVIEW.


There is a pdf file named "comparison.pdf". It shows the comparison between nearest and linear methods of reconstructed data and original data with their SNR value and reconstruction time.