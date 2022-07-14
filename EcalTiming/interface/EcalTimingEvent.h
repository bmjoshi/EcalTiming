#ifndef ecaltimingevent_hh
#define ecaltimingevent_hh

#include <iostream>
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalDetId/interface/EcalDetIdCollections.h"

/** \class EcalTimingEvent EcalTiming.cc EcalTiming.cc
 *
 * Description: basic timing information
 */

#define MAX_TIME 32.767
#define MAX_ENERGY 655.35

class EcalTimingEvent
{
public:
        EcalTimingEvent()
        {
           detid_ = DetId(0);
           setTime(MAX_TIME);
           setEnergy(MAX_ENERGY);
        }
	EcalTimingEvent(DetId id) {
           detid_ = id;
           setTime(MAX_TIME);
           setEnergy(MAX_ENERGY);
        }
	EcalTimingEvent(const EcalRecHit& rec) {
           detid_ = rec.detid();
           setTime(rec.time());
           setEnergy(rec.energy());
        }

        /// Time is stored in a int16_t in ps. time() returns a float in ns
        float time() const{ return float(time_)/1000.0f; }
        /// Energy is stored in a uint16_t in 10's of MeV. energy() returns a float in GeV
        float energy() const { return float(energy_)/100.0f; }
        const DetId& detid() const { return detid_; }

        void setTime(float t);
        void setEnergy(float e);

private:
        DetId detid_;
        int16_t time_;
        uint16_t energy_;
public:
	friend std::ostream& operator << (std::ostream& os, const EcalTimingEvent& event)
	{
		if(event.detid().subdetId() == EcalBarrel) {
			EBDetId id(event.detid());
			os  << id.ieta() << "\t" << id.iphi() << "\t" << id.zside() << "\t";
		} else {
			EEDetId id(event.detid());
			os << id.ix() << "\t" << id.iy() << "\t" << id.zside() << "\t";
		}

		os << event.time() << "\t" << event.energy();
		return os;
	}

	bool operator== (const EcalTimingEvent &first) const
	{
		// only check amp, time, sigmaT
		if (first.energy() == this->energy() &&
		        first.time() == this->time())
                {
			return true;
		}
		return false;
	}

};

typedef std::vector<EcalTimingEvent> EcalTimingCollection;

#endif

