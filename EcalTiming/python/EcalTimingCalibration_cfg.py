import FWCore.ParameterSet.Config as cms

process = cms.PSet()

process.ioFilesOpt = cms.PSet(

    ##input file
    inputFile = cms.string('/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320497/timing_reco_selections_320497_7.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_10.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_11.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_12.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_13.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_14.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_15.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320500/timing_reco_selections_320500_9.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_16.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_17.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_18.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_19.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_20.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_21.root,/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy//320557/timing_reco_selections_320557_22.root'),
    
    ##input tree
    inputTree = cms.string('/timing/EcalSplashTiming/timingEventsTree'),

    ## base output directory: default output/
    outputDir = cms.string(''),

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

