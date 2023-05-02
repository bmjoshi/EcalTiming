import os
from random import random
from datetime import datetime

template_file = 'CRAB_run_job_template.py'
with open(template_file, 'r') as f0:
    tmp_lines = f0.readlines()

globaltag = '130X_dataRun3_Prompt_v2'

tstamp = datetime.now()
date = '{}{}{}{}{}{}'.format(tstamp.day,tstamp.month,tstamp.year,tstamp.hour,tstamp.minute,tstamp.second)

runmap = {'366873': ['/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/873/00000/0a336950-1fbb-46be-bd5a-be8bc0f74c81.root',
'/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/873/00000/40460202-5f38-44a0-b560-2cbc184db6c8.root',
'/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/873/00000/5e544884-2f1b-4e6a-81fe-766ed8f47864.root',
'/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/873/00000/8241a5f3-cd31-4101-9d76-d4da2e40691c.root',
'/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/873/00000/e26172e6-c4c3-4f99-b832-ac9770f13a91.root'],
'366874': ['/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/874/00000/803eb188-30f5-4481-871c-e95b2f585584.root'],
'366891': ['/store/data/Run2023B/AlCaPhiSym/RAW/v1/000/366/891/00000/edc1a8b0-3e25-4e6b-8b79-c4fffe2f501d.root']
}

for run in runmap:
   lines = [l for l in tmp_lines]
   files = '","'.join(runmap[run])
   files = '"'+files+'"'
   nfiles = len(runmap[run])
   with open('crab_Production_{}_{}.py'.format(date, run), 'w') as f0:
      for line in lines:
          if '<DATE>' in line: line = line.replace('<DATE>', date)
          if '<RUN>' in line: line = line.replace('<RUN>', run)
          if '<GT>' in line: line = line.replace('<GT>', globaltag)
          if '<NFILES>' in line: line = line.replace('<NFILES>', '1')
          if '<FILES>' in line: line = line.replace('<FILES>', files)
          f0.write(line)
   print('crab submit -c crab_Production_{}_{}.py'.format(date, run))
