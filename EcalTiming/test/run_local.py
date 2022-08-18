import os, sys
import errno
import argparse
from datetime import datetime

import numpy as np
import awkward as ak
import pandas as pd

import uproot
import math

import json

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb, to_rgba
from matplotlib import ticker, cm
from matplotlib import colors as clr
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start-run', type=int, help='Starting run', default=355862)
parser.add_argument('-e', '--end-run', type=int, help='Ending run', default=355872)
parser.add_argument('-ns', '--nsigma', type=int, default=2, help='Width of the cut in units of sigma.')
parser.add_argument('-r', '--max-range', type=int, default=10, help='Maximum range of the distribution.')

args = parser.parse_args()

dt = datetime.now()
date = '{:04d}_{:02d}_{:02d}'.format(dt.year, dt.month, dt.day)
#date = '{:02d}_{:02d}_{:04d}'.format(dt.day, dt.month, dt.year)


filelist = []
# get list of files
for run in range(args.start_run, args.end_run+1):
    path = '/eos/cms/store/group/dpg_ecal/alca_ecalcalib/automation_prompt/timing/{}/'.format(run)
    if not os.path.exists(path): continue
    filelist += [ path+f for f in os.listdir(path) if '.root' in f ]

fstr = ','.join(filelist)

with open('EcalTimingCalibration_cfg.py','r') as f:
    lines = f.readlines()

with open('FILELIST_{}_{}'.format(args.start_run,args.end_run), 'w') as f:
    for file in filelist:
        f.write(file)
        f.write('\n')

path_to_output = '/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2022A/Calibration/{}_{}/'.format(args.start_run,args.end_run)

with open('EcalTimingCalibration_cfg_{}_{}.py'.format(args.start_run,args.end_run),'w') as f:
    for line in lines:
        if '<FILELIST>' in line: line = line.replace('<FILELIST>',fstr)
        if '<OUTPUT>' in line: line = line.replace('<OUTPUT>',path_to_output)
        f.write(line)

if not os.path.exists(path_to_output):
    os.system('mkdir {}'.format(path_to_output))
else:
    print("Directory already present.")
    
if not os.path.exists('{}/plots'.format(path_to_output)):
   os.system('mkdir {}/plots'.format(path_to_output))
if not os.path.exists('{}/plots/bad_channels/'.format(path_to_output)):
   os.system('mkdir {}/plots/bad_channels'.format(path_to_output))

# set custom functions
plt.rcParams['axes.linewidth'] = 1.4
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.minor.size'] = 2.5
plt.rcParams['xtick.minor.size'] = 4.0
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['ytick.labelsize'] = 'large'
plt.rcParams['xtick.labelsize'] = 'large'

# define custom cmap
cmap_rainbow = cm.get_cmap('jet', 256)
newcolors = cmap_rainbow(np.linspace(0, 1, 256))
cwhite = np.array([1, 1, 1, 1])
newcolors[:1, :] = cwhite
newcmp = ListedColormap(newcolors)

# arguments
nSigma = args.nsigma
maxRange = args.max_range

path_to_input='/eos/cms/store/group/dpg_ecal/alca_ecalcalib/automation_prompt/timing/'

runlist = []
timing_df_map = {
    'EEP': [],
    'EB': [],
    'EEM': []
}

binning_map = {
    'EB': {
        'xbins': 171,
        'ybins': 360,
        'xrange': [-85.0, 86.0],
        'yrange': [1.0, 361.0],
        'half_binx': 0.5,
        'half_biny': 0.5,
        'centers_x': np.linspace(-84.5, 85.5, 171),
        'centers_y': np.linspace(1.5, 360.5, 360)
    },
    'EEP':{
        'xbins': 100,
        'ybins': 100,
        'xrange': [1.0, 101.0],
        'yrange': [1.0, 101.0],
        'half_binx': 0.5,
        'half_biny': 0.5,
        'centers_x': np.linspace(1.5, 100.5, 100),
        'centers_y': np.linspace(1.5, 100.5, 100)
    },
    'EEM':{
        'xbins': 100,
        'ybins': 100,
        'xrange': [1.0, 101.0],
        'yrange': [1.0, 101.0],
        'half_binx': 0.5,
        'half_biny': 0.5,
        'centers_x': np.linspace(1.5, 100.5, 100),
        'centers_y': np.linspace(1.5, 100.5, 100)
    }
}

