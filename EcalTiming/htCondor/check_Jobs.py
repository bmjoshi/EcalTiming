import sys
import os
import argparse
import random
from math import *

def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(xrange(start, end + 1)).difference(L))

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--inputDir", type=str, help="inputDir", required=True)
parser.add_argument("-n", "--nJobs", type=int, help="nJobs", required=True)
args = parser.parse_args()

finish_jobs = []
files = os.popen('ls '+args.inputDir+'/*/*.root').readlines()  
for iFile, file in enumerate(files):
   file_root = file.split('/')[len(file.split('/'))-1] 
   jobId = file_root.split('_') [len(file_root.split('_'))-1]
   jobId = jobId.replace('.root\n','')
   finish_jobs.append(int(jobId))

print finish_jobs

print "Missing jobs: ",missing_elements(finish_jobs)

