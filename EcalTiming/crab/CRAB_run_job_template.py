# -----------------------------------------
# CRAB Job: Created on 2022/2/27 18:28:11 UTC
# -----------------------------------------

try:
  from CRABClient.UserUtilities import config
except ImportError:
  print
  print('ERROR: Could not load CRABClient.UserUtilities.  Please source the crab3 setup:')
  print('source /cvmfs/cms.cern.ch/crab3/crab.sh')
  exit(-1)

config = config()

config.General.requestName = 'AlCaPhiSym_Run<ERA>-v1_RAW_<RUN>'
config.General.workArea = 'crab_projects/Production_<DATE>'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.pyCfgParams = ['outputFile=timing_reco_selections.root', 'globaltag=<GT>' <VALIDATE>]
config.JobType.psetName = 'ecalTime_fromAlcaStream.py'

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 1440
config.JobType.maxMemoryMB = 3200
#config.JobType.sendPythonFolder = True

config.Data.userInputFiles = [<FILES>]

config.Data.inputDBS      = 'global'
config.Data.splitting     = 'FileBased' #'LumiBased' / 'FileBased'
config.Data.unitsPerJob   = <NFILES> #30000
config.Data.outLFNDirBase = '/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run<ERA>_Prompt/'
config.Data.publication   = False
config.Data.allowNonValidInputDataset = True

# GRID
config.Site.storageSite   = 'T2_CH_CERN'
#config.Site.Whitelist     = ['T3_CH_CERN_CAF']
#config.Site.Blacklist     = ['T1_US_FNAL', 'T2_UA_KIPT', 'T2_UK_London_Brunel', 'T2_CH_CSCS', 'T2_US_*']
config.Site.ignoreGlobalBlacklist = False
