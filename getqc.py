import os

studydir = ""

for file in next(os.walk(studydir))[1]:
  # run all the steps from the image
  
  # the input to the qc_grab function will be the full path to the txt file
