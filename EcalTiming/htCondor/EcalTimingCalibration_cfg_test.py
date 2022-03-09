import FWCore.ParameterSet.Config as cms

process = cms.PSet()

process.ioFilesOpt = cms.PSet(

    ##input file
    inputFile = cms.string('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/AlCaPhiSym/crab_AlCaPhiSym_Run2018D-v1_RAW/220227_184141/0000/timing_reco_selections_2.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/AlCaPhiSym/crab_AlCaPhiSym_Run2018D-v1_RAW/220227_184141/0000/timing_reco_selections_4.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/AlCaPhiSym/crab_AlCaPhiSym_Run2018D-v1_RAW/220227_184141/0000/timing_reco_selections_6.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/AlCaPhiSym/crab_AlCaPhiSym_Run2018D-v1_RAW/220227_184141/0000/timing_reco_selections_7.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/AlCaPhiSym/crab_AlCaPhiSym_Run2018D-v1_RAW/220227_184141/0000/timing_reco_selections_8.root'),
    
    ##input tree
    inputTree = cms.string('/timing/EcalSplashTiming/timingEventsTree'),

    ## base output directory: default output/
    outputDir = cms.string('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/calib_test/'),

    ## base output: default ecalTiming.dat
    outputCalib = cms.string('ecalTiming.dat'),
     
    ## base output: default ecalTiming-corr.dat
    outputCalibCorr = cms.string('ecalTiming-corr.dat'),

    ## base output: default ecalTiming.root
    outputFile = cms.string('ecalTiming.root'),

    ## maxEvents
    maxEvents = cms.untracked.int32(-1)
)

process.calibOpt = cms.PSet(

    ## nSigma
    nSigma = cms.int32(2),

    ## maxRange
    maxRange = cms.int32(10)
    
)

