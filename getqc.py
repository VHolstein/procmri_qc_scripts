import re
import os
import glob

studydir = "/data/sbdp/PHOENIX/GENERAL/BLS"

def get_vals(file_path):
  # define search paths
  #regex1 = "\bqc_sSNR:\s+\K\S+"
  #regex2 = "\mot_abs_xyz_max:\s+\K\S+"

  #regex1a = "\bqc_sSNR:\s+\K\S+"
  regex1b = "[\n\r].*qc_sSNR:\s*([^\n\r]*)"
  regex2b = "[\n\r].*mot_abs_xyz_max:\s*([^\n\r]*)"

  # open txt file
  with open(file_path, 'r') as file:
    # read all content of a file
    content = file.read()
    # check if string present in a file
    res1 = re.findall(regex1b, content)
    res2 = re.findall(regex2b, content)
    
    return res1, res2

  # regex1a = "\bqc_sSNR:\s+\K\S+"
  # regex1b = "[\n\r].*qc_sSNR:\s*([^\n\r]*)"

## main ##
for subj in next(os.walk(studydir))[1]:
    procmri_dir = os.path.join(studydir, subj,'mri', 'processed','process_mri')

    if os.path.exists(procmri_dir):
        for mri_session in next(os.walk(procmri_dir))[1]:
            bqc_dir = os.path.join(procmri_dir,mri_session,'qc','boldqc')

            if os.path.exists(bqc_dir):
                rest_dir = os.path.join(bqc_dir,'REST')
                task_dir = os.path.join(bqc_dir,'TASK')
                
                if os.path.exists(rest_dir):
                    for restRun in next(os.walk(rest_dir))[1]:
                        restRun_dir = os.path.join(rest_dir, restRun)
                        rsExtd_dir = os.path.join(restRun_dir,'extended-qc')
                        
                        if os.path.exists(rsExtd_dir):
                            restRpt_path = glob.glob(os.path.join(rsExtd_dir,'*_auto_report.txt'))
                            
                            try:
                                r1,r2 = get_vals(restRpt_path[0])                    
                                print(r1)
                                print(r2)

                            except IndexError:
                                pass

                            

                if os.path.exists(task_dir):
                    for taskRun in next(os.walk(task_dir))[1]:
                        taskRun_dir = os.path.join(task_dir, taskRun)
                        tkExtd_dir = os.path.join(taskRun_dir,'extended-qc')
                        
                        if os.path.exists(tkExtd_dir):
                            tkRpt_path = glob.glob(os.path.join(tkExtd_dir, '*_auto_report.txt'))
                            
                            try:
                                print(tkRpt_path[0])
                            
                            except IndexError:
                                pass









#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc/TASK/12/extended-qc/



#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc/TASK


#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc
    # run all the steps from the image
    # the input to the qc_grab function will be the full path to the txt file

