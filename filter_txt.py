import re


def get_vals(file_path):
  # define search paths
  regex1 = "\bqc_sSNR:\s+\K\S+"
  regex2 = "\mot_abs_xyz_max:\s+\K\S+"
  # open txt file
  with open(file_path, 'r') as file:
    # read all content of a file
    content = file.read()
    # check if string present in a file
    res1 = re.findall(regex1, content)
    res2 = re.findall(regex2, content)
    
    return res1, res2
    
  # regex1a = "\bqc_sSNR:\s+\K\S+"
  # regex1b = "[\n\r].*qc_sSNR:\s*([^\n\r]*)"
  
