import FWCore.ParameterSet.Config as cms

timing = cms.EDFilter("EcalTimingCalibProducer",
                    isSplash = cms.bool(False),
                    makeEventPlots = cms.bool(False),
                    applyAmpThresEB = cms.bool(True),
                    applyAmpThresEE = cms.bool(True),
                    ebUncalibRechits = cms.InputTag("ecalMultiFitUncalibRecHit","EcalUncalibRecHitsEB"),
                    eeUncalibRechits = cms.InputTag("ecalMultiFitUncalibRecHit","EcalUncalibRecHitsEE"),
                    timingCollection = cms.InputTag("EcalTimingEvents"),
                    recHitMinimumN = cms.uint32(2),
                    minRecHitEnergyStep = cms.double(0.5),
                    minRecHitEnergyNStep = cms.double(10),
                    energyThresholdOffsetEB = cms.double(0.0),
                    energyThresholdOffsetEE = cms.double(0.0),
                    ampFrac = cms.double(2.),
                    ampCut_barrelP = cms.vdouble(16.31759, 16.33355, 16.34853, 16.36281, 16.37667, 16.39011, 16.40334, 16.41657, 16.42994, 16.44359, 16.45759, 16.47222, 16.48748, 16.50358, 16.52052, 16.53844, 16.55755, 16.57778, 16.59934, 16.62216, 16.64645, 16.67221, 16.69951, 16.72849, 16.75894, 16.79121, 16.82502, 16.86058, 16.89796, 16.93695, 16.97783, 17.02025, 17.06442, 17.11041, 17.15787, 17.20708, 17.25783, 17.31026, 17.36409, 17.41932, 17.47602, 17.53384, 17.5932, 17.65347, 17.715, 17.77744, 17.84086, 17.90505, 17.97001, 18.03539, 18.10147, 18.16783, 18.23454, 18.30146, 18.36824, 18.43502, 18.50159, 18.56781, 18.63354, 18.69857, 18.76297, 18.82625, 18.88862, 18.94973, 19.00951, 19.06761, 19.12403, 19.1787, 19.23127, 19.28167, 19.32955, 19.37491, 19.41754, 19.45723, 19.49363, 19.52688, 19.55642, 19.58218, 19.60416, 19.62166, 19.63468, 19.64315, 19.64665, 19.6449, 19.6379), #ADC noise + 2ADC
                    ampCut_barrelM = cms.vdouble(16.31759, 16.33355, 16.34853, 16.36281, 16.37667, 16.39011, 16.40334, 16.41657, 16.42994, 16.44359, 16.45759, 16.47222, 16.48748, 16.50358, 16.52052, 16.53844, 16.55755, 16.57778, 16.59934, 16.62216, 16.64645, 16.67221, 16.69951, 16.72849, 16.75894, 16.79121, 16.82502, 16.86058, 16.89796, 16.93695, 16.97783, 17.02025, 17.06442, 17.11041, 17.15787, 17.20708, 17.25783, 17.31026, 17.36409, 17.41932, 17.47602, 17.53384, 17.5932, 17.65347, 17.715, 17.77744, 17.84086, 17.90505, 17.97001, 18.03539, 18.10147, 18.16783, 18.23454, 18.30146, 18.36824, 18.43502, 18.50159, 18.56781, 18.63354, 18.69857, 18.76297, 18.82625, 18.88862, 18.94973, 19.00951, 19.06761, 19.12403, 19.1787, 19.23127, 19.28167, 19.32955, 19.37491, 19.41754, 19.45723, 19.49363, 19.52688, 19.55642, 19.58218, 19.60416, 19.62166, 19.63468, 19.64315, 19.64665, 19.6449, 19.6379), #ADC noise + 2ADC
                    ampCut_endcapP = cms.vdouble(16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0), #ADC noise + 2ADC
                    ampCut_endcapM = cms.vdouble(16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0), #ADC noise + 2ADC
                    eThresholdsEB_par0 = cms.vdouble(0.759103, 0.759103), #fit of Run2018D energy (EB-, EB+) 
                    eThresholdsEB_par1 = cms.vdouble(-4.24162e-05, -4.24162e-05), #fit of Run2018D energy (EB-, EB+) 
                    eThresholdsEB_par2 = cms.vdouble(4.27113e-05, 4.27113e-05), #fit of Run2018D energy (EB-, EB+) 
                    eThresholdsEE_par0 = cms.vdouble(1.40137, 28.6184), #fit of Run2018D energy (EE ring<29, EE ring>=29) 
                    eThresholdsEE_par1 = cms.vdouble(0.00613101, -2.0534), #fit of Run2018D energy (EE ring<29, EE ring>=29)  
                    eThresholdsEE_par2 = cms.vdouble(0.00155616, 0.0406052), #fit of Run2018D energy (EE ring<29, EE ring>=29)  
                    minEntries = cms.uint32(1),
                    globalOffset = cms.double(0.),
                    storeEvents = cms.bool(False),
                    produceNewCalib = cms.bool(True),
                    outputDumpFile = cms.string('output.dat'),
                    maxSkewnessForDump = cms.double(2),
                    )
