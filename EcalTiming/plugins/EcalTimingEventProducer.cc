// -*- C++ -*-
//
// Package:    EcalTiming/EcalTimingEventProducer
// Class:      EcalTimingEventProducer
// 
/**\class EcalTimingEventProducer EcalTimingEventProducer.cc EcalTiming/EcalTimingEventProducer/plugins/EcalTimingEventProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Peter Hansen
//         Created:  Tue, 21 Jul 2015 09:35:32 GMT
//
//


// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "EcalTiming/EcalTiming/interface/EcalTimingEvent.h"

//
// class declaration
//

class EcalTimingEventProducer : public edm::EDProducer {
   public:
      explicit EcalTimingEventProducer(const edm::ParameterSet&);
      ~EcalTimingEventProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
		edm::EDGetTokenT<EBRecHitCollection> _ecalRecHitsEBtoken;
		edm::EDGetTokenT<EERecHitCollection> _ecalRecHitsEEtoken;
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
EcalTimingEventProducer::EcalTimingEventProducer(const edm::ParameterSet& iConfig):
	_ecalRecHitsEBtoken(consumes<EBRecHitCollection>(iConfig.getParameter<edm::InputTag>("recHitEBCollection"))),
	_ecalRecHitsEEtoken(consumes<EERecHitCollection>(iConfig.getParameter<edm::InputTag>("recHitEECollection")))
{
   //register your products
   produces<EcalTimingCollection>();
}


EcalTimingEventProducer::~EcalTimingEventProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EcalTimingEventProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
	// here the getByToken of the rechits
	edm::Handle<EcalRecHitCollection> RecHitEBHandle;
	iEvent.getByToken(_ecalRecHitsEBtoken, RecHitEBHandle);
	edm::Handle<EcalRecHitCollection> RecHitEEHandle;
	iEvent.getByToken(_ecalRecHitsEEtoken, RecHitEEHandle);

        std::unique_ptr<EcalTimingCollection> timing_out(new EcalTimingCollection());

	for(auto  recHit_itr : *RecHitEBHandle) {
		timing_out->push_back(EcalTimingEvent(recHit_itr));
	}
	for(auto  recHit_itr : *RecHitEEHandle) {
		timing_out->push_back(EcalTimingEvent(recHit_itr));
	}

   iEvent.put(std::move(timing_out));

/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
EcalTimingEventProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EcalTimingEventProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
EcalTimingEventProducer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
EcalTimingEventProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
EcalTimingEventProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
EcalTimingEventProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EcalTimingEventProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("recHitEECollection");
  desc.add<edm::InputTag>("recHitEBCollection");
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EcalTimingEventProducer);
