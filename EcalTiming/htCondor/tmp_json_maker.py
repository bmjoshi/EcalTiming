import json
runfile = 'runlist_AlCaPhiSym_Run2018D-v1_RAW.dat'
flistfile = 'filelist_AlCaPhiSym_Run2018D-v1_RAW.dat'

with open(runfile, 'r') as _file:
        runlist = [ r.strip('\r\n') for r in _file.readlines() ]

with open(flistfile, 'r') as _file:
        files = [ f.strip('\r\n') for f in _file.readlines()]

if len(runlist)!=len(files):
        print('Length of files not equal!!')

map = {}
for irun, r in enumerate(runlist):
        if r in map:
                map[r].append(files[irun])
        else:
                map[r] = [files[irun]]


with open('run_file_map_AlCaPhiSym_Run2018D-v1_RAW.json', 'w') as _file:
        json.dump(map, _file)
