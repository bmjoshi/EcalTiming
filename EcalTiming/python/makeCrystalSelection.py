
#recovered xtals in EE+
recovered = [ (58, 41), (59, 41), (59, 42), (60, 41), (60, 42),
		(81, 21), (81, 22), (81, 23), (81, 24), (81, 25),
		(82, 21), (82, 22), (82, 23), (82, 24), (82, 25),
		(83, 21), (83, 22), (83, 23), (83, 24), (83, 25),
		(84, 21), (84, 22), (84, 23), (84, 24), (84, 25),
		(85, 21), (85, 22), (85, 23), (85, 24), (85, 25),
		(86, 16), (86, 17), (86, 18), (86, 19), (86, 20),
		(86, 21), (86, 22), (86, 23), (86, 24), (86, 25),
		(87, 16), (87, 17), (87, 18), (87, 19), (87, 20),
		(87, 21), (87, 22), (87, 23), (87, 24), (87, 25),
		(88, 21), (88, 22), (88, 23), (88, 24), (88, 25),
		(89, 21), (89, 22), (89, 23), (89, 24), (89, 25),
		(90, 21), (90, 22), (90, 23), (90, 24), (90, 25),
		(91, 21), (91, 22), (91, 23), (91, 24), (91, 25),
		(92, 21), (92, 22), (92, 23), (92, 24), (92, 25),]

#range to fix in EB

iphi_min = 161
iphi_max = 170
ieta_min = 26
ieta_max = 45

fix = [ (ieta,iphi) for iphi in range(iphi_min, iphi_max +1) for ieta in
		range( ieta_min, ieta_max +1)]

def fixCrystal(a,b,det):
	if det == -1:
		return False
	elif det == 1:
		return (a,b) in recovered
	elif det == 0:
		return (a,b) in fix

def getCalibrations(filename, invert = -1):
	calibrations = dict()
	with open(filename) as f:
		for line in f:
			data = line.split()
			x = int(data[0])
			y = int(data[1])
			detector = int(data[2])
			constant = invert*float(data[3])
			err = float(data[4])

			# if invert != -1 store things that fail instead
			if( fixCrystal(x,y,detector) == (invert == -1) ):
				calibrations[(x,y,detector)] = (constant,err)
	return calibrations

nBeam1 = 26
nBeam2 = 31

beam1file = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_26_events_beam_1-corr-0.dat'
beam2file = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_31_events_beam_2-corr-0.dat'
oldcalibfile = '/afs/cern.ch/user/p/phansen/public/ecal-timing/CMSSW_7_3_4/src/Usercode/DBDump/dump_EcalTimeCalibConstants_v07_offline__since_00204623_till_4294967295.dat'

beam1 = getCalibrations(beam1file)
beam2 = getCalibrations(beam2file)
oldcalib = getCalibrations(oldcalibfile, invert = 1)

average = dict()

for crystal in beam1:
	b1ave,b1err = beam1[crystal]
	b2ave,b2err = beam2[crystal]
	ave = (b1ave * nBeam1 + b2ave*nBeam2)/ (nBeam1 +nBeam2)
	err = ((b1ave - b2ave)**2*nBeam1*nBeam2)/(nBeam1 + nBeam2)**2 + (nBeam1*b1err**2 + nBeam2*b2err**2)/(nBeam1 + nBeam2)
	average[crystal] = (ave,err)

print(len(beam1), len(beam2), len(oldcalib))

from EcalTiming.EcalTiming.calibrationXML import CalibrationXML

cal = CalibrationXML()

for (x,y,d),(ave,err) in average.iteritems():
	cal.addCrystal(x,y,d,ave,err)

for (x,y,d),(ave,err) in oldcalib.iteritems():
	cal.addCrystal(x,y,d,ave,err)

print(len(cal.crystals))
cal.sort()

cal.writeConstant("const.xml")
cal.writeErrors("error.xml")

import ROOT
from EcalTiming.EcalTiming.PlotUtils import drawMultipleGrid,customROOTstyle
customROOTstyle()

def plotCalibration(crystals,histoname):
	EB = ROOT.TProfile2D(histoname + "EB",histoname + " EB",360,1,361,85*2,-84,86) 
	EEP = ROOT.TProfile2D(histoname + "EEP",histoname + " EEP", 100, 1, 101, 100, 1, 101)
	EEM = ROOT.TProfile2D(histoname + "EEM",histoname + " EEM", 100, 1, 101, 100, 1, 101)
	
	EB.SetZTitle("ns")
	EB.SetXTitle("i#phi")
	EB.SetYTitle("i#eta")

	EEP.SetZTitle("ns")
	EEP.SetXTitle("ix")
	EEP.SetYTitle("iy")
	EEM.SetZTitle("ns")
	EEM.SetXTitle("ix")
	EEM.SetYTitle("iy")

	for c in crystals:
		if c.det == 0:
			EB.Fill(c.iphi,c.ieta,c.calib)
		elif c.det == -1:
			EEM.Fill(c.ix,c.iy,c.calib)
		elif c.det == 1:
			EEP.Fill(c.ix,c.iy,c.calib)

	return (EEM, EB, EEP)

print("plot")
drawMultipleGrid(plotCalibration(cal.crystals, "new_calib"),"plots/new_calib.png", limits = [[-10,10]]*3, height = 600 )



