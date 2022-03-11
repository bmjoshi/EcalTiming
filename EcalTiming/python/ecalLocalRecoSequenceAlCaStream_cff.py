from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *

ecalLocalRecoSequenceAlCaStream = cms.Sequence (ecalMultiFitUncalibRecHitTask, ecalRecHitTask)

ecalMultiFitUncalibRecHit.cpu.EBdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEB")
ecalMultiFitUncalibRecHit.cpu.EEdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEE")

ecalMultiFitUncalibRecHit.cpu.algoPSet = cms.PSet(
      useLumiInfoRunHeader = cms.bool(False),
      activeBXs = cms.vint32(-5,-4,-3,-2,-1,0,1,2,3,4)
      )

ecalRecHit.cpu.killDeadChannels = False
ecalRecHit.cpu.recoverEBFE = False
ecalRecHit.cpu.recoverEEFE = False
#copied
ecalRecHit.cpu.killDeadChannels = cms.bool( False )
ecalRecHit.cpu.recoverEBVFE = cms.bool( False )
ecalRecHit.cpu.recoverEEVFE = cms.bool( False )
ecalRecHit.cpu.recoverEBFE = cms.bool( False )
ecalRecHit.cpu.recoverEEFE = cms.bool( False )
ecalRecHit.cpu.recoverEEIsolatedChannels = cms.bool( False )
ecalRecHit.cpu.recoverEBIsolatedChannels = cms.bool( False )
