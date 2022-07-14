#!/usr/bin/env python3
# create json file for a dataset
import sys, os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dataset', type=str, default='/AlCaPhiSym/Run2018D-v1/RAW')
args = parser.parse_args()

_dataset = args.dataset

json_filename = 'run_file_map_{}.json'.format(_dataset.replace('/','_')[1:])

run_map = {}
files = []

cmd = 'dasgoclient --query "file dataset={}"'.format(_dataset)
files = [ f.strip('\r\n') for f in os.popen(cmd).readlines()]

# check if file are present
if len(files)==0:
        print('No files present in the datset!!')
        sys.exit(2)

for ifile, f in enumerate(files):
        #if ifile>3: break
        cmd = 'dasgoclient --query "run file={}"'.format(f)
        runs = os.popen(cmd).readlines()
        for run in runs:
           run = run.strip('\r\n')
           if run in run_map:
                run_map[run].append(f)
           else:
                run_map[run] = [f]

with open(json_filename, 'w') as _file:
        json.dump(run_map, _file)
