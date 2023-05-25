#include "EcalTiming/EcalTiming/interface/EcalTimingEvent.h"
#include <vector>
#include <TTree.h>

/** \class EcalCrystalTimingCalibration EcalCrystalTimingCalibration.h EcalTiming/EcalTiming/interface/EcalCrystalTimingCalibration.h
 *
 * Description: add a description here
 * This class contains all the timing information for a single crystal
 */

//Defines for Dump Status (reason for dumping each crystal)
#define DS_NONE         0x00
#define DS_HIGH_SKEW    0x01
#define DS_UNSTABLE_EN  0x02
#define DS_CCU_OOT      0x04
#define DS_RING         0x08
#define DS_CRYS     		0x10

class EcalCrystalTimingCalibration
{

   private:

      float _sum; ///< scalar sum of the time of each timingEvent
      float _sum2; ///< scalar sum of the square of the time of each timingEvent
      unsigned long int _num; ///< number of timingEvents;

      float _sumE; ///< scalar sum of the energy of each timingEvent: needed for average energy
      bool _storingEvents;

      mutable std::map<float, float> _sumWithinNSigma, _sum2WithinNSigma, _sum3WithinNSigma, _sumEWithinNSigma; ///< variables for calculation of mean, stdDev within n-times the origina stdDev (to remove tails)
      mutable std::map<float, unsigned int> _numWithinNSigma; ///< variables for calculation of mean, stdDev within n-times the origina stdDev (to remove tails)


      std::vector<EcalTimingEvent> timingEvents; ///< vector containing  all the events for this crystal
      std::vector<EcalTimingEvent>::iterator maxChi2Itr;


   public:
      /// default constructor
      EcalCrystalTimingCalibration(bool weightMean = true) :
         //_detId(),
         _sum(0), _sum2(0), _num(0), _sumE(0), _storingEvents(true)
         //totalChi2(-1),
         //useWeightedMean(weightMean)
   {
   }

      inline unsigned int num() const
      {
         return _num;
      };
      inline float mean() const
      {
         if(!_num) return -999.f;
         return _sum / _num;
      }; ///< average time (mean of the time distribution)
      inline float stdDev() const  ///< standard deviation of the time distribution
      {
         float mean_ = mean();
         return sqrt(_sum2 / _num - mean_ * mean_);
      };
      inline float meanError() const
      {
         return stdDev() / sqrt(_num);
      };
      inline float meanE() const
      {
         return _sumE / _num;
      }; ///< average Energy (mean of the Energy  distribution)
      /* bool operator<( EcalCrystalTimingCalibration& rhs) */
      /* { */
      /* 	if(_detId < rhs._detId) return true; */
      /* 	else return false; */
      /* } */
      //float totalChi2;

      float getMeanWithinNSigma(float sigma, float maxRange) const; ///< returns the mean time within abs(mean+ n * stdDev) to reject tails
      float getStdDevWithinNSigma(float sigma, float maxRange) const; ///< returns the stdDev calculated within abs(mean+ n * stdDev) to reject tails
      float getNumWithinNSigma(float sigma, float maxRange) const; ///< returns the num calculated within abs(mean+ n * stdDev) to reject tails
      float getMeanErrorWithinNSigma(float sigma, float maxRange) const; ///< returns the error on the mean calculated within abs(mean+ n * stdDev) to reject tails
      float getSkewnessWithinNSigma(float sigma, float maxRange) const; ///< returns the skewness calculated within abs(mean+ n * stdDev) to reject tails

      friend std::ostream& operator<< (std::ostream& os, const EcalCrystalTimingCalibration& s)
      {
         os << s.mean() << "\t" << s.stdDev() << "\t" << s.num();
         return os;
      }

      /// add new event for this crystal
      inline bool add(EcalTimingEvent te_, bool storeEvent = true)
      {
         return insertEvent(te_,storeEvent);
      }
      inline void clear()
      {
         _sum = 0.0f;
         _sum2 = 0.0f;
         _num = 0;
         _sumE = 0.0f;
         _sumWithinNSigma.clear();
         _sum2WithinNSigma.clear();
         _sum3WithinNSigma.clear();
         _numWithinNSigma.clear();

         timingEvents.clear();
      }

      void dumpToTree(TTree *tree, int ix_, int iy_, int iz_, unsigned int status_, unsigned int elecID_, int iRing_); ///< dump the full set of events in a TTree:  need an empty tree
      void dumpCalibToTree(TTree * tree, int rawid_, int ix_, int iy_, int iz_, unsigned int elecID_, int iRing_) const; ///< dump the callibratoin to the tree
      /// checks if the time measurement is stable changing the min energy threshold
      bool isStableInEnergy(float min, float max, float step, std::vector< std::pair<float, EcalCrystalTimingCalibration*> > &ret);

   private:
      void calcAllWithinNSigma(float n_sigma, float maxRange = 10) const; ///< calculate sum, sum2, sum3, n for time if time within n x stdDev and store the result
      // since the values are stored, the calculation is done only once with only one loop over the events

      /// \todo weighted average by timeError
      bool insertEvent(EcalTimingEvent te_, bool storeEvent)
      {
         if(!storeEvent) _storingEvents = false;
         //exclude values with wrong timeError estimation
         //if(!(te_.timeError() > 0 && te_.timeError() < 1000 && te_.timeError() < 3)) 
         //   return false;

         _sum += te_.time();
         _sum2 += te_.time() * te_.time();
         _sumE += te_.energy();
         _num++;
         if(_storingEvents)
            timingEvents.push_back(te_);
         return true;
      }

};
