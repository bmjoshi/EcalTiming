bad_channels = []

with open('list_large_negative_shifts_ee.dat','r') as f:
    ch = f.readlines()
    for l in ch:
        l = l.replace('\n','')
        l = l.replace(' ','\t')
        if l[-1]!='\t': l+= '\t'
        bad_channels.append(l)


with open('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2022A/Calibration/355862/ecalTiming-corr.dat', 'r') as f:
    prev = f.readlines()

with open('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2022A/Calibration/356371//ecalTiming-corr_2022_07_29.dat','rb') as f:
    curr = f.readlines()

prev_vals = {}
curr_vals = {}

for il, l in enumerate(curr):
    for ch in bad_channels:
        if ch in l: curr_vals[ch] = l.split('\t')[3].strip('\t')

for il, l in enumerate(prev):
    for ch in bad_channels:
        if ch in l: prev_vals[ch] = l.split('\t')[3].strip('\t')

keys = []
for ch in curr_vals.keys()+prev_vals.keys():
    if ch not in keys: keys.append(ch)

for ch in keys:
    
    if ch not in curr_vals: curr_vals[ch] = '-0'
    if ch not in prev_vals: prev_vals[ch] = '-0'

    out = '{}\t{}\t{}'.format(ch,prev_vals[ch],curr_vals[ch])
    out = out.replace('\t\t','\t')
    print(out)
