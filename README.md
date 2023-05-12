EcalTiming
================

1) Install:

```
cmsrel CMSSW_13_0_3
cd CMSSW_13_0_3/src
cmsenv
git clone git@github.com:bmjoshi/EcalTiming.git  
git checkout -b Run3_CMSSW_13_X
scram b -j 10
```

2) Run local:

```
cd EcalTiming/EcalTiming/
cmsRun test/ecalTime_fromAlcaStream_cfg.py files=root://cms-xrd-global.cern.ch//store/data/Run2023C/AlCaPhiSym/RAW/v1/000/367/260/00000/6612587f-87e5-4228-943f-30505384b0b0.root globaltag=130X_dataRun3_v2
```
 NOTE: the outputs are produced in one step and CANNOT BE MERGED with other outputs.
    
3) Run on parallel (using HTCondor):

launch 1st step (selection step):
```
cd EcalTiming/EcalTiming/htCondor/
voms-proxy-init --voms cms --valid 168:00 #copy proxy to your /afs/cern.ch/user/{user}/{user}/
python condor_timing_selections.py -d /AlCaPhiSym/Run2018D-v1/RAW -gt 106X_dataRun2_v28 -o /store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/ -c /afs/cern.ch/work/b/bmarzocc/ECAL_TIMING_New/CMSSW_10_6_14 -q tomorrow -p x509up_u35923 -m 5000  # -b 323513 -e 323545
condor_submit condor_job.txt
```
launch 2nd step (calibration step):
```
cd EcalTiming/EcalTiming/htCondor/
python condor_timing_calib.py -i /eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/ -l input_List_2018D.txt -o /eos/cms//store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Calib/ -c /afs/cern.ch/work/b/bmarzocc/ECAL_TIMING_New/CMSSW_10_6_14 -q workday
condor_submit condor_job.txt
```
4) Produce the sql tag file:

The output of the calibration needs to have the following name format:

```
  python EcalTiming/EcalTiming/test/add_Date_toCorr.py -i input_List_2018_RunD_UL.dat #ecalTiming-corr.dat -> ecalTiming-corr_2017_09_26.dat
```
Produce the absolute time calibration (xml file) from the latest IOV:
```
  cd EcalTiming/EcalTiming/test/
  eg: python makeTimingXML.py --tag=EcalTimeCalibConstants_v01_express --inList=input_List_2017.dat
  eg: python makeTimingXML.py --tag=EcalTimeCalibConstants_v01_express --calib=/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2017E/Calibration/303948/ecalTiming-corr_2017_09_26.dat
  eg: python makeTimingXML.py --payload=2cc0da4e6a1ec506d037aa476e76bca8ac9ab9fb --inList=input_List_2017.dat
  eg: python makeTimingXML.py --payload=2cc0da4e6a1ec506d037aa476e76bca8ac9ab9fb --calib=/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2017E/Calibration/303948/ecalTiming-corr_2017_09_26.dat
```
Produce the sqlite file from the absolute timing xml file:
```
  cd EcalTiming/EcalTiming/test/
  eg: python makeTimingSqlite.py --calib=/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2017E/Calibration/303948/ecalTiming-abs_2017_09_26.xml --tag=EcalTimeCalibConstants_Legacy2017_v1
  eg: python makeTimingSqlite.py --inList=input_List_2017_absTiming.dat --tag=EcalTimeCalibConstants_Legacy2017_v1 
  sh launch_tagCreation.sh
```
5) Make history plot:
```   
cd EcalTiming/EcalTiming/test/
eg: python makeHistoryPlot.py --tag=EcalTimeCalibConstants_v01_express --year=2017
eg: python makeHistoryPlot.py --inList=input_List_2017.dat
eg: python makeHistoryPlot.py --inList=input_List_2017.dat --runBased
eg: python makeHistoryPlot.py --inList=input_List_2017_RunE.dat --epoch=E
eg: python makeHistoryPlot.py --inList=input_List_2017_absTiming.dat --absTime
``` 
