from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *

ecalLocalRecoSequenceAlCaStream = cms.Sequence (ecalMultiFitUncalibRecHit * 
                                                    ecalRecHit)

ecalMultiFitUncalibRecHit.EBdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEB")
ecalMultiFitUncalibRecHit.EEdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEE")

ecalMultiFitUncalibRecHit.algoPSet = cms.PSet(
      useLumiInfoRunHeader = cms.bool(False),
      activeBXs = cms.vint32(-5,-4,-3,-2,-1,0,1,2,3,4)
      )

ecalRecHit.killDeadChannels = False
ecalRecHit.recoverEBFE = False
ecalRecHit.recoverEEFE = False
#copied
ecalRecHit.killDeadChannels = cms.bool( False )
ecalRecHit.recoverEBVFE = cms.bool( False )
ecalRecHit.recoverEEVFE = cms.bool( False )
ecalRecHit.recoverEBFE = cms.bool( False )
ecalRecHit.recoverEEFE = cms.bool( False )
ecalRecHit.recoverEEIsolatedChannels = cms.bool( False )
ecalRecHit.recoverEBIsolatedChannels = cms.bool( False )
