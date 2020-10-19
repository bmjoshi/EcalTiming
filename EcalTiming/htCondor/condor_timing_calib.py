import sys
import os
import argparse
import random
from math import *

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele+","   
    
    # return string   
    return str1  

with open("command_step2.txt", "w") as of:
    of.write(" ".join(["python"]+sys.argv))

'''
This scripts runs hadd on single crystal files to 
group them in strips reading a DOF file
'''
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--inputDir", type=str, help="inputDir", required=True)
parser.add_argument("-l", "--inputList", type=str, help="inputList", required=True)
parser.add_argument("-o", "--outputDir", type=str, help="OutputDir", required=True)
parser.add_argument("-c", "--cmssw", type=str, help="CMSSW tar", required=True)
parser.add_argument("-q", "--queue", type=str, help="Condor queue", default="longlunch", required=True)
args = parser.parse_args()

# Check input files
input_files = []
output_dir = []
with open(args.inputList) as f_list:
   data_list = f_list.read()
lines = data_list.splitlines() 
for iLine,line in enumerate(lines):
   files_tmp = []
   runs = line.split(',')
   #print iLine, runs
   for run in runs:
      files = os.popen('ls '+args.inputDir+'/'+run+'/*.root').readlines()  
      for file in files: files_tmp.append(file[:-1]) 
   input_files.append(files_tmp)
   output_dir.append(line.replace(',','_'))

#print "Selected Files: ",files_selected

# Prepare condor jobs
condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))

+JobFlavour             = "{queue}"
+AccountingGroup        = "group_u_CMS.CAF.ALCA" 
queue arguments from arguments.txt

'''

condor = condor.replace("{queue}", args.queue)
user = os.environ["USER"]

script = '''#!/bin/sh -e

JOBID=$1
INPUTFILES=$2;
OUTPUTDIR=$3;

cp -r {cmssw_loc} ./
cd {cmssw_file}/src

echo -e "evaluate"
eval `scramv1 ru -sh`
export HOME='/afs/cern.ch/user/{user1}/{user}'

cd EcalTiming/EcalTiming/htCondor/

eos mkdir ${OUTPUTDIR}

sed -i "s%LISTOFFILES%${INPUTFILES}%" EcalTimingCalibration_cfg.py
sed -i "s%OUTPUT%${OUTPUTDIR}%" EcalTimingCalibration_cfg.py

echo -e ">>> Run calibration";
EcalTimingCalibration EcalTimingCalibration_cfg.py

echo -e "DONE";
'''

script = script.replace("{user1}", user[:1])
script = script.replace("{user}", user)
cmssw_file = args.cmssw.split("/")[-1]
script = script.replace("{cmssw_loc}", args.cmssw)
script = script.replace("{cmssw_file}", cmssw_file)


arguments= []

for iJob,files in enumerate(input_files):
    output = args.outputDir+'/'+output_dir[iJob]+'/'  
    arguments.append("{} {} {}".format(iJob+1,listToString(files)[:-1],output))

print("Njobs: ", len(arguments))
    
with open("condor_job.txt", "w") as cnd_out:
    cnd_out.write(condor)

with open("arguments.txt", "w") as args:
    args.write("\n".join(arguments))

with open("run_script.sh", "w") as rs:
    rs.write(script)

#os.system("condor_submit condor_job.txt")


