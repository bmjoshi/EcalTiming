import os, sys, gc
import getopt

import ecalic as ecal

import subprocess
from ROOT import TXMLEngine, XMLDocPointer_t, XMLNodePointer_t, Int_t
from ROOT import TFile, TTree
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

def writeCalibXML(filename, eb_abs_calib, ee_abs_calib, eb_global_shift_=0.0, ee_global_shift_=0.0):
    ebclass_begin_txt = '''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <!DOCTYPE boost_serialization>
    <boost_serialization signature="serialization::archive" version="19">
    <cmsCondPayload class_id="0" tracking_level="0" version="0">
        <eb- class_id="1" tracking_level="0" version="0">
            <m_items>
                <count>61200</count>
                <item_version>0</item_version>
    '''
    eeclass_end_txt = '''        </m_items>
        </ee->
    </cmsCondPayload>
    </boost_serialization>
    '''
    ebclass_end_txt = '''        </m_items>
        </eb->
        <ee- class_id="3" tracking_level="0" version="0">
            <m_items>
                <count>14648</count>
                <item_version>0</item_version>
                
    '''
    with open(filename, 'w+') as f0:
        f0.write(ebclass_begin_txt)
        for val in eb_abs_calib:
            f0.write('\t\t\t\t<item>{:0.9E}</item>\n'.format(val-eb_global_shift_))
        f0.write(ebclass_end_txt)
        for val in ee_abs_calib:
            f0.write('\t\t\t\t<item>{:0.9E}</item>\n'.format(val-ee_global_shift_))
        f0.write(eeclass_end_txt)

def usage():
    print("Usage: python makeTimingXML.py --tag=[tag] --calib=[calib]")
    print("Usage: python makeTimingXML.py --payload=[payload] --calib=[calib]")
    print("""Make sure that the payload is specified if corrections are to updated with respect to previous entries.
Otherwise the script will use the payload from the latest entry in the conditions database corresponding the to the specified tag.""")
    
try:
     opts, args = getopt.getopt(sys.argv[1:], "t:i:c:p:h", ["tag=","calib=","payload=","help"])

except getopt.GetoptError:
     #* print help information and exit:*
     usage()
     sys.exit(2)

tag = ""
calib = ""
payload = ""
help = False
for opt, arg in opts:
     if opt in ("--tag"):
        tag = arg
     if opt in ("--calib"):
        calib = arg
     if opt in ("--payload"):
        payload = arg    
     if opt in ("--help"):
        help = True     

for opt, arg in opts:
    print(opt, arg)


if(help == True):
   usage()
   sys.exit(2)

goodMode = False

if ( not ( tag=="" and payload==""))  and calib!="":
   goodMode = True
if not goodMode:
   usage()
   sys.exit(2)

if(tag != ""):
   print("tag          = ",tag)
if(payload != ""):
   print("payload      = ",payload)
if(calib != ""):
   print("calib        = ",calib)

IOVs_date = []
IOVs_time = []
IOVs_info = []

#dump IOVs xml
print("---- Dumping IOVs info ----")

if(payload != ""):
   print("---> Dumping the pyload: ",payload)
   command = os.system("conddb dump "+ str(payload) +" > dump_tmp")
else:
   command = """
   conddb list EcalTimeCalibConstants_v01_prompt | tail -2 | head -1 &> tmp;
   cat tmp | cut -d$" " -f11 > tmppyload;
   rm tmp;
   conddb dump $(cat tmppyload) > dump_tmp;
   rm tmppyload;
   """
   os.system(command)

df = pd.read_csv(calib, header=None, delimiter='\t')
df.columns = ['ix','iy','iz','mean','std','n','tmp', 'cmsswId']
df = df.set_index('cmsswId')

with open('deadcrystalsEB.txt','r') as f_:
    deadEB_lines = f_.readlines()
deadEB_lines = [ l.strip('\r\n').split('\t') for l in deadEB_lines if l!='']

with open(str(calib)) as f_interCalib:
    data_interCalib = f_interCalib.readlines()
lines_interCalib = [ l.strip('\n\r').split('\t') for l in data_interCalib ]

timing_ic = ecal.xml('dump_tmp').icCMS().set_index('cmsswId')
timing_ic['new_calib'] = timing_ic['ic']
timing_ic = timing_ic.join(df['mean'])
timing_ic['new_calib'] -= timing_ic['mean']
nan_corr = np.isnan(timing_ic['new_calib'])
timing_ic['new_calib'].fillna(timing_ic['ic'], inplace=True)

redCol = ['hashedId','ix','iy','iz','FED','ccu']
large_corr = abs(timing_ic['new_calib'].values)>20
print('------------------------------------------------------')
print('             NAN Entries                 ')
print('------------------------------------------------------')
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(timing_ic[redCol][nan_corr])
print('------------------------------------------------------')
print('WARNING: Large corrections (setting to previous value)')
print('------------------------------------------------------')
print(timing_ic[redCol][large_corr])
print('-----------------------------------------')


eb_abs_calib = timing_ic['new_calib'][timing_ic['iz']==0].values
ee_abs_calib = timing_ic['new_calib'][timing_ic['iz']!=0].values

filename = calib.replace("corr","abs")
filename = filename.replace(".dat",".xml")
writeCalibXML(filename, eb_abs_calib, ee_abs_calib)

os.system("rm dump_tmp")
