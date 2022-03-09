// -*- C++ -*-
//
// Package:    ECALlite/DummyRechitDigis
// Class:      DummyRechitDigis
// 
/**\class DummyRechitDigis DummyRechitDigis.cc ECALlite/DummyRechitDigis/plugins/DummyRechitDigis.cc
 Description: [one line class summary]
 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Joshua Robert Hardenbrook
//         Created:  Mon, 01 Jun 2015 06:58:24 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/CaloRecHit/interface/CaloID.h"
#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"

#include "CondFormats/EcalObjects/interface/EcalSampleMask.h"

#include "EcalTiming/EcalTiming/plugins/EcalTimingCalibProducer.h"

//
// class declaration
//

class DummyRechitDigis : public edm::EDProducer {
public:
  explicit DummyRechitDigis(const edm::ParameterSet&);
  ~DummyRechitDigis();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
      
  // ----------member data ---------------------------
  edm::InputTag tag_barrelHitProducer_;
  edm::InputTag tag_endcapHitProducer_;
  const std::string barrelRecHitCollection_;
  const std::string endcapRecHitCollection_;
  edm::InputTag tag_barrelDigiProducer_;
  edm::InputTag tag_endcapDigiProducer_;
  const std::string barrelDigiCollection_;
  const std::string endcapDigiCollection_;
  const bool doDigi_;
};

DummyRechitDigis::DummyRechitDigis(const edm::ParameterSet& iConfig):
  tag_barrelHitProducer_       (iConfig.getParameter< edm::InputTag > ("barrelHitProducer")),
  tag_endcapHitProducer_       (iConfig.getParameter< edm::InputTag > ("endcapHitProducer")),
  barrelRecHitCollection_  (iConfig.getUntrackedParameter<std::string>("barrelRecHitCollection")),
  endcapRecHitCollection_  (iConfig.getUntrackedParameter<std::string>("endcapRecHitCollection")),
  tag_barrelDigiProducer_      (iConfig.getParameter< edm::InputTag > ("barrelDigis")),
  tag_endcapDigiProducer_      (iConfig.getParameter< edm::InputTag > ("endcapDigis")),
  barrelDigiCollection_ (iConfig.getUntrackedParameter<std::string>("barrelDigiCollection")),
  endcapDigiCollection_ (iConfig.getUntrackedParameter<std::string>("endcapDigiCollection")),
  doDigi_ (iConfig.getUntrackedParameter<bool>("doDigi"))
{
  if(doDigi_) { 
    produces< EBDigiCollection >(barrelDigiCollection_);
    produces< EEDigiCollection >(endcapDigiCollection_);
  }
  else {
    produces< EcalRecHitCollection >(barrelRecHitCollection_);
    produces< EcalRecHitCollection >(endcapRecHitCollection_);
  }
}

DummyRechitDigis::~DummyRechitDigis(){ }

void DummyRechitDigis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){
  //std::cout << "\n-----------New Event ----------------\n " << std::endl;
  using namespace edm;   
  // build an empty collection
  // fake rechits
  // handle to try to fill
  edm::Handle<EcalRecHitCollection> barrelRecHitsHandle;
  edm::Handle<EcalRecHitCollection> endcapRecHitsHandle;
  // dummy collection to Put()
  auto rechits_temp = std::make_unique<EcalRecHitCollection>();
  auto rechits_temp2 = std::make_unique<EcalRecHitCollection>();  

  //   EcalRecHit::EcalRecHit(const DetId& id, float energy, float time, uint32_t flags, uint32_t flagBits)
  // add one rechit
  EcalRecHit zero_rechit(0,0,0,0,0);
  EcalRecHitCollection zero_collection;
  zero_collection.push_back(zero_rechit);
  *rechits_temp  = zero_collection;
  *rechits_temp2 = zero_collection;

  auto rechits_eb = std::make_unique<EcalRecHitCollection>();
  auto rechits_ee = std::make_unique<EcalRecHitCollection>();  

  // fake digis
  // handle to try to fill
  Handle<EBDigiCollection> digisEBHandle;
  Handle<EEDigiCollection> digisEEHandle;
  // dummy collection to Put()
  auto outputEBDigiCollection = std::make_unique<EBDigiCollection>();
  auto outputEEDigiCollection = std::make_unique<EEDigiCollection>();  

  //Digi zero_digi;
  EBDigiCollection ebfakecol;
  EEDigiCollection eefakecol;
  //ebfakecol.push_back(zerodigi);
  //eefakecol.push_back(zerodigi);

  // fake empty collections
  auto fakeEBDigiCollection = std::make_unique<EBDigiCollection>();
  *fakeEBDigiCollection = ebfakecol;
  auto fakeEEDigiCollection = std::make_unique<EEDigiCollection>();
  *fakeEEDigiCollection = eefakecol;

  if(!doDigi_) { 
    bool foundEBRechit = true;
    bool foundEERechit = true;
    std::cout<<"sono entrato nel !dodigi"<<std::endl;

    // if you dont find the barrel rechits youre looking for, put in a fake one
    try { 
      iEvent.getByLabel(tag_barrelHitProducer_, barrelRecHitsHandle);
      *rechits_eb = *(barrelRecHitsHandle.product());    
      for (auto recHit_itr = barrelRecHitsHandle->begin(); recHit_itr != barrelRecHitsHandle->end(); ++recHit_itr){
          std::cout<<"sono entrato nell'if eb"<<std::endl;
      }
    }
    catch(cms::Exception& ex) { foundEBRechit = rechits_eb->size() > 0;}     
    // if you found the collection put it back into the event
    iEvent.put( foundEBRechit ? std::move(rechits_eb) : std::move(rechits_temp), barrelRecHitCollection_);
     
    // if you dont find the endcap rechits youre looking for, put in a fake one
    try {
      //std::cout<<"sono entrato nell'if ee dodigi"<<std::endl;
      iEvent.getByLabel(tag_endcapHitProducer_, endcapRecHitsHandle);
      *rechits_ee = *(endcapRecHitsHandle.product());
    } 
    catch (cms::Exception& ex){ foundEERechit = rechits_ee->size() > 0;
    } 

    iEvent.put( foundEERechit ? std::move(rechits_ee) : std::move(rechits_temp2), endcapRecHitCollection_);
    std::cout<<"Build fake digi!"<<std::endl;
  } // end dummy rechits
  // Build fake digi collections
  else {    
    bool foundEBDigi = true;
    bool foundEEDigi = true;

    //std::cout<<"sono nell'else di dummyrecHit"<<std::endl;

    try { // barrel digis
      iEvent.getByLabel(tag_barrelDigiProducer_, digisEBHandle);
      for(EBDigiCollection::const_iterator digiItr = digisEBHandle->begin(); digiItr != digisEBHandle->end(); ++digiItr){
          //EBDetId id_crystal(digiItr->id());
          DetId id = digiItr->id();
          //std::cout<<id.subdetId()<<std::endl;
          //std::cout<<"SUBDETID!! Barrel "<<digiItr->id()<<std::endl;
          if(id.subdetId()!=EcalBarrel){
               std::cout<<"SUBDETID: "<<id.subdetId()<<std::endl;
               throw cms::Exception("EcalProblem") << "No valid subdetId() \n";
          }

      }

      *outputEBDigiCollection = *(digisEBHandle.product());
      //std::cout<<"sono entrato nell'else eb"<<std::endl;
    }
    catch (cms::Exception& ex) {
      foundEBDigi = outputEBDigiCollection->size() > 0;
      //std::cout<<"sono entrato nel catch eb"<<std::endl;
    }     

    // insert the EB collection
    iEvent.put(foundEBDigi ? std::move(outputEBDigiCollection) : std::move(fakeEBDigiCollection), barrelDigiCollection_);

    try { // endcap digis
     iEvent.getByLabel(tag_endcapDigiProducer_, digisEEHandle);
     for(EEDigiCollection::const_iterator digiItr = digisEEHandle->begin(); digiItr != digisEEHandle->end(); ++digiItr){
              DetId id = digiItr->id();
             // std::cout<<id.subdetId()<<std::endl;
             // std::cout<<"SUBDETID: "<<id.subdetId()<<std::endl;
              if(id.subdetId()!=EcalEndcap){
                 std::cout<<"SUBDETID: "<<id.subdetId()<<std::endl;
                 throw cms::Exception("EcalProblem") << "No valid subdetId() \n"; 
              }
             // EEDetId id_crystal(digiItr->id());
             // std::cout<<"SUBDETID!! Endcap "<<digiItr->id()<<std::endl;
     //             throw cms::Exception("EcalProblem") << "No valid subdetId(): "<<digiItr->id().subdetId() <<"\n"; 
     }
     *outputEEDigiCollection = *(digisEEHandle.product());
      //std::cout<<"sono entrato nell'else ee"<<std::endl;
    }
    catch (cms::Exception& ex) {
      foundEEDigi = outputEEDigiCollection->size() > 0;
      //std::cout<<"sono entrato nel catch ee"<<std::endl;
    }
    //     std::cout << "Putting Real EE collection?  " << foundEEDigi <<  std::endl;
    iEvent.put(foundEEDigi ? std::move(outputEEDigiCollection) : std::move(fakeEEDigiCollection), endcapDigiCollection_);
     
  }
  //std::cout << "-----------End Dummy Rechits ---------- " << std::endl;
}

void DummyRechitDigis::beginJob(){ }
void DummyRechitDigis::endJob(){ }
void DummyRechitDigis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DummyRechitDigis);


