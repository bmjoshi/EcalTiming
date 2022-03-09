import ROOT
from EcalTiming.EcalTiming.txt2tree import txt2tree
from collections import namedtuple
import math

Crystal = namedtuple('Crystal',("ix", "iy", "iz", "elecID", "FED", "CCU", "iRing"))
Calib = namedtuple('Calib',("time", "stddev", "num", "energy","rawid" ))


det_name = {0:"EB", -1:"EEM", 1:"EEP", (0,-1):"EBM", (0,1):"EBP"}

def getCalibFromTree(tree):
	calibMap = dict()
	for event in tree:
		calibMap[event.rawid] = event.time
	return calibMap

def getCalib():
	input = "/afs/cern.ch/user/p/phansen/public/ecal-timing/dump_EcalTimeCalibConstants_v07_offline__since_00204623_till_4294967295.dat"

	return getCalibFromFile(input)

def getRawIDMap():
	"""
	returns rawidMap[rawid]= Crystal(ix, iy, iz, elecID, FED, CCU, iRing)
	where Crystal is a named tuple
	"""

	rawidMap = dict()

	input = "data/crystalmap.txt"
	with open(input,'r') as f:
		for line in f:
			if line[0] == "#": continue
			line = line.split()
			line = [int(val) for val in line]
			ix, iy, iz, elecID, FED, CCU, iRing, rawid = line
			rawidMap[rawid] = Crystal(ix, iy, iz, elecID, FED, CCU, iRing)
	return rawidMap

rawidMap = getRawIDMap()

def getColumnFromFile(input,col):
	"""
	value from column col and rawid from last column
	"""

	calibMap = dict()
	linenumber = 0
	with open(input,'r') as f:
		for line in f:
			linenumber += 1
			if line[0] == "#": continue
			if "nan" in line: continue
			line = line.split()
			val = float(line[col])
			#print( linenumber, line)
			rawid = int(line[-1])
			calibMap[(rawid)] = val
	return calibMap

def getCalibFromFile(input):
	"""
	Get map of Rawid to time (column 4 in input)
	"""
	return getColumnFromFile(input,3)

def getErrorFromFile(input):
	"""
	Get map of Rawid to time (column 5 in input)
	"""
	return getColumnFromFile(input,4)

def getFullCalibFromFile(input):
	"""
	Get map of Rawid to time (column 5 in input)
	"""
	calibMap = dict()
	linenumber = 0
	with open(input,'r') as f:
		for line in f:
			linenumber += 1
			if line[0] == "#": continue
			if "nan" in line: continue
			ix, iy, iz, time, stddev, num, energy, rawid  = line.split()
			
			calibMap[int(rawid)] = Calib(float(time), float(stddev), int(num),
					float(energy), int(rawid))
	return calibMap

def addCalib(map1, map2, c1, c2):
	"""
	returns ret[id] = map1[id]*c1 + map2[id]*c2
	only contains crystals in both sets
	"""
	ids = set(map1) & set(map2)
	ret = dict()
	for id in ids:
		ret[id] = map1[id]*c1 + map2[id]*c2
	return ret

def divideCalib(map1, map2):
	"""
	returns ret[id] = map1[id]map2[id]*c2
	only contains crystals in both sets
	"""
	ids = set(map1) & set(map2)
	ret = dict()
	for id in ids:
		if map2[id]:
			ret[id] = map1[id]/map2[id]
	return ret

def addOffset(map, offsets):
	"""
	adds different offsets to each Subdetector
	offsets = {0: EB_off, -1:EEM_off, 1:EEp_off}
	"""
	global rawidMap

	ret = dict()
	for id in map:
		ret[id] = map[id] + offsets[rawidMap[id].iz]
	return ret

def subtractOffset(map,offsets):
	os = dict( [ (iz,-offsets[iz]) for iz in offsets] )
	return addOffset(map,os)

