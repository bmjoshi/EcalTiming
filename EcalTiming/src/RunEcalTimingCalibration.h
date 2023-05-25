// system include files
#include <memory>
#include <iostream>
#include <fstream>

// Make Histograms the way!!
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESProducts.h"
#include "FWCore/Framework/interface/Event.h"
// input collections
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
//RingTools
#include "Calibration/Tools/interface/EcalRingCalibrationTools.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "Geometry/EcalMapping/interface/EcalElectronicsMapping.h"
#include "Geometry/EcalMapping/interface/EcalMappingRcd.h"

// record to be produced:
#include "CondFormats/DataRecord/interface/EcalTimeCalibConstantsRcd.h"
#include "CondFormats/DataRecord/interface/EcalTimeCalibErrorsRcd.h"
#include "CondFormats/DataRecord/interface/EcalTimeOffsetConstantRcd.h"
#include "CondTools/Ecal/interface/EcalCondHeader.h"

#include "CondFormats/EcalObjects/interface/EcalTimeCalibConstants.h"
#include "CondFormats/EcalObjects/interface/EcalTimeCalibErrors.h"
#include "CondFormats/EcalObjects/interface/EcalTimeOffsetConstant.h"

#include "EcalTiming/EcalTiming/interface/EcalTimingEvent.h"
#include "EcalTiming/EcalTiming/interface/EcalCrystalTimingCalibration.h"

#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"

#include "TSystem.h"
#include "TFile.h"
#include "TProfile.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TProfile2D.h"
#include "TChain.h"

#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include <map>
#include <vector>
#include <algorithm>
#include <functional>
#include <set>
#include <assert.h>
#include <time.h>

#include <TMath.h>
#include <Math/VectorUtil.h>
//#include <boost/tokenizer.hpp>

#include "EcalTiming/EcalTiming/interface/EcalTimeCalibrationMapFwd.h"
#include "EcalTiming/EcalTiming/interface/EcalTimeCalibrationUtils.h"

#include "FWCore/FWLite/interface/FWLiteEnabler.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSetReader/interface/ParameterSetReader.h"
#include "PhysicsTools/Utilities/macros/setTDRStyle.C"

using namespace std;

class RunEcalTimingCalibration {

   public:
      // parser argument variables
      int maxEvents = -1;
      float ebECut, eeECut, nSigma, maxRange;
      std::string files, inputTree, outputDir, outputFile, outputCalib, outputCalibCorr;
      std::vector<string> inputFiles;
      
      void Analyze();
      std::vector<std::string> split(const string &, char);

   private:

      TProfile2D* EneMapEB_ = new TProfile2D("EneMapEB", "RecHit Energy[GeV] EB profile map;i#phi; i#eta;E[GeV]", 360, 1., 361., 171, -85, 86);
      TProfile2D* TimeMapEB_ = new TProfile2D("TimeMapEB", "Mean Time [ns] EB profile map; i#phi; i#eta;Time[ns]", 360, 1., 361., 171, -85, 86);
      TProfile2D* TimeErrorMapEB_ = new TProfile2D("TimeErrorMapEB", "Error Time [ns] EB profile map; i#phi i#eta;Time[ns]", 361, 1., 361., 171, -85, 86);

