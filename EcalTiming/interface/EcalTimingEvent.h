#ifndef ecaltimingevent_hh
#define ecaltimingevent_hh

#include <iostream>
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalDetId/interface/EcalDetIdCollections.h"

/** \class EcalTimingEvent EcalTiming.cc EcalTiming.cc
 *
 * Description: basic timing information
 */

class EcalTimingEvent : public EcalRecHit
{
   public:

      ///copy constructor
      EcalTimingEvent(const EcalRecHit& rec): EcalRecHit(rec) {};

      /* EcalRecHit(rec.detid(), rec.energy(), rec.time(), 0, 0){ */
      /* 		setChi2(rec.chi2()); */
      /* 		setEnergyError(rec.energyError()); */
      /* 		uint32_t timeErrorBits = getMasked(extra_, 24, 8); */
      /* 		extra_ = setMasked(rec.extra_, timeErrBits & 0xFF, 24, 8); */
      friend std::ostream& operator << (std::ostream& os, const EcalTimingEvent& event)
      {
         if(event.detid().subdetId() == EcalBarrel) {
            EBDetId id(event.detid());
            os  << id.ieta() << "\t" << id.iphi() << "\t" << id.zside() << "\t";
         } else {
            EEDetId id(event.detid());
            os << id.ix() << "\t" << id.iy() << "\t" << id.zside() << "\t";
         }

         os << event.time() << "\t" << event.timeError() << "\t" << event.energy();
         return os;
      }

      bool operator== (const EcalTimingEvent &first) const
      {
         // only check amp, time, sigmaT
         if (first.energy() == this->energy() &&
               first.time() == this->time() &&
               first.timeError() == this->timeError()) {
            return true;
         }

         return false;
      }

};

#endif

