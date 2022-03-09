import FWCore.ParameterSet.Config as cms

EcalTimingEvents= cms.EDProducer("EcalTimingEventProducer",
                    recHitEECollection = cms.InputTag("ecalRecHitEBSelector"),
                    recHitEBCollection = cms.InputTag("ecalRecHitEESelector"),
                    )
