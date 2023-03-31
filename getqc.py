import re
import os
import glob
import pandas as pd
import pdb

studydir = "/data/sbdp/PHOENIX/GENERAL/BLS"

def get_vals(file_path):
    #define search paths

    regex_qcsnr = "[\n\r].*qc_sSNR\s*([^\n\r]*)"
    regex_motabs = "[\n\r].*mot_abs_xyz_max\s*([^\n\r]*)"

    # open txt file
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        res1 = re.findall(regex_qcsnr, content, re.MULTILINE)
        res2 = re.findall(regex_motabs, content, re.MULTILINE)
    
    return res1, res2

  # regex1a = "\bqc_sSNR:\s+\K\S+"
  # regex1b = "[\n\r].*qc_sSNR:\s*([^\n\r]*)"

## main ##
df = []

for subj in next(os.walk(studydir))[1]:
    procmri_dir = os.path.join(studydir, subj,'mri', 'processed','process_mri')

    if os.path.exists(procmri_dir):
        for mri_session in next(os.walk(procmri_dir))[1]:
            bqc_dir = os.path.join(procmri_dir,mri_session,'qc','boldqc')
            cbig_dir = os.path.join(procmri_dir, "cbig", mri_session, "surf")
            # get niipath file
            npt_dir = os.path.join(procmri_dir, "cbig", "niipaths")
            npt_nme = subj + "_" + mri_session + "_run_info.csv"
            npt_pth = os.path.join(npt_dir, npt_nme)
            try:
                npt_csv = pd.read_csv(npt_pth, dtype={'cbig_num': str})
            except FileNotFoundError:
                print("No npt path for: ", npt_pth)
                pass
            except pd.errors.EmptyDataError:
                print("Empty data for ", npt_pth)
                pass

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
                                r1, r2 = get_vals(restRpt_path[0])
                                cbig_num = npt_csv.loc[npt_csv['run_num'] == int(restRun), 'cbig_num'].iloc[0]
                                cbig_str = "*bld" + cbig_num + "*"
                                df_rest = pd.DataFrame({"SubjID": [subj], "SessionID": [mri_session], "Type": ["REST"],
                                                        "Run": [restRun], "cbig_num": [cbig_num], "cbig_dir": [cbig_dir],
                                                        "cbig_str": [cbig_str],"qc_sSNR": [r1[0]], "mot_abs_xyz_max": [r2[0]]})    
                                df.append(df_rest)
                            except IndexError:
                                pass

                if os.path.exists(task_dir):
                    for taskRun in next(os.walk(task_dir))[1]:
                        taskRun_dir = os.path.join(task_dir, taskRun)
                        tkExtd_dir = os.path.join(taskRun_dir,'extended-qc')
                        
                        if os.path.exists(tkExtd_dir):
                            tkRpt_path = glob.glob(os.path.join(tkExtd_dir, '*_auto_report.txt'))
                            
                            try:
                                r1, r2 = get_vals(tkRpt_path[0])
                                cbig_num = npt_csv.loc[npt_csv['run_num'] == int(taskRun), 'cbig_num'].iloc[0]
                                cbig_str = "*bld" + cbig_num + "*"
                                df_task = pd.DataFrame({"SubjID": [subj], "SessionID": [mri_session], "Type": ["TASK"],
                                                        "Run": [taskRun], "cbig_num": [cbig_num], "cbig_dir": [cbig_dir],
                                                        "cbig_str": [cbig_str], "qc_sSNR": [r1[0]], "mot_abs_xyz_max": [r2[0]]})
                                df.append(df_task)

                            except IndexError:
                                pass


df = pd.concat(df)
df.to_csv('/PHShome/vlh14/Downloads/BLSqc.csv', index=None)






#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc/TASK/12/extended-qc/



#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc/TASK


#/data/sbdp/PHOENIX/GENERAL/BLS/7NE49/mri/processed/process_mri/160229_HTP01825/qc/boldqc
    # run all the steps from the image
    # the input to the qc_grab function will be the full path to the txt file

