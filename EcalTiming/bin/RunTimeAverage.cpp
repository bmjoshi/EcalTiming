#include "EcalTiming/EcalTiming/src/RunEcalTimingCalibration.h"
#include "boost/program_options.hpp"

using namespace std;


int main(int argc, char** argv)
{
   RunEcalTimingCalibration calib;

   //Command line parameters
   std::string context;
   context = "Processing command line arguments";
   std::string descString(argv[0]);

   boost::program_options::options_description desc(descString);

   try {
      desc.add_options()
         ("help", "produce help message")
         ("files", boost::program_options::value<std::string>(), "List of comma separated input files.")
         ("inputTree", boost::program_options::value<std::string>(), "Name of the tree.")
         ("maxEvents", boost::program_options::value<int>(), "maxEvents")
         ("nSigma", boost::program_options::value<float>(), "Half-width of the window of selection.")
         ("maxRange", boost::program_options::value<float>(), "Maximum absolute RecHit time range.")
         ("ebECut", boost::program_options::value<float>(), "Minimum RecHit energy in the barrel.")
         ("eeECut", boost::program_options::value<float>(), "Minimum RecHit energy in the endcaps.")
         ("outputFile", boost::program_options::value<std::string>(), "Name of the output file.")
         ("outputCalib", boost::program_options::value<std::string>(), "Name of the output calibrations file.")
         ("outputCalibCorr", boost::program_options::value<std::string>(), "Name of the output calibration corrections file.")
         ("outputDir", boost::program_options::value<std::string>(), "Path to the output directory.");

      boost::program_options::variables_map vm;
      boost::program_options::store(boost::program_options::parse_command_line(argc, argv, desc), vm);
      boost::program_options::notify(vm);

      if (vm.count("help")) {
         cout << desc << "\n";
         return 0;
      }

      if (vm.count("files")) calib.files = vm["files"].as<std::string>(); 
      else calib.files=std::string("timing_reco_selection.root");

      cout<<vm["files"].as<string>()<<endl;
     
      calib.inputFiles = calib.split(calib.files,',');

      if (vm.count("inputTree")) calib.inputTree = vm["inputTree"].as<std::string>();
      else calib.inputTree = "/timing/EcalSplashTiming/timingEventsTree";

      if (vm.count("nSigma"))  calib.nSigma = vm["nSigma"].as<float>() ;
      else calib.nSigma = 2.0;

      if (vm.count("maxRange"))  calib.maxRange = vm["maxRange"].as<float>() ;
      else calib.maxRange = -1; 

      if (vm.count("ebECut"))  calib.ebECut = vm["ebECut"].as<float>() ;
      else calib.ebECut = 0.5;

      if (vm.count("eeECut"))  calib.eeECut= vm["eeECut"].as<float>() ;
      else calib.eeECut = 0.5;

      if (vm.count("outputCalib")) calib.outputCalib = vm["outputCalib"].as<string>();
      else calib.outputCalib = "ecalTiming.dat";

      if (vm.count("outputCalibCorr")) calib.outputCalibCorr = vm["outputCalibCorr"].as<string>(); 
      else calib.outputCalibCorr = "ecalTiming-corr.dat"; 

      if (vm.count("outputFile")) calib.outputFile = vm["outputFile"].as<string>();
      else calib.outputFile = "ecalTiming.root"; 

      if (vm.count("outputDir"))  calib.outputDir = vm["outputDir"].as<float>() ;
      else calib.outputDir = "output/";

   }
   catch(exception& e) {
      cerr << "error: " << e.what() << "\n";
      return 1;
   }
   catch(...) {
      cerr << "Exception of unknown type!\n";
      return 1;
   }

   calib.Analyze();

}