def calcMeanBySD(map):
	sum = {0:0, -1:0, 1:0}
	num = {0:0, -1:0, 1:0}
	global rawidMap
	for id in map:
		sum[rawidMap[id].iz] += map[id]
		num[rawidMap[id].iz] += 1

	return dict( [ (iz, sum[iz]/num[iz]) for iz in [0,-1,1] ] )

def calcMeanByCCU(map):
	global rawidMap
	CCU_sum = dict()
	CCU_num = dict()
	for id in map:
		key =(rawidMap[id].FED, rawidMap[id].CCU)
		CCU_sum[key] = 0
		CCU_num[key] = 0

	for id in map:
		key =(rawidMap[id].FED, rawidMap[id].CCU)
		CCU_sum[key] += map[id]
		CCU_num[key] += 1
	
	out_map = dict()
	for id in map:
		key =(rawidMap[id].FED, rawidMap[id].CCU)
		out_map[id] = CCU_sum[key]/CCU_num[key]

	printed = set()
	for id,time in out_map.items():
		if abs(time) > 1.:
			c = rawidMap[id]
			k = (c.FED, c.CCU)
			if k not in printed:
				print(c.FED, c.CCU, c.ix, c.iy, c.iz, time)
				printed.add(k)
	return out_map



def plot1d(map, dir, name, low, hi,xtitle="[ns]", ytitle="Events"):
	global rawidMap

	c = ROOT.TCanvas("c","c",1600,1200)
	hists = dict()
	for iz in [-1, 0 ,1 ]:
		hists[iz] = ROOT.TH1F(det_name[iz] + "_" + name, det_name[iz] + ' ' + name, 50, low, hi)
		hists[iz].SetXTitle(xtitle)
		hists[iz].SetYTitle(ytitle)
	for id,time in map.iteritems():
		hists[rawidMap[id].iz].Fill(time)

	for h in hists.values():
		h.Draw()
		c.SaveAs(dir + '/' + h.GetName() + ".png")

def plotiRing(map, dir, name):
	global rawidMap

	c = ROOT.TCanvas("c","c",1600,1200)
	hists = dict()
	hists[0] = ROOT.TProfile("EB_" + name, 'EB ' + name,  171, -85, 86)
	hists[-1] = ROOT.TProfile("EEM_" + name, 'EEM ' + name, 39, 0, 39)
	hists[1] = ROOT.TProfile("EEP_" + name, 'EEP ' + name, 39, 0, 39)
	for id,time in map.iteritems():
		hists[rawidMap[id].iz].Fill(rawidMap[id].iRing, time)
		hists[rawidMap[id].iz].SetXTitle("#eta ring")
		hists[rawidMap[id].iz].SetYTitle("[ns]")

	for h in hists.values():
		h.Draw()
		c.SaveAs(dir + '/' + h.GetName() + ".png")
	
	return hists
	
def plot2d(map, dir, name, low, hi,setLogz=False):
	global rawidMap

	c = ROOT.TCanvas("c","c",1600,1200)
	if setLogz:
		c.SetLogz()
	hists = dict()
	hists[0] = ROOT.TProfile2D("EB_" + name, 'EB ' + name,  360, 1, 361, 171, -85, 86)
	hists[0].SetXTitle("i#phi")
	hists[0].SetYTitle("i#eta")
	hists[-1] = ROOT.TProfile2D("EEM_" + name, 'EEM ' + name, 100, 1, 101, 100, 1, 101)
	hists[-1].SetXTitle("ix")
	hists[-1].SetYTitle("iy")
	hists[1] = ROOT.TProfile2D("EEP_" + name, 'EEP ' + name, 100, 1, 101, 100, 1, 101)
	hists[1].SetXTitle("ix")
	hists[1].SetYTitle("iy")
	for id,time in map.iteritems():
		if id not in rawidMap: continue
		crys = rawidMap[id]
		if crys.iz == 0:
			x = crys.iy
			y = crys.ix
		else:
			x = crys.ix
			y = crys.iy
		hists[crys.iz].Fill(x,y,time)

	for h in hists.values():
		h.SetAxisRange(low,hi,"Z")
		h.Draw("colz")
		c.SaveAs(dir + '/' + h.GetName() + ".png")

