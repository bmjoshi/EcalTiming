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

with open("command_step1.txt", "w") as of:
    of.write(" ".join(["python"]+sys.argv))

'''
This scripts runs hadd on single crystal files to 
group them in strips reading a DOF file
'''
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--inputDataset", type=str, help="inputDataset", required=True)
parser.add_argument("-b", "--beginRun", type=str, help="beginRun", required=False)
parser.add_argument("-e", "--endRun", type=str, help="endRun", required=False)
parser.add_argument("-m", "--maxJobs", type=str, help="maxJobs", required=False)
parser.add_argument("-gt", "--GT", type=str, help="globalTag", required=True)
parser.add_argument("-o", "--outputdir", type=str, help="Outputdir", required=True)
parser.add_argument("-c", "--cmssw", type=str, help="CMSSW tar", required=True)
parser.add_argument("-q", "--queue", type=str, help="Condor queue", default="longlunch", required=True)
parser.add_argument("-p", "--proxy", type=str, default="x509up_u35923", help="proxy key", required=False)
args = parser.parse_args()

# MaxJobs
maxJobs = 5000
if args.maxJobs is not None:
   maxJobs = int(args.maxJobs)

# Check input files
runs = os.popen('dasgoclient --query=\'run dataset='+args.inputDataset+'\'').readlines()
runs_selected = []
files_selected = []

beginRun = args.beginRun
endRun = args.endRun
if beginRun is None or endRun is None:
   for run in runs: 
      runs_selected.append(int(run))  
else:
   for run in runs:
      if int(run)>=int(beginRun) and int(run)<=int(endRun):
         runs_selected.append(int(run))       

#print "Selected Runs: ", runs_selected 
print "Number selected runs: ", len(runs_selected) 
for run in runs_selected:
   files = os.popen('dasgoclient --query=\'file dataset='+args.inputDataset+' run='+str(run)+'\'').readlines()
   files_tmp = []
   for file in files:
      file = file.rstrip("\n")
      files_tmp.append('root://cms-xrd-global.cern.ch/'+file)
   files_selected.append(files_tmp)

if maxJobs<len(runs_selected):
   maxJobs = len(runs_selected)

jobModulo = int(float(maxJobs)/float(len(runs_selected)))
print "jobModulo: ",jobModulo

job_files = []
run_files = []
for iRun, files in enumerate(files_selected):
   step = len(files_selected[iRun])/jobModulo
   if len(files_selected[iRun])%jobModulo!=0:
      step+=1
   #print "Run: ",runs_selected[iRun],len(files_selected[iRun]),step
   for iJob in range(0,int(jobModulo)):
      files_tmp=[]
      for iFile, file in enumerate(files):
         if iFile>=iJob*int(step) and iFile<(iJob+1)*int(step):
            files_tmp.append(file) 
      if len(files_tmp)!=0:
         job_files.append(files_tmp) 
         run_files.append(runs_selected[iRun]) 
      
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
RUN=$2
INPUTFILES=$3;
OUTPUTDIR=$4;
GT=$5
PROXY=$6

export X509_USER_PROXY=/afs/cern.ch/user/{user1}/{user}/${PROXY}
voms-proxy-info

cp -r {cmssw_loc} ./
cd {cmssw_file}/src

echo -e "evaluate"
eval `scramv1 ru -sh`
export HOME='/afs/cern.ch/user/{user1}/{user}'

cd EcalTiming/EcalTiming

echo -e "cmsRun..";

echo -e ">>> Run RECO and selections";
cmsRun test/ecalTime_fromAlcaStream_cfg.py files=${INPUTFILES} globaltag=${GT} outputFile=timing_reco_selections_${RUN}_${JOBID}.root
eos mkdir ${OUTPUTDIR}/${RUN}
xrdcp -f --nopbar  timing_reco_selections_${RUN}_${JOBID}.root root://eoscms.cern.ch/${OUTPUTDIR}/${RUN};
rm timing_reco_selections_${RUN}_${JOBID}.root

echo -e "DONE";
'''

script = script.replace("{user1}", user[:1])
script = script.replace("{user}", user)
cmssw_file = args.cmssw.split("/")[-1]
script = script.replace("{cmssw_loc}", args.cmssw)
script = script.replace("{cmssw_file}", cmssw_file)

arguments= []

for iJob, job in enumerate(job_files):
    arguments.append("{} {} {} {} {} {}".format(iJob+1,run_files[iJob],listToString(job)[:-1],args.outputdir,args.GT, args.proxy))

print("Njobs: ", len(arguments))
    
with open("condor_job.txt", "w") as cnd_out:
    cnd_out.write(condor)

with open("arguments.txt", "w") as args:
    args.write("\n".join(arguments))

with open("run_script.sh", "w") as rs:
    rs.write(script)

#os.system("condor_submit condor_job.txt")



