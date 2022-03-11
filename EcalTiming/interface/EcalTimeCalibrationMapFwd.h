/** In this file the time Map is defined
 */

class EcalTimingEvent;
class EcalCrystalTimingCalibration;

// Map of detId and Crystal time
typedef std::map<DetId, EcalCrystalTimingCalibration> EcalTimeCalibrationMap;
typedef std::map<unsigned int, EcalCrystalTimingCalibration> EcalHWCalibrationMap;


typedef std::map<DetId, EcalTimingEvent> EventTimeMap;

