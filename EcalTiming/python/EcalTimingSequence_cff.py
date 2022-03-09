from EcalTiming.EcalTiming.RecHitsSelector_cfi import *
from EcalTiming.EcalTiming.EcalTimingEventProducer_cfi import *

EcalTimingEventSeq = cms.Sequence((ecalRecHitEBSelector + ecalRecHitEESelector) * EcalTimingEvents)
