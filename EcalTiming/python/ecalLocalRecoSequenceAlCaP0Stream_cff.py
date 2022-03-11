from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *

ecalLocalRecoSequenceAlCaP0Stream = cms.Sequence (ecalMultiFitUncalibRecHit * 
                                                        ecalRecHit)

ecalMultiFitUncalibRecHit.cpu.EBdigiCollection = cms.InputTag("dummyHits","dummyBarrelDigis")
ecalMultiFitUncalibRecHit.cpu.EEdigiCollection = cms.InputTag("dummyHits","dummyEndcapDigis")


#ecalDetIdToBeRecovered =  RecoLocalCalo.EcalRecProducers.ecalDetIdToBeRecovered_cfi.ecalDetIdToBeRecovered.clone()
ecalRecHit.cpu.killDeadChannels = cms.bool( False )
ecalRecHit.cpu.recoverEBVFE = cms.bool( False )
ecalRecHit.cpu.recoverEEVFE = cms.bool( False )
ecalRecHit.cpu.recoverEBFE = cms.bool( False )
ecalRecHit.cpu.recoverEEFE = cms.bool( False )
ecalRecHit.cpu.recoverEEIsolatedChannels = cms.bool( False )
ecalRecHit.cpu.recoverEBIsolatedChannels = cms.bool( False )