# print filenames
print('reading files...')
for ifile, filename in enumerate(filelist):
    run = filename.replace('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/automation_prompt/timing/','')
    run = int(run.split('/')[0])
    if run not in runlist: 
        runlist.append(run)
    try:
        timing_tree = uproot.open(filename)['timing/EcalSplashTiming/timingEventsTree']
    except(OSError):
        print('%s could not be opened!' % filename)
        continue
    print('opened %s' % filename)
    timing_df = timing_tree.arrays(timing_tree.keys())
    try: 
        timing_df_map['EEM'].append(timing_df[timing_df['iz']==-1]) 
    except(ValueError):
        print('could not convert tree in %s!' % filename)
    try: 
        timing_df_map['EB'].append(timing_df[timing_df['iz']==0]) 
    except(ValueError):
        print('could not convert tree in %s!' % filename)
    try: 
        timing_df_map['EEP'].append(timing_df[timing_df['iz']==1]) 
    except(ValueError):
        print('could not convert tree in %s!' % filename)

print('\n\nRunlist: ')
for run in runlist: print('\t%s' % str(run))

occupancy_map = {}
energy_map = {}
average_time_map = {}
time_error_map = {}

for region in ['EB','EEP','EEM']:
    
    xbins = binning_map[region]['xbins']
    ybins = binning_map[region]['ybins']
    xrange = binning_map[region]['xrange']
    yrange = binning_map[region]['yrange']
    half_binx = binning_map[region]['half_binx']
    half_biny = binning_map[region]['half_biny']

    Ax = np.concatenate(([x['ix'] for x in timing_df_map[region][0:]]), axis=0)
    Ay = np.concatenate(([x['iy'] for x in timing_df_map[region][0:]]), axis=0)
    Ax = np.array(Ax)
    Ay = np.array(Ay)
    
    E = np.concatenate(([x['energy'] for x in timing_df_map[region][0:]]), axis=0)
    E = np.array(E)
    E = np.nan_to_num(E, True, -99.)
    
    T = np.concatenate(([x['time'] for x in timing_df_map[region][0:]]), axis=0)
    T = np.array(T)
    T = np.nan_to_num(T, True, 0.)

    Mx = ((binning_map[region]['centers_x'].reshape(xbins,1))*np.ones(ybins)).flatten() 
    My = ((binning_map[region]['centers_y'].reshape(ybins,1))*np.ones(xbins)).T.flatten()

    fill = plt.hist2d(Ax, Ay,
               range=(tuple(xrange), tuple(yrange)), bins=(xbins, ybins))
    
    fill_energy = plt.hist2d(Ax, Ay, weights=E,
                            range=(tuple(xrange), tuple(yrange)), bins=(xbins, ybins))
    
    fill_time = plt.hist2d(Ax, Ay, weights=T,
                          range=(tuple(xrange), tuple(yrange)), bins=(xbins, ybins))
    
    
    occupancy_map[region] = fill
    energy_map[region] = fill_energy
    average_time_map[region] = fill_time
    
    for plot in ['Occupancy', 'Energy', 'Time', 'TimeError']:
        
        unit = ''
        if plot=='Occupancy':
            F = fill[0]
            unit = ''
        elif plot=='Energy':
            F = fill_energy[0]/fill[0]
            unit = ' (GeV)'
        elif plot=='Time':
            F = fill_time[0]/fill[0]
            unit = ' (ns)'
        
        nofill = 0
        F = np.nan_to_num(F, True, 0.)
        
        if 'Time' in plot: cmap_='bwr'
        else:
            cmap_ = newcmp
            nofill = -99.
        
        if region=='EB':
            xlabel_ = 'i$\eta$'
            ylabel_ = 'i$\phi$'
        else:
            xlabel_ = 'ix'
            ylabel_ = 'iy'
        
        plt.clf()
        plt.figure(figsize=(7.7,6.6))

        plt.xlabel(xlabel_, fontsize=14)
        plt.ylabel(ylabel_, fontsize=14)
        plt.title(plot+region+unit, fontsize=16)

        plt.hist2d(Mx, My, weights=F.flatten(),
                   cmap=cmap_, 
                   range=(tuple(xrange), tuple(yrange)), bins=(xbins, ybins))
        
        zmax = max(abs(min(F.flatten())), abs(max(F.flatten())))
        plt.colorbar()
        if 'Time' in plot: plt.clim(-5, 5)       
        else: plt.clim(0, max(F.flatten()))
        plt.savefig('{}/plots/{}_{}.png'.format(path_to_output,plot,region))