      TProfile2D* EneMapEEP_ = new TProfile2D("EneMapEEP", "RecHit Energy[GeV] profile map EE+;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
      TProfile2D* EneMapEEM_ = new TProfile2D("EneMapEEM", "RecHit Energy[GeV] profile map EE-;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
      TProfile2D* TimeMapEEP_ = new TProfile2D("TimeMapEEP", "Mean Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
      TProfile2D* TimeMapEEM_ = new TProfile2D("TimeMapEEM", "Mean Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
      TProfile2D* TimeErrorMapEEP_ = new TProfile2D("TimeErrorMapEEP", "Error Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
      TProfile2D* TimeErrorMapEEM_ = new TProfile2D("TimeErrorMapEEM", "Error Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);

      TH1F* RechitEneEB_ = new TH1F("RechitEneEB", "RecHit Energy[GeV] EB;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);
      TH1F* RechitTimeEB_ = new TH1F("RechitTimeEB", "RecHit Mean Time[ns] EB;RecHit Time[ns]; Events", 1000000, -50.0, 50.0);
      TH1F* RechitEneEEM_ = new TH1F("RechitEneEEM", "RecHit Energy[GeV] EE-;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);
      TH1F* RechitTimeEEM_ = new TH1F("RechitTimeEEM", "RecHit Mean Time[ns] EE-;RecHit Time[ns]; Events", 1000000, -50.0, 50.0);
      TH1F* RechitEneEEP_ = new TH1F("RechitEneEEP", "RecHit Energy[GeV] EE+;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);
      TH1F* RechitTimeEEP_ = new TH1F("RechitTimeEEP", "RecHit Mean Time[ns] EE+;RecHit Time[ns]; Events", 1000000, -50.0, 50.0);

      TProfile2D* HWTimeMapEB_ = new TProfile2D("HWTimeMapEB",  "Mean HW Time[ns] EB profile map; i#phi; i#eta;Time[ns]", 360, 1., 361., 171, -85, 86);
      TProfile2D* HWTimeMapEEM_ = new TProfile2D("HWTimeMapEEM", "Mean HW Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
      TProfile2D* HWTimeMapEEP_ = new TProfile2D("HWTimeMapEEP", "Mean HW Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);

      TProfile2D* RingTimeMapEB_ = new TProfile2D("RingTimeMapEB",  "Mean Ring Time[ns] EB profile map; i#phi; i#eta;Time[ns]", 360, 1., 361., 171, -85, 86);
      TProfile2D* RingTimeMapEEM_ = new TProfile2D("RingTimeMapEEM", "Mean Ring Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
      TProfile2D* RingTimeMapEEP_ = new TProfile2D("RingTimeMapEEP", "Mean Ring Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);

      TH1F* BXTimeEB_ = new TH1F("BXTimeEB",  "Mean BX Time[ns] EB; BX;Time[ns]",3500,0,3500);
      TH1F* BXTimeEEM_ = new TH1F("BXTimeEEM", "Mean BX Time[ns] EE-;BX; Time[ns]", 3500,0,3500);
      TH1F* BXTimeEEP_ = new TH1F("BXTimeEEP", "Mean BX Time[ns] EE+;BX; Time[ns]", 3500,0,3500);

      TH1F* BXTimeEB_Num_ = new TH1F("BXTimeEB_Num",  "BX occupancy EB; BX;#Hits",3500,0,3500);
      TH1F* BXTimeEEM_Num_ = new TH1F("BXTimeEEM_Num", "BX occupancy EE-;BX;#Hits", 3500,0,3500);
      TH1F* BXTimeEEP_Num_ = new TH1F("BXTimeEEP_Num", "BX occupancy EE+;BX;#Hits", 3500,0,3500);

      TH1F* BXTimeEB_3GeV_ = new TH1F("BXTimeEB_3GeV",  "Mean BX Time[ns] EB; BX;Time[ns]",3500,0,3500);
      TH1F* BXTimeEB_Num_3GeV_ = new TH1F("BXTimeEB_Num_3GeV",  "BX occupancy EB; BX;#Hits",3500,0,3500);
      TH1F* BXTimeEB_4GeV_ = new TH1F("BXTimeEB_4GeV",  "Mean BX Time[ns] EB; BX;Time[ns]",3500,0,3500);
      TH1F* BXTimeEB_Num_4GeV_ = new TH1F("BXTimeEB_Num_4GeV",  "BX occupancy EB; BX;#Hits",3500,0,3500);
      TH1F* BXTimeEB_5GeV_ = new TH1F("BXTimeEB_5GeV",  "Mean BX Time[ns] EB; BX;Time[ns]",3500,0,3500);
      TH1F* BXTimeEB_Num_5GeV_ = new TH1F("BXTimeEB_Num_5GeV",  "BX occupancy EB; BX;#Hits",3500,0,3500);


      TProfile2D* OccupancyEB_ = new TProfile2D("OccupancyEB", "Occupancy EB; i#phi; i#eta; #Hits", 360, 1., 361., 171, -85, 86);
      TProfile2D* OccupancyEEM_ = new TProfile2D("OccupancyEEM", "OccupancyEEM; iy; ix; #Hits", 100, 1, 101, 100, 1, 101);
      TProfile2D* OccupancyEEP_ = new TProfile2D("OccupancyEEP", "OccupancyEEP; iy; ix; #Hits", 100, 1, 101, 100, 1, 101);


      map< int,map< int, map< int,uint32_t > > > rawIDMap;
      map< int,map< int, map< int,UShort_t > > > elecIDMap;
      map< int,map< int, map< int,int > > > ringMap;
      map< uint32_t,int > numMap;
      map< uint32_t,float  > sigmaMap;
      map< uint32_t,float > meanEMap;

      map< int,map< int, map< int,vector<float> > > > timingEventsMap_time;
      map< int,map< int, map< int,vector<float> > > > timingEventsMap_energy;
      map< int,map< int, vector<float> > > timingEventBX_time;
      map< int,vector<float> > timingEventsHWMap_time;
      map< int,vector<float> > timingEventsRingMap_time;

      map< int,map< int, vector<float> > > timingEventBX_time_3GeV;
      map< int,map< int, vector<float> > > timingEventBX_time_4GeV;
      map< int,map< int, vector<float> > > timingEventBX_time_5GeV;

      // Declaration of leaf types
      UInt_t        rawid;
      Int_t         ix;
      Int_t         iy;
      Int_t         iz;
      Float_t       time;
      Float_t       energy;
      UShort_t      elecID;
      Int_t         iRing;
      Int_t         run;
      Int_t         lumi;
      Int_t         event;
      Int_t         bx;

      // List of branches
      TBranch        *b_rawid;   //!
      TBranch        *b_ix;   //!
      TBranch        *b_iy;   //!
      TBranch        *b_iz;   //!
      TBranch        *b_time;   //!
      TBranch        *b_energy;   //!
      TBranch        *b_elecID;   //!
      TBranch        *b_iRing;   //!
      TBranch        *b_run;   //!
      TBranch        *b_lumi;   //!
      TBranch        *b_event;   //!
      TBranch        *b_bx;   //!


};
