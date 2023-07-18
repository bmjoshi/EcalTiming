import os
from random import random
from datetime import datetime
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mode',type=str,help="compute/validate; validate will need an sqlite file")
parser.add_argument('-s','--start-run',type=str,default=367406)
parser.add_argument('-e','--end-run',type=str,default=367416)
parser.add_argument('-gt','--global-tag',type=str,default='130X_dataRun3_Prompt_v3')
parser.add_argument('--era',type=str,default='Test')
parser.add_argument('-sq','--sqlite-file',type=str,default='ecalTiming-abs.db')
parser.add_argument('-d', '--das',type=str,default='yes')
args = parser.parse_args()
print(args.mode)
if args.mode not in ["validate","compute"]:
    print("check the mode!")
    exit(2);

template_file = 'CRAB_run_job_template.py'
with open(template_file, 'r') as f0:
    tmp_lines = f0.readlines()

#os.system('./clear.sh')

tstamp = datetime.now()
date = '{}{}{}{}{}{}'.format(tstamp.day,tstamp.month,tstamp.year,tstamp.hour,tstamp.minute,tstamp.second)

if args.das=='yes':
    cmd = 'dasgoclient --query "file dataset=/AlCaPhiSym/Run2023C-v1/RAW run in ['
    for i in range(int(args.start_run),int(args.end_run)+1):
        cmd += '%s' % str(i)
        if i!=int(args.end_run): cmd+=','
    cmd += ']" -json > das_query.json'
    print(cmd)
    os.system(cmd)


    with open('das_query.json','r') as f_:
        filemap = json.load(f_)
    runmap = {}
    size = len(filemap)
    for i in range(size):
        run = filemap[i]['file'][0]['run_num']
        file = filemap[i]['file'][0]['name']
    if run not in runmap:
        runmap[run] = []
    runmap[run].append(file)

else:
    runmap = {}
    with open('das_query.json','r') as f_:
        runmap = json.load(f_)[0]

print(runmap)

for run in runmap:
   lines = [l for l in tmp_lines]
   files = '","'.join(runmap[run])
   files = '"'+files+'"'
   nfiles = len(runmap[run])
   with open('crab_Production_{}_{}.py'.format(date, run), 'w') as f0:
      for line in lines:
          if '<DATE>' in line: line = line.replace('<DATE>', date)
          if '<RUN>' in line: line = line.replace('<RUN>', str(run))
          if '<GT>' in line: line = line.replace('<GT>', args.global_tag)
          if '<ERA>' in line: line = line.replace('<ERA>', args.era)
          if '<NFILES>' in line: line = line.replace('<NFILES>', '1')
          if '<FILES>' in line: line = line.replace('<FILES>', files)
          if '<VALIDATE>' in line:
             if args.mode=='validate':
                  line = line.replace('<VALIDATE>', ",'useCustomTimeCalib=True', 'sqliteRecord=sqlite_file:src/EcalTiming/EcalTiming/data/templates/{}'".format(args.sqlite_file))
             else:
                 line = line.replace('<VALIDATE>','')
          if '<FILES>' in line: line = line.replace('<FILES>', files)
          f0.write(line)
   print('crab submit -c crab_Production_{}_{}.py'.format(date, run))