plt.clf()
plt.figure(figsize=(6.6,6.6))
plt.hist(average_time_map['EB'][0].flatten()/occupancy_map['EB'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EB', color='tab:blue', linewidth=2, density=True)
plt.hist(average_time_map['EEP'][0].flatten()/occupancy_map['EEP'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EE+', color='tab:orange', linewidth=2, density=True)
plt.hist(average_time_map['EEM'][0].flatten()/occupancy_map['EEM'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EE-', color='tab:green', linewidth=2, density=True)
plt.xlabel('Time (ns)', fontsize=14)
plt.ylabel('a.u.', fontsize=14)
plt.title('Average Time/ crystal', fontsize=16)
plt.legend(loc='upper left', fontsize=14)
plt.savefig('{}/plots/average_time_normalized.png'.format(path_to_output))
plt.close()

plt.clf()
plt.figure(figsize=(6.6,6.6))
plt.hist(average_time_map['EB'][0].flatten()/occupancy_map['EB'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EB', color='tab:blue', linewidth=2, density=False)
plt.hist(average_time_map['EEP'][0].flatten()/occupancy_map['EEP'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EE+', color='tab:orange', linewidth=2, density=False)
plt.hist(average_time_map['EEM'][0].flatten()/occupancy_map['EEM'][0].flatten(), histtype='step', bins=50, range=(-4, 2), label='EE-', color='tab:green', linewidth=2, density=False)
plt.xlabel('Time (ns)', fontsize=14)
plt.ylabel('a.u.', fontsize=14)
plt.title('Average Time/ crystal', fontsize=16)
plt.legend(loc='upper left', fontsize=14)
plt.savefig('{}/plots/average_time.png'.format(path_to_output))

bad_EEP_list = []
bad_EEM_list = []
bad_EB_list = []

for ix, A in enumerate(average_time_map['EB'][0]/occupancy_map['EB'][0]):
    for iy, t in enumerate(A):
        if t<-4 or t>4: bad_EB_list.append((ix+1, iy+1))

for ix, A in enumerate(average_time_map['EEM'][0]/occupancy_map['EEM'][0]):
    for iy, t in enumerate(A):
        if t<-4 or t>4: bad_EEM_list.append((ix+1, iy+1))

for ix, A in enumerate(average_time_map['EEP'][0]/occupancy_map['EEP'][0]):
    for iy, t in enumerate(A):
        if t<-4 or t>4: bad_EEP_list.append((ix+1, iy+1))

region = 'EEP'
time_array = np.concatenate(([x['time'] for x in timing_df_map[region][0:]]), axis=0)
energy_array = np.concatenate(([x['energy'] for x in timing_df_map[region][0:]]), axis=0)
ix_array = np.concatenate(([x['ix'] for x in timing_df_map[region][0:]]), axis=0)
iy_array = np.concatenate(([x['iy'] for x in timing_df_map[region][0:]]), axis=0)
iz_array = np.concatenate(([x['iz'] for x in timing_df_map[region][0:]]), axis=0)

for ieta_, iphi_ in bad_EEP_list:
    print('.')
    rechit_time_array = time_array[(iz_array==1)*(ix_array==ieta_)*(iy_array==iphi_)]
    rechit_time_array = rechit_time_array[~np.isnan(rechit_time_array)]

    std_ = np.std(rechit_time_array)
    mean_ = np.mean(rechit_time_array)

    cropped_rechit_time_array = rechit_time_array[abs(rechit_time_array-mean_)<nSigma*std_]
    shift_ = np.mean(cropped_rechit_time_array)

    plt.clf()
    plt.figure(figsize=(6.6,6.6))
    
    minx = mean_-3*std_
    maxx = mean_+3*std_
    
    if not minx or not maxx:
        print('ieta = {}, iphi = {} has nan range!'.format(ieta_, iphi_))
        continue
    
    try:
        tmphist = plt.hist(rechit_time_array,
             bins=50, range=(minx, maxx), histtype='step',
             color='black', linewidth=2)
    except(ValueError):
        print('ieta = {}, iphi = {} could not be plotted!'.format(ieta_, iphi_))
        continue
    plt.xlabel('RecHit Time [ns]', fontsize=14)
    plt.ylabel('Counts', fontsize=14)
    yhigh_ = 1.05*max(tmphist[0])
    plt.ylim(0, yhigh_)
    plt.plot([shift_, shift_], [0, yhigh_], 'r--', label='shift')
    plt.plot([mean_-nSigma*std_, mean_-nSigma*std_], [0, yhigh_], 'b--',
             label='{}$\sigma$ cut'.format(nSigma))
    plt.plot([mean_+nSigma*std_, mean_+nSigma*std_], [0, yhigh_], 'b--')
    plt.legend(loc='upper right', fontsize=14)
    plt.title('EE+ xtal (ix={}, iy={})'.format(ieta_, iphi_), fontsize=16)
    plt.text(x=minx, y=0.85*yhigh_, s='shift = %0.2f ns' % shift_, fontsize=14)
    plt.xlim(minx, maxx)
    plt.savefig('{}/plots/bad_channels/EEP_xtal_time_ieta_{}_iphi_{}.png'.format(path_to_output, ieta_, iphi_))
    plt.close()

region = 'EEM'
time_array = np.concatenate(([x['time'] for x in timing_df_map[region][0:]]), axis=0)
energy_array = np.concatenate(([x['energy'] for x in timing_df_map[region][0:]]), axis=0)
ix_array = np.concatenate(([x['ix'] for x in timing_df_map[region][0:]]), axis=0)
iy_array = np.concatenate(([x['iy'] for x in timing_df_map[region][0:]]), axis=0)
iz_array = np.concatenate(([x['iz'] for x in timing_df_map[region][0:]]), axis=0)


for ieta_, iphi_ in bad_EEM_list:
    rechit_time_array = time_array[(iz_array==-1)*(ix_array==ieta_)*(iy_array==iphi_)]
    rechit_time_array = rechit_time_array[~np.isnan(rechit_time_array)]

    std_ = np.std(rechit_time_array)
    mean_ = np.mean(rechit_time_array)

    cropped_rechit_time_array = rechit_time_array[abs(rechit_time_array-mean_)<nSigma*std_]
    shift_ = np.mean(cropped_rechit_time_array)

    plt.clf()
    plt.figure(figsize=(6.6,6.6))
    
    minx = mean_-3*std_
    maxx = mean_+3*std_
    
    if not minx or not maxx:
        print('ieta = {}, iphi = {} has nan range!'.format(ieta_, iphi_))
        continue
    
    try:
        tmphist = plt.hist(rechit_time_array,
             bins=50, range=(minx, maxx), histtype='step',
             color='black', linewidth=2)
    except(ValueError):
        print('ieta = {}, iphi = {} could not be plotted!'.format(ieta_, iphi_))
        continue
    plt.xlabel('RecHit Time [ns]', fontsize=14)
    plt.ylabel('Counts', fontsize=14)
    yhigh_ = 1.05*max(tmphist[0])
    plt.ylim(0, yhigh_)
    plt.plot([shift_, shift_], [0, yhigh_], 'r--', label='shift')
    plt.plot([mean_-nSigma*std_, mean_-nSigma*std_], [0, yhigh_], 'b--',
             label='{}$\sigma$ cut'.format(nSigma))
    plt.plot([mean_+nSigma*std_, mean_+nSigma*std_], [0, yhigh_], 'b--')
    plt.legend(loc='upper right', fontsize=14)
    plt.title('EE- xtal (ix={}, iy={})'.format(ieta_, iphi_), fontsize=16)
    plt.text(x=minx, y=0.85*yhigh_, s='shift = %0.2f ns' % shift_, fontsize=14)
    plt.xlim(minx, maxx)
    plt.savefig('{}/plots/bad_channels/EEM_xtal_time_ieta_{}_iphi_{}.png'.format(path_to_output, ieta_, iphi_))
    plt.close()

region = 'EB'
time_array = np.concatenate(([x['time'] for x in timing_df_map[region][0:]]), axis=0)
energy_array = np.concatenate(([x['energy'] for x in timing_df_map[region][0:]]), axis=0)
ix_array = np.concatenate(([x['ix'] for x in timing_df_map[region][0:]]), axis=0)
iy_array = np.concatenate(([x['iy'] for x in timing_df_map[region][0:]]), axis=0)
iz_array = np.concatenate(([x['iz'] for x in timing_df_map[region][0:]]), axis=0)

for ieta_, iphi_ in bad_EB_list:
    rechit_time_array = time_array[(iz_array==0)*(ix_array==ieta_)*(iy_array==iphi_)]
    rechit_time_array = rechit_time_array[~np.isnan(rechit_time_array)]

    std_ = np.std(rechit_time_array)
    mean_ = np.mean(rechit_time_array)

    cropped_rechit_time_array = rechit_time_array[abs(rechit_time_array-mean_)<nSigma*std_]
    shift_ = np.mean(cropped_rechit_time_array)

    plt.clf()
    plt.figure(figsize=(6.6,6.6))
    
    minx = mean_-3*std_
    maxx = mean_+3*std_
    
    if not minx or not maxx:
        print('ieta = {}, iphi = {} has nan range!'.format(ieta_, iphi_))
        continue
    
    try:
        tmphist = plt.hist(rechit_time_array,
             bins=50, range=(minx, maxx), histtype='step',
             color='black', linewidth=2)
    except(ValueError):
        print('ieta = {}, iphi = {} could not be plotted!'.format(ieta_, iphi_))
        continue
    plt.xlabel('RecHit Time [ns]', fontsize=14)
    plt.ylabel('Counts', fontsize=14)
    yhigh_ = 1.05*max(tmphist[0])
    plt.ylim(0, yhigh_)
    plt.plot([shift_, shift_], [0, yhigh_], 'r--', label='shift')
    plt.plot([mean_-nSigma*std_, mean_-nSigma*std_], [0, yhigh_], 'b--',
             label='{}$\sigma$ cut'.format(nSigma))
    plt.plot([mean_+nSigma*std_, mean_+nSigma*std_], [0, yhigh_], 'b--')
    plt.legend(loc='upper right', fontsize=14)
    plt.title('EB xtal (i$\eta$={}, i$\phi$={})'.format(ieta_, iphi_), fontsize=16)
    plt.text(x=minx, y=0.85*yhigh_, s='shift = %0.2f ns' % shift_, fontsize=14)
    plt.xlim(minx, maxx)
    plt.savefig('{}/plots/bad_channels/EB_xtal_time_ieta_{}_iphi_{}.png'.format(path_to_output, ieta_, iphi_))
    plt.close()
'''
os.system('EcalTimingCalibration EcalTimingCalibration_cfg_{}_{}.py'.format(args.start_run,args.end_run))
os.system('mv EcalTimingCalibration_cfg_{}_{}.py {}'.format(args.start_run,args.end_run,path_to_output))
os.system('mv FILELIST_{}_{} {}'.format(args.start_run,args.end_run,path_to_output))
os.system('cp {out}/ecalTiming-corr.dat {out}/ecalTiming-corr_{date}.dat'.format(out=path_to_output, date=date))
os.system('python makeTimingXML.py --tag=EcalTimeCalibConstants_v01_express --calib={}/ecalTiming-corr_{}.dat'.format(path_to_output,date))
os.system('python makeTimingSqlite.py --tag=EcalTimeCalibConstants_Prompt2022_v1 --calib={}/ecalTiming-abs_{}.xml'.format(path_to_output,date))
'''
