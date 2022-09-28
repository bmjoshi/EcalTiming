import sys
from matplotlib import pyplot as plt
import numpy as np


filename = sys.argv[1]+'/ecalTiming-corr.dat'

runs = filename.replace('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2022A/Calibration/','')
runs = runs.split('/')[0]
runs = runs.split('_')

with open(filename, 'r') as f:
    lines = f.readlines()

lines = [ l.strip('\r\n').split('\t') for l in lines ]

eb_corrections = []
eep_corrections = []
eem_corrections = []

eb_ix = []
eb_iy = []
eep_ix = []
eep_iy = []
eem_ix = []
eem_iy = []

for l in lines:
    if l[2]=='0':
        eb_corrections.append(float(l[3]))
        eb_ix.append(int(l[0]))
        eb_iy.append(int(l[1]))
    elif l[2]=='1':
        eep_corrections.append(float(l[3]))
        eep_ix.append(int(l[0]))
        eep_iy.append(int(l[1]))
    elif l[2]=='-1':
        eem_corrections.append(float(l[3]))
        eem_ix.append(int(l[0]))
        eem_iy.append(int(l[1]))

plt.clf()
plt.figure(figsize=(6.6,6.6))
h1 = plt.hist(eb_corrections, histtype='step', bins=50, range=(-4, 2), label='EB', color='tab:blue', linewidth=2, density=True)
h2 = plt.hist(eep_corrections, histtype='step', bins=50, range=(-4, 2), label='EE+', color='tab:orange', linewidth=2, density=True)
h3 = plt.hist(eem_corrections, histtype='step', bins=50, range=(-4, 2), label='EE-', color='tab:green', linewidth=2, density=True)
plt.xlabel('Time (ns)', fontsize=14)
plt.ylabel('a.u.', fontsize=14)
plt.title('Average Time/ crystal ({}-{})'.format(runs[0],runs[1]), fontsize=16)
plt.legend(loc='upper left', fontsize=14)
maxy = max(np.concatenate((h1[0],h2[0],h3[0])))
plt.text(x=-4, y=maxy*0.5, s='EB (mean)={:.2f} ns'.format(np.mean(np.array(eb_corrections)[~np.isnan(eb_corrections)])))
plt.text(x=-4, y=maxy*0.5*(1.75/2), s='EE+ (mean)={:.2f} ns'.format(np.mean(np.array(eep_corrections)[~np.isnan(eep_corrections)])))
plt.text(x=-4, y=maxy*0.5*(1.5/2), s='EE- (mean)={:.2f} ns'.format(np.mean(np.array(eem_corrections)[~np.isnan(eem_corrections)])))
plt.savefig(sys.argv[1]+'/corrections.png')
#plt.show()
