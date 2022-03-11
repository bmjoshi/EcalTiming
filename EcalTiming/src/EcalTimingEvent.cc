#include "EcalTiming/EcalTiming/interface/EcalTimingEvent.h"
#include <cmath>
void EcalTimingEvent::setTime(float t)
{
   if (t >= MAX_TIME) t = MAX_TIME;
   else if (t <= -MAX_TIME) t = -MAX_TIME;
   time_ = (int16_t)std::round(t*1000);
}
void EcalTimingEvent::setEnergy(float e) 
{
   if (e >= MAX_ENERGY) e = MAX_ENERGY;
   energy_ = (uint16_t)std::round(e*100.0f);
}
