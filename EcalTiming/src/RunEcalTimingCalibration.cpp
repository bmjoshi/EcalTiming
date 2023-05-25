#include "EcalTiming/EcalTiming/src/RunEcalTimingCalibration.h"
#include "boost/program_options.hpp"

using namespace std;

std::vector<std::string> RunEcalTimingCalibration::split(const string &text, char sep) {
   vector<string> tokens;
   size_t start = 0, end = 0;
   while ((end = text.find(sep, start)) != string::npos) {
      tokens.push_back(text.substr(start, end - start));
      start = end + 1;
   }
   tokens.push_back(text.substr(start));
   return tokens;
}

void RunEcalTimingCalibration::Analyze(){

   TChain* tree = new TChain(inputTree.c_str());
   for(unsigned int ifile = 0; ifile< inputFiles.size(); ifile++)
   {
      cout << "---> " << ifile+1 << " - Input file = " << inputFiles.at(ifile) << endl;
      tree->Add(inputFiles.at(ifile).c_str());
   }

   rawIDMap.clear();
   elecIDMap.clear();
   ringMap.clear();
   numMap.clear();
   sigmaMap.clear();
   meanEMap.clear();
   timingEventsMap_time.clear();
   timingEventsMap_energy.clear();
   timingEventBX_time.clear();
   timingEventsHWMap_time.clear();
   timingEventsRingMap_time.clear();
   timingEventBX_time_3GeV.clear();
   timingEventBX_time_4GeV.clear();
   timingEventBX_time_5GeV.clear();

   tree->SetBranchAddress("rawid", &rawid, &b_rawid);
   tree->SetBranchAddress("ix", &ix, &b_ix);
   tree->SetBranchAddress("iy", &iy, &b_iy);
   tree->SetBranchAddress("iz", &iz, &b_iz);
   tree->SetBranchAddress("time", &time, &b_time);
   tree->SetBranchAddress("energy", &energy, &b_energy);
   tree->SetBranchAddress("elecID", &elecID, &b_elecID);
   tree->SetBranchAddress("iRing", &iRing, &b_iRing);
   tree->SetBranchAddress("run", &run, &b_run);
   tree->SetBranchAddress("lumi", &lumi, &b_lumi);
   tree->SetBranchAddress("event", &event, &b_event);
   tree->SetBranchAddress("bx", &bx, &b_bx);

   long long int nEvents = 0;

   if(maxEvents == -1) nEvents = tree->GetEntries();
   else {
      if(maxEvents > tree->GetEntries()) nEvents = tree->GetEntries();
      if(maxEvents < tree->GetEntries()) nEvents = maxEvents;
   }
   cout << "maxEvents = " << nEvents << endl;

   for(int entry = 0; entry < nEvents; entry++){

      if(entry%1000000==0) cout << "--- Reading entry = " << entry << endl;
      tree->GetEntry(entry);

      if(iz == 0) { 
         ix += 85;
         if (energy<ebECut) continue;
      }
      else if(iz < 0) {
         iz = 1;
         if (energy<eeECut) continue;
      }
      else if(iz > 0){
         iz = 2;
         if (energy<eeECut) continue;
      }

      rawIDMap[ix][iy][iz] = rawid;
      elecIDMap[ix][iy][iz] = elecID;
      ringMap[ix][iy][iz] = iRing;
      timingEventsMap_time[ix][iy][iz].push_back(time); 
      timingEventsMap_energy[ix][iy][iz].push_back(energy);
      timingEventsHWMap_time[elecID].push_back(time);
      timingEventsRingMap_time[iRing].push_back(time);
      timingEventBX_time[bx][iz].push_back(time);

      if(energy > 3.) timingEventBX_time_3GeV[bx][iz].push_back(time);
      if(energy > 4.) timingEventBX_time_4GeV[bx][iz].push_back(time);
      if(energy > 5.) timingEventBX_time_5GeV[bx][iz].push_back(time);

   }

   EcalTimeCalibrationUtils* untils = new EcalTimeCalibrationUtils();
   EcalTimeCalibConstants timeCalibConstants;

   for(auto tx : timingEventsMap_time) 
      for(auto ty : tx.second) 
         for(auto tz : ty.second) {

            untils->clear();
            untils->add(timingEventsMap_time[tx.first][ty.first][tz.first]); 
            numMap[rawIDMap[tx.first][ty.first][tz.first]] = untils->num();
            sigmaMap[rawIDMap[tx.first][ty.first][tz.first]] = untils->stdDev();

            if(untils->num() == 0) continue; 

            int ieta = 0;
            int iphi = 0;
            int ix = 0;    
            int iy = 0;    

            if(tz.first == 0) {
               ieta = tx.first-85;
               iphi = ty.first;
            } else if(tz.first < 0) {
               ix = tx.first;
               iy = ty.first;
            } else if(tz.first > 0) {
               ix = tx.first;
               iy = ty.first;
            }

            if(tz.first == 0) {
               TimeMapEB_->Fill(iphi,ieta, untils->getMeanWithinNSigma(nSigma,maxRange)); 
               TimeErrorMapEB_->Fill(iphi,ieta, untils->getMeanErrorWithinNSigma(nSigma,maxRange)); 
               OccupancyEB_->Fill(iphi,ieta, untils->num()); 
               RechitTimeEB_->Fill(untils->getMeanWithinNSigma(nSigma,maxRange)); 
            } else if(tz.first == 1) {
               TimeMapEEM_->Fill(ix,iy, untils->getMeanWithinNSigma(nSigma,maxRange));
               TimeErrorMapEEM_->Fill(ix,iy, untils->getMeanErrorWithinNSigma(nSigma,maxRange));
               OccupancyEEM_->Fill(ix,iy, untils->num());
               RechitTimeEEM_->Fill(untils->getMeanWithinNSigma(nSigma,maxRange));
            } else if(tz.first == 2) {
               TimeMapEEP_->Fill(ix,iy, untils->getMeanWithinNSigma(nSigma,maxRange));
               TimeErrorMapEEP_->Fill(ix,iy, untils->getMeanErrorWithinNSigma(nSigma,maxRange));
               OccupancyEEP_->Fill(ix,iy, untils->num());
               RechitTimeEEP_->Fill(untils->getMeanWithinNSigma(nSigma,maxRange));
            }

            float correction =  -1*untils->getMeanWithinNSigma(nSigma,maxRange);
            timeCalibConstants.setValue(rawIDMap[tx.first][ty.first][tz.first], correction);

            untils->clear();
            untils->add(timingEventsMap_energy[tx.first][ty.first][tz.first]); 
            meanEMap[rawIDMap[tx.first][ty.first][tz.first]] = untils->mean();

            if(tz.first == 0) {
               EneMapEB_->Fill(iphi,ieta, untils->mean()); 
               RechitEneEB_->Fill(untils->mean());  
            } else if(tz.first == 1) {
               EneMapEEM_->Fill(ix,iy, untils->mean());
               RechitEneEEM_->Fill(untils->mean());
            } else if(tz.first == 2) {
               EneMapEEP_->Fill(ix,iy, untils->mean());
               RechitEneEEP_->Fill(untils->mean());
            }

            untils->clear();
            untils->add(timingEventsHWMap_time[elecIDMap[tx.first][ty.first][tz.first]]); 

            if(tz.first == 0) {
               HWTimeMapEB_->Fill(iphi,ieta, untils->mean());   
            } else if(tz.first == 1) {
               HWTimeMapEEM_->Fill(ix,iy, untils->mean());
            } else if(tz.first == 2) {
               HWTimeMapEEP_->Fill(ix,iy, untils->mean());
            }

            untils->clear();
            untils->add(timingEventsRingMap_time[ringMap[tx.first][ty.first][tz.first]]); 

            if(tz.first == 0) {
               RingTimeMapEB_->Fill(iphi,ieta, untils->mean());   
            } else if(tz.first == 1) {
               RingTimeMapEEM_->Fill(ix,iy, untils->mean());
            } else if(tz.first == 2) {
               RingTimeMapEEP_->Fill(ix,iy, untils->mean());
            }

         }

   for(auto tx : timingEventBX_time) 
      for(auto tz : tx.second) {

         untils->clear();
         untils->add(timingEventBX_time[tx.first][tz.first]); 

         if(untils->num() == 0) continue; 

         if(tz.first == 0) BXTimeEB_->SetBinContent(BXTimeEB_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));
         else if(tz.first == 1) BXTimeEEM_->SetBinContent(BXTimeEEM_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));
         else if(tz.first == 2) BXTimeEEP_->SetBinContent(BXTimeEEP_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));

         if(tz.first == 0) BXTimeEB_->SetBinError(BXTimeEB_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));
         else if(tz.first == 1) BXTimeEEM_->SetBinError(BXTimeEEM_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));
         else if(tz.first == 2) BXTimeEEP_->SetBinError(BXTimeEEP_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));

         if(tz.first == 0) BXTimeEB_Num_->SetBinContent(BXTimeEB_Num_->FindBin(tx.first),untils->num());
         else if(tz.first == 1) BXTimeEEM_Num_->SetBinContent(BXTimeEEM_Num_->FindBin(tx.first),untils->num());
         else if(tz.first == 2) BXTimeEEP_Num_->SetBinContent(BXTimeEEP_Num_->FindBin(tx.first),untils->num());

      }

   //test different EB energy thresholds 

   for(auto tx : timingEventBX_time_3GeV) 
      for(auto tz : tx.second) {

         untils->clear();
         untils->add(timingEventBX_time_3GeV[tx.first][tz.first]); 

         if(untils->num() == 0) continue; 

         if(tz.first == 0) {
            BXTimeEB_3GeV_->SetBinContent(BXTimeEB_3GeV_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));
            BXTimeEB_3GeV_->SetBinError(BXTimeEB_3GeV_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));
            BXTimeEB_Num_3GeV_->SetBinContent(BXTimeEB_Num_3GeV_->FindBin(tx.first),untils->num());
         }

      }

   for(auto tx : timingEventBX_time_4GeV) 
      for(auto tz : tx.second) {

         untils->clear();
         untils->add(timingEventBX_time_4GeV[tx.first][tz.first]); 

         if(untils->num() == 0) continue; 

         if(tz.first == 0) {
            BXTimeEB_4GeV_->SetBinContent(BXTimeEB_4GeV_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));
            BXTimeEB_4GeV_->SetBinError(BXTimeEB_4GeV_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));
            BXTimeEB_Num_4GeV_->SetBinContent(BXTimeEB_Num_4GeV_->FindBin(tx.first),untils->num());
         }

      }

   for(auto tx : timingEventBX_time_5GeV) 
      for(auto tz : tx.second) {

         untils->clear();
         untils->add(timingEventBX_time_5GeV[tx.first][tz.first]); 

         if(untils->num() == 0) continue; 

         if(tz.first == 0) {
            BXTimeEB_5GeV_->SetBinContent(BXTimeEB_5GeV_->FindBin(tx.first),untils->getMeanWithinNSigma(nSigma,maxRange));
            BXTimeEB_5GeV_->SetBinError(BXTimeEB_5GeV_->FindBin(tx.first),untils->getMeanErrorWithinNSigma(nSigma,maxRange));
            BXTimeEB_Num_5GeV_->SetBinContent(BXTimeEB_Num_5GeV_->FindBin(tx.first),untils->num());
         }

      }

   ofstream fout((outputDir+outputCalib).c_str(), ios::out | ios::trunc);  

   //EB
   for(unsigned int i = 0; i < timeCalibConstants.barrelItems().size(); ++i) {
      EBDetId id(EBDetId::detIdFromDenseIndex(i)); 
      fout << id.ieta() << "\t" << id.iphi() << "\t" << 0 << "\t" << timeCalibConstants.barrelItems()[i] << "\t" << id.rawId() << endl;
   }
   //EE
   for(unsigned int i = 0; i < timeCalibConstants.endcapItems().size(); ++i) {
      EEDetId id(EEDetId::detIdFromDenseIndex(i)); 
      fout << id.ix() << "\t" << id.iy() << "\t" << id.zside() << "\t" << timeCalibConstants.endcapItems()[i] << "\t" << id.rawId() << endl;
   }

   fout.close();

   ofstream fout_corr((outputDir+outputCalibCorr).c_str(), ios::out | ios::trunc);

   //EB-
   for(int ieta = -1; ieta>= -85; ieta--)
      for(int iphi = 1; iphi<= 360; iphi++) {
         untils->clear();
         untils->add(timingEventsMap_time[ieta+85][iphi][0]); 
         if(numMap[rawIDMap[ieta+85][iphi][0]] != 0) fout_corr << ieta << "\t" << iphi << "\t" << 0
            << "\t" << untils->getMeanWithinNSigma(nSigma,maxRange) << "\t" << sigmaMap[rawIDMap[ieta+85][iphi][0]] << "\t" << numMap[rawIDMap[ieta+85][iphi][0]] << "\t" << meanEMap[rawIDMap[ieta+85][iphi][0]]
               << "\t" << rawIDMap[ieta+85][iphi][0] << endl;

      }
   //EB+
   for(int ieta = 1; ieta<= 85; ieta++)
      for(int iphi = 1; iphi<= 360; iphi++) {
         untils->clear();
         untils->add(timingEventsMap_time[ieta+85][iphi][0]); 
         if(numMap[rawIDMap[ieta+85][iphi][0]] != 0) fout_corr << ieta << "\t" << iphi << "\t" << 0
            << "\t" << untils->getMeanWithinNSigma(nSigma,maxRange) << "\t" << sigmaMap[rawIDMap[ieta+85][iphi][0]] << "\t" << numMap[rawIDMap[ieta+85][iphi][0]] << "\t" << meanEMap[rawIDMap[ieta+85][iphi][0]]
               << "\t" << rawIDMap[ieta+85][iphi][0] << endl;

      }
   //EE-
   for(int ix = 1; ix <=100; ix++)
      for(int iy = 1; iy<= 100; iy++) {
         untils->clear();
         untils->add(timingEventsMap_time[ix][iy][1]); 
         if(numMap[rawIDMap[ix][iy][1]] != 0) fout_corr << ix << "\t" << iy << "\t" << -1
            << "\t" << untils->getMeanWithinNSigma(nSigma,maxRange) << "\t" << sigmaMap[rawIDMap[ix][iy][1]] << "\t" << numMap[rawIDMap[ix][iy][1]] << "\t" << meanEMap[rawIDMap[ix][iy][1]]
               << "\t" << rawIDMap[ix][iy][1] << endl;

      }
   //EE+
   for(int ix = 1; ix <=100; ix++)
      for(int iy = 1; iy<= 100; iy++) {
         untils->clear();
         untils->add(timingEventsMap_time[ix][iy][2]); 
         if(numMap[rawIDMap[ix][iy][2]] != 0) fout_corr << ix << "\t" << iy << "\t" << 1
            << "\t" << untils->getMeanWithinNSigma(nSigma,maxRange) << "\t" << sigmaMap[rawIDMap[ix][iy][2]] << "\t" << numMap[rawIDMap[ix][iy][2]] << "\t" << meanEMap[rawIDMap[ix][iy][2]]
               << "\t" << rawIDMap[ix][iy][2] << endl;

      }

   fout_corr.close();

   TFile* file = new TFile((outputDir+outputFile).c_str(),"RECREATE");  
   file->cd();

   EneMapEB_->Write();
   TimeMapEB_->Write();
   TimeErrorMapEB_->Write();

   EneMapEEP_->Write();
   EneMapEEM_->Write();
   TimeMapEEP_->Write();
   TimeMapEEM_->Write();
   TimeErrorMapEEP_->Write();
   TimeErrorMapEEM_->Write();

   RechitEneEB_->Write();
   RechitTimeEB_->Write();
   RechitEneEEM_->Write();
   RechitTimeEEM_->Write();
   RechitEneEEP_->Write();
   RechitTimeEEP_->Write();

   HWTimeMapEB_->Write();
   HWTimeMapEEM_->Write();
   HWTimeMapEEP_->Write();

   RingTimeMapEB_->Write();
   RingTimeMapEEM_->Write();
   RingTimeMapEEP_->Write();

   BXTimeEB_->Write();
   BXTimeEEM_->Write();
   BXTimeEEP_->Write();

   BXTimeEB_Num_->Write();
   BXTimeEEM_Num_->Write();
   BXTimeEEP_Num_->Write();

   BXTimeEB_3GeV_->Write();
   BXTimeEB_Num_3GeV_->Write();
   BXTimeEB_4GeV_->Write();
   BXTimeEB_Num_4GeV_->Write();
   BXTimeEB_5GeV_->Write();
   BXTimeEB_Num_5GeV_->Write();

   OccupancyEB_->Write();
   OccupancyEEM_->Write();
   OccupancyEEP_->Write();

   file->Close();
}