def calcMeanByiRing(m,iRings):
	global rawidMap
	time_sum  = dict(zip(iRings,[0]*len(iRings)))
	time_sum2 = dict(zip(iRings,[0]*len(iRings)))
	time_num  = dict(zip(iRings,[0]*len(iRings)))
	
	for id,time in m.iteritems():
		try:
			crys = rawidMap[id]
		except KeyError:
			print(id, "not found")
			continue
		key = (crys.iz, crys.iRing)
		if key in iRings:
			time_sum[key] += time
			time_sum2[key] += time*time
			time_num[key] += 1
	
	if sum(time_num.values()) < 100:
		return None, None

	mean = dict()
	stddev = dict()
	for k in time_sum:
		if time_num[k]:
			mean[k] = time_sum[k]/time_num[k]
			stddev[k] = math.sqrt(time_sum2[k]/time_num[k] - mean[k]**2)
	return mean,stddev

def calcMean(m):
	global rawidMap
	time_sum = dict(zip(det_name.keys(),[0]*len(det_name)))
	time_sum2 = dict(zip(det_name.keys(),[0]*len(det_name)))
	time_num = dict(zip(det_name.keys(),[0]*len(det_name)))
	
	for id,time in m.iteritems():
		try:
			crys = rawidMap[id]
		except KeyError:
			print(id, "not found")
			continue
		if crys.iz == 0:
			side = math.copysign(1,crys.ix)
			time_sum[(0,side)] += time
			time_sum2[(0,side)] += time*time
			time_num[(0,side)] += 1
			time_sum[0] += time
			time_sum2[0] += time*time
			time_num[0] += 1
		else:
			time_sum[crys.iz] += time
			time_sum2[crys.iz] += time*time
			time_num[crys.iz] += 1
	
	if sum(time_num.values()) < 100:
		return None, None

	mean = dict()
	stddev = dict()
	for k in time_sum:
		if time_num[k]:
			mean[k] = time_sum[k]/time_num[k]
			stddev[k] = math.sqrt(time_sum2[k]/time_num[k] - mean[k]**2)
	return mean,stddev

def calcPull(m1, m2, errors):
	global rawidMap

	diffMap = addCalib(m1, m2, -1, 1)
	resMap = divideCalib(diffMap, errors)

	time_sum = dict(zip(det_name.keys(),[0]*len(det_name)))
	time_sum2 = dict(zip(det_name.keys(),[0]*len(det_name)))
	time_sum3 = dict(zip(det_name.keys(),[0]*len(det_name)))
	time_num = dict(zip(det_name.keys(),[0]*len(det_name)))
	
	for id,time in resMap.iteritems():
		try:
			crys = rawidMap[id]
		except KeyError:
			print(id, "not found")
			continue
		if crys.iz == 0:
			side = math.copysign(1,crys.ix)
			time_sum[(0,side)] += time
			time_sum2[(0,side)] += time**2
			time_sum3[(0,side)] += time**3
			time_num[(0,side)] += 1
			time_sum[0] += time
			time_sum2[0] += time**2
			time_sum3[0] += time**3
			time_num[0] += 1
		else:
			time_sum[crys.iz] += time
			time_sum2[crys.iz] += time**2
			time_sum3[crys.iz] += time**3
			time_num[crys.iz] += 1
	
	mean = dict()
	stddev = dict()
	skew = dict()
	for k in time_sum:
		if time_num[k]:
			mean[k] = time_sum[k]/time_num[k]
			stddev[k] = math.sqrt(time_sum2[k]/time_num[k] - mean[k]**2)
			skew[k] =  (time_sum3[k] / time_num[k] - 3 * mean[k] * stddev[k]**2 - mean[k]**3) / stddev[k]**3;
	return mean,stddev,skew


if __name__ == "__main__":
	print("hi")
	calib = getCalib();
	print(len(calib))

