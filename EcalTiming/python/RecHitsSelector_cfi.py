import FWCore.ParameterSet.Config as cms

ecalRecHitEBSelector= cms.EDProducer("RecHitSelector",
                    recHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                    recHitFlags = cms.vint32([0]), # only recHits with these flags are accepted for calibration
                    minRecHitEnergy = cms.double(0.5),
                    maxTimeError = cms.double(3.0),
                    maxChi2 = cms.double(50.0),
                    )

ecalRecHitEESelector= cms.EDProducer("RecHitSelector",
                    recHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                    recHitFlags = cms.vint32([0]), # only recHits with these flags are accepted for calibration
                    minRecHitEnergy = cms.double(0.5),
                    maxTimeError = cms.double(3.0),
                    maxChi2 = cms.double(50.0),
                    )
