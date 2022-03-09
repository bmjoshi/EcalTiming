import ROOT
from EcalTiming.EcalTiming.PlotUtils import customROOTstyle, drawMultipleGrid
import EcalTiming.EcalTiming.TokenRing as TokenRing
import math

def drawMultipleGrid(hists,outname,limits=[],setLogY=False,setLogZ=False,ncols = 3):
    c = ROOT.TCanvas("c", "c", 1500,1100)
    nhists = len(hists)
    nrows = (nhists-1)/ncols+1
    c.Divide(ncols,nrows)
    
    if len(limits) == 2:
        limits = [limits]*nhists
    if len(limits) == ncols and len(limits[0]) == 2:
        limits = limits*nrows

    for pad in range(len(hists)):
        p = c.cd(pad +1)
        if setLogY: p.SetLogy()
        if setLogZ: p.SetLogz()
        if limits: hists[pad].GetZaxis().SetRangeUser(limits[pad][0], limits[pad][1])
        hists[pad].Draw("colz")


    c.SaveAs(outname)

def plotCalibration(filename,histoname,invert=1,doEnergy=True):
    EB = ROOT.TProfile2D(histoname + "EB",histoname + " EB",360,1,361,85*2,-84,86) 
    EEP = ROOT.TProfile2D(histoname + "EEP",histoname + " EEP", 100, 1, 101, 100, 1, 101)
    EEM = ROOT.TProfile2D(histoname + "EEM",histoname + " EEM", 100, 1, 101, 100, 1, 101)
    
    EB_err = ROOT.TProfile2D(histoname + "EB_err",histoname + " EB error",360,1,361,85*2,-84,86) 
    EEP_err = ROOT.TProfile2D(histoname + "EEP_err",histoname + " EEP error", 100, 1, 101, 100, 1, 101)
    EEM_err = ROOT.TProfile2D(histoname + "EEM_err",histoname + " EEM error", 100, 1, 101, 100, 1, 101)

    EB.SetZTitle("ns")
    EB.SetXTitle("i#phi")
    EB.SetYTitle("i#eta")

    EEP.SetZTitle("ns")
    EEP.SetXTitle("ix")
    EEP.SetYTitle("iy")
    EEM.SetZTitle("ns")
    EEM.SetXTitle("ix")
    EEM.SetYTitle("iy")

    EB_err.SetZTitle("ns")
    EB_err.SetXTitle("i#phi")
    EB_err.SetYTitle("i#eta")

    EEP_err.SetZTitle("ns")
    EEP_err.SetXTitle("ix")
    EEP_err.SetYTitle("iy")
    EEM_err.SetZTitle("ns")
    EEM_err.SetXTitle("ix")
    EEM_err.SetYTitle("iy")

    if doEnergy:
        EB_en = ROOT.TProfile2D(histoname + "EB_Energy",histoname + " EB Energy",360,1,361,85*2,-84,86) 
        EEP_en = ROOT.TProfile2D(histoname + "EEP_Energy",histoname + " EEP Energy", 100, 1, 101, 100, 1, 101)
        EEM_en = ROOT.TProfile2D(histoname + "EEM_Energy",histoname + " EEM Energy", 100, 1, 101, 100, 1, 101)

        EB_en.SetZTitle("GeV")
        EB_en.SetXTitle("i#phi")
        EB_en.SetYTitle("i#eta")

        EEP_en.SetZTitle("GeV")
        EEP_en.SetXTitle("ix")
        EEP_en.SetYTitle("iy")
        EEM_en.SetZTitle("GeV")
        EEM_en.SetXTitle("ix")
        EEM_en.SetYTitle("iy")

    with open(filename) as f:
        for line in f:
            data = line.split()
            x = int(data[0])
            y = int(data[1])
            detector = int(data[2])
            constant = invert*float(data[3])
            err = float(data[4])
            raw = int(data[-1])
            if err > 1.0:
                print("noisy:", raw, err)
            if detector == 0:
                if(x < 0): x+=1
                EB.Fill(y,x,constant)
                EB_err.Fill(y,x,err)
            elif detector == -1:
                EEM.Fill(x,y,constant)
                EEM_err.Fill(x,y,err)
            elif detector == 1:
                EEP.Fill(x,y,constant)
                EEP_err.Fill(x,y,err)

            if doEnergy:
                energy = float(data[6])
                if detector == 0:
                    if(x < 0): x+=1
                    EB_en.Fill(y,x,energy)
                elif detector == -1:
                    EEM_en.Fill(x,y,energy)
                elif detector == 1:
                    EEP_en.Fill(x,y,energy)


    if doEnergy:
        return (EEM, EB, EEP), (EEM_err, EB_err, EEP_err), (EEM_en, EB_en, EEP_en)
    else:
        return (EEM, EB, EEP), (EEM_err, EB_err, EEP_err)

def plotElectronics(filename,histoname,invert=1):

    EcalTPGParam = ROOT.TFile("EcalTPGParam.root")    
    tpgmap = EcalTPGParam.Get("tpgmap")

    feds = dict()
    trs = dict()
    ccus = dict()

    crystalmap = dict()

    for crystal in tpgmap:
        fed = crystal.fed
        tr = crystal.TR
        ccu = crystal.CCU

        crystalmap[(crystal.ix, crystal.iy, crystal.iz, crystal.ieta, crystal.iphi)] = (fed,tr,ccu)

        if fed not in feds:
            feds[fed] = ROOT.TH1D(histoname + "fed" + str(fed), "FED " + str(fed) + " Timing", 100,-10,10)
            feds[fed].SetXTitle("[ns]")
            feds[fed].SetYTitle("Events")

        if (fed, tr) not in trs:
            trs[(fed,tr)] = ROOT.TH1D(histoname + "fed" + str(fed) + "_TR" + str(tr), "FED " + str(fed) + " TR " + str(tr) + " Timing", 100,-10,10)
            trs[(fed,tr)].SetXTitle("[ns]")
            trs[(fed,tr)].SetYTitle("Events")

        if (fed, ccu) not in ccus:
            ccus[(fed,ccu)] = ROOT.TH1D(histoname + "fed" + str(fed) + "_ccu" + str(ccu), "FED " + str(fed) + " CCU " + str(ccu) + " Timing", 100,-10,10)
            ccus[(fed,ccu)].SetXTitle("[ns]")
            ccus[(fed,ccu)].SetYTitle("Events")

    
    with open(filename) as f:
        for line in f:
            data = line.split()
            x = int(data[0])
            y = int(data[1])
            detector = int(data[2])
            constant = invert*float(data[3])
            err = float(data[4])

            ix = -999
            iy = -999
            ieta = -999
            iphi = -999

            if detector == 0:
                ieta = x
                iphi = y
                iz = math.copysign(1,ieta)
            elif detector == -1:
                ix = x
                iy = y
                iz = -1
            elif detector == 1:
                ix = x
                iy = y
                iz = 1
            fed, tr, ccu = crystalmap[(ix, iy, iz, ieta, iphi)]
            feds[fed].Fill(constant)
            trs[(fed,tr)].Fill(constant)
            ccus[(fed,ccu)].Fill(constant)
            
    fedEB = ROOT.TProfile2D(histoname  + "fedEB", histoname + "fed EB",  360, 1, 361, 171, -85,86) 
    fedEEP = ROOT.TProfile2D(histoname + "fedEEP",histoname + "fed EEP", 100, 1, 101, 100, 1, 101)
    fedEEM = ROOT.TProfile2D(histoname + "fedEEM",histoname + "fed EEM", 100, 1, 101, 100, 1, 101)
    federrEB = ROOT.TProfile2D(histoname  + "federrEB", histoname + "fed err EB",  360, 1, 361, 171, -85,86) 
    federrEEP = ROOT.TProfile2D(histoname + "federrEEP",histoname + "fed err EEP", 100, 1, 101, 100, 1, 101)
    federrEEM = ROOT.TProfile2D(histoname + "federrEEM",histoname + "fed err EEM", 100, 1, 101, 100, 1, 101)
    fedskewEB = ROOT.TProfile2D(histoname  + "fedskewEB", histoname + "fed skew EB",  360, 1, 361, 171, -85,86) 
    fedskewEEP = ROOT.TProfile2D(histoname + "fedskewEEP",histoname + "fed skew EEP", 100, 1, 101, 100, 1, 101)
    fedskewEEM = ROOT.TProfile2D(histoname + "fedskewEEM",histoname + "fed skew EEM", 100, 1, 101, 100, 1, 101)
    trEB = ROOT.TProfile2D(histoname  + "trEB", histoname + "tr EB",  360, 1, 361, 171, -85,86) 
    trEEP = ROOT.TProfile2D(histoname + "trEEP",histoname + "tr EEP", 100, 1, 101, 100, 1, 101)
    trEEM = ROOT.TProfile2D(histoname + "trEEM",histoname + "tr EEM", 100, 1, 101, 100, 1, 101)
    trerrEB = ROOT.TProfile2D(histoname  + "trerrEB", histoname + "tr err EB",  360, 1, 361, 171, -85,86) 
    trerrEEP = ROOT.TProfile2D(histoname + "trerrEEP",histoname + "tr err EEP", 100, 1, 101, 100, 1, 101)
    trerrEEM = ROOT.TProfile2D(histoname + "trerrEEM",histoname + "tr err EEM", 100, 1, 101, 100, 1, 101)
    trskewEB = ROOT.TProfile2D(histoname  + "trskewEB", histoname + "tr skew EB",  360, 1, 361, 171, -85,86) 
    trskewEEP = ROOT.TProfile2D(histoname + "trskewEEP",histoname + "tr skew EEP", 100, 1, 101, 100, 1, 101)
    trskewEEM = ROOT.TProfile2D(histoname + "trskewEEM",histoname + "tr skew EEM", 100, 1, 101, 100, 1, 101)
    ccuEB = ROOT.TProfile2D(histoname  + "ccuEB", histoname + "ccu EB",  360, 1, 361, 171, -85,86) 
    ccuEEP = ROOT.TProfile2D(histoname + "ccuEEP",histoname + "ccu EEP", 100, 1, 101, 100, 1, 101)
    ccuEEM = ROOT.TProfile2D(histoname + "ccuEEM",histoname + "ccu EEM", 100, 1, 101, 100, 1, 101)
    ccuerrEB = ROOT.TProfile2D(histoname  + "ccuerrEB", histoname + "ccu err EB",  360, 1, 361, 171, -85,86) 
    ccuerrEEP = ROOT.TProfile2D(histoname + "ccuerrEEP",histoname + "ccu err EEP", 100, 1, 101, 100, 1, 101)
    ccuerrEEM = ROOT.TProfile2D(histoname + "ccuerrEEM",histoname + "ccu err EEM", 100, 1, 101, 100, 1, 101)
    ccuskewEB = ROOT.TProfile2D(histoname  + "ccuskewEB", histoname + "ccu skew EB",  360, 1, 361, 171, -85,86) 
    ccuskewEEP = ROOT.TProfile2D(histoname + "ccuskewEEP",histoname + "ccu skew EEP", 100, 1, 101, 100, 1, 101)
    ccuskewEEM = ROOT.TProfile2D(histoname + "ccuskewEEM",histoname + "ccu skew EEM", 100, 1, 101, 100, 1, 101)


    for ix, iy, iz, ieta, iphi in crystalmap:
        fed, tr, ccu = crystalmap[(ix,iy,iz,ieta,iphi)]
        if ix != -999:
            if iz == 1:
                fedEEP.Fill(ix, iy, feds[fed].GetMean())
                trEEP.Fill( ix, iy,  trs[(fed,tr)].GetMean())
                ccuEEP.Fill(ix, iy, ccus[(fed,ccu)].GetMean())
                federrEEP.Fill(ix, iy, feds[fed].GetRMS())
                trerrEEP.Fill( ix, iy,  trs[(fed,tr)].GetRMS())
                ccuerrEEP.Fill(ix, iy, ccus[(fed,ccu)].GetRMS())
                fedskewEEP.Fill(ix, iy, feds[fed].GetSkewness())
                trskewEEP.Fill( ix, iy,  trs[(fed,tr)].GetSkewness())
                ccuskewEEP.Fill(ix, iy, ccus[(fed,ccu)].GetSkewness())
            else:
                fedEEM.Fill(ix, iy, feds[fed].GetMean())
                trEEM.Fill( ix, iy,  trs[(fed,tr)].GetMean())
                ccuEEM.Fill(ix, iy, ccus[(fed,ccu)].GetMean())
                federrEEM.Fill(ix, iy, feds[fed].GetRMS())
                trerrEEM.Fill( ix, iy,  trs[(fed,tr)].GetRMS())
                ccuerrEEM.Fill(ix, iy, ccus[(fed,ccu)].GetRMS())
                fedskewEEM.Fill(ix, iy, feds[fed].GetSkewness())
                trskewEEM.Fill( ix, iy,  trs[(fed,tr)].GetSkewness())
                ccuskewEEM.Fill(ix, iy, ccus[(fed,ccu)].GetSkewness())
        else:
            fedEB.Fill(iphi, ieta, feds[fed].GetMean())
            trEB.Fill( iphi, ieta,  trs[(fed,tr)].GetMean())
            ccuEB.Fill(iphi, ieta, ccus[(fed,ccu)].GetMean())
            federrEB.Fill(iphi, ieta, feds[fed].GetRMS())
            trerrEB.Fill( iphi, ieta,  trs[(fed,tr)].GetRMS())
            ccuerrEB.Fill(iphi, ieta, ccus[(fed,ccu)].GetRMS())
            fedskewEB.Fill(iphi, ieta, feds[fed].GetSkewness())
            trskewEB.Fill( iphi, ieta,  trs[(fed,tr)].GetSkewness())
            ccuskewEB.Fill(iphi, ieta, ccus[(fed,ccu)].GetSkewness())
    
    limits =  [[-5, 5]]*3 + [[ 0, 3]]*3 + [[-2, 2]]*3
    fedhists = [fedEEM, fedEB, fedEEP, federrEEM, federrEB, federrEEP, fedskewEEM, fedskewEB, fedskewEEP]
    drawMultipleGrid(fedhists,"plots/elec/" + histoname + "fed.png", limits= limits)
    trhists = [trEEM, trEB, trEEP, trerrEEM, trerrEB, trerrEEP, trskewEEM, trskewEB, trskewEEP ]
    drawMultipleGrid(trhists,"plots/elec/" + histoname + "tr.png", limits= limits)
    ccuhists = [ccuEEM, ccuEB, ccuEEP, ccuerrEEM, ccuerrEB, ccuerrEEP, ccuskewEEM, ccuskewEB, ccuskewEEP]
    drawMultipleGrid(ccuhists,"plots/elec/" + histoname + "ccu.png", limits= limits)

def addConstant(h,c):
    for i in range(1,h.GetNbinsX()+1):
        for j in range(1,h.GetNbinsY()+1):
            bin = h.GetBin(i,j)
            if h.GetBinEntries(bin):
                h.AddBinContent(bin,c)

def to1d(h,min=float("-inf"), max=float("inf"),bins=100):
    ROOT.gStyle.SetOptStat(111111)
    new = ROOT.TH1D(h.GetName()+ "_1d", h.GetTitle(), bins,min,max)
    new.SetXTitle("ns")
    new.SetYTitle("Crystals")
    for i in range(1,h.GetNbinsX()+1):
        for j in range(1,h.GetNbinsY()+1):
            bin = h.GetBin(i,j)
            if h.GetBinEntries(bin):
                new.Fill(h.GetBinContent(bin))
    return new

def plotTimevsErr(filename,histoname,invert=1,doEnergy=True):
    EB =  ROOT.TH2D(histoname + "EB_time_vs_err",  histoname + " EB",  50, -10, 10, 50, 0, 3) 
    EEP = ROOT.TH2D(histoname + "EEP_time_vs_err", histoname + " EEP", 50, -10, 10, 50, 0, 3)
    EEM = ROOT.TH2D(histoname + "EEM_time_vs_err", histoname + " EEM", 50, -10, 10, 50, 0, 3)
    
    EB.SetZTitle( "Events")
    EB.SetXTitle( "Time"  )
    EB.SetYTitle( "Error" )
    EEP.SetZTitle("Events")
    EEP.SetXTitle("Time"  )
    EEP.SetYTitle("Error" )
    EEM.SetZTitle("Events")
    EEM.SetXTitle("Time"  )
    EEM.SetYTitle("Error" )

    with open(filename) as f:
        for line in f:
            data = line.split()
            x = int(data[0])
            y = int(data[1])
            detector = int(data[2])
            constant = invert*float(data[3])
            err = float(data[4])

            if detector == 0:
                if(x < 0): x+=1
                EB.Fill(constant, err)
            elif detector == -1:
                EEM.Fill(constant, err)
            elif detector == 1:
                EEP.Fill(constant, err)

        return (EEM, EB, EEP) 

def addHistogram(h1,h2,c=1):
    for i in range(1,h1.GetNbinsX()+1):
        for j in range(1,h1.GetNbinsY()+1):
            bin = h1.GetBin(i,j)
            if h1.GetBinEntries(bin):
                h1.SetBinContent(bin,h1.GetBinContent(bin) + c*h2.GetBinContent(bin))

def countRangeHistogram(h1,min=float("-inf"), max=float("inf")):
    inside = 0
    outside = 0
    for i in range(1,h1.GetNbinsX()+1):
        for j in range(1,h1.GetNbinsY()+1):
            bin = h1.GetBin(i,j)
            if min< h1.GetBinContent(bin) < max: 
                inside += 1
            else:
                outside += 1
    return inside,outside

beam1file0 = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_26_events_beam_1-corr-0.dat'
beam2file0 = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_31_events_beam_2-corr-0.dat'
beam1file1 = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_26_events_beam_1-corr-1.dat'
beam2file1 = '/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_31_events_beam_2-corr-1.dat'

oldcalibfile = '/afs/cern.ch/user/p/phansen/public/ecal-timing/CMSSW_7_3_4/src/Usercode/DBDump/dump_EcalTimeCalibConstants_v07_offline__since_00204623_till_4294967295.dat'

customROOTstyle()
ROOT.gROOT.SetBatch(True)

plotElectronics(beam1file0,"beam1",invert=-1)
plotElectronics(beam2file0,"beam2",invert=-1)
plotElectronics(oldcalibfile,"oldcalib")

beam1, beam1err, beam1en = plotCalibration(beam1file0,"beam1",invert=-1)
drawMultipleGrid(beam1 + beam1err,"plots/beam1.png",limits=[[-10,10]]*3 + [[0,2]]*3)

beam2, beam2err, beam2en = plotCalibration(beam2file0,"beam2",invert=-1)
drawMultipleGrid(beam2 + beam2err,"plots/beam2.png",limits=[[-10,10]]*3 + [[0,2]]*3)

old, olderr, = plotCalibration(oldcalibfile,"oldcalib",doEnergy=False)
drawMultipleGrid(old + olderr,"plots/oldcalib.png",limits=[[-10,10]]*3 + [[0,2]]*3)

drawMultipleGrid(beam1 + beam2,      "plots/times.png",  limits=[-10,10])
drawMultipleGrid(beam1err + beam2err,"plots/errors.png", limits=[0,3])
drawMultipleGrid(beam1en + beam2en,  "plots/energy.png", limits=[1,1000],setLogZ=True)

beam1_0_timevserr = plotTimevsErr(beam1file0,"beam1-0", invert = -1)
beam2_0_timevserr = plotTimevsErr(beam2file0,"beam2-0", invert = -1)
beam1_1_timevserr = plotTimevsErr(beam1file1,"beam1-1", invert = -1)
beam2_1_timevserr = plotTimevsErr(beam2file1,"beam2-1", invert = -1)

drawMultipleGrid( beam1_0_timevserr + beam2_0_timevserr, "plots/timevserr_0.png", setLogZ = True)
drawMultipleGrid( beam1_1_timevserr + beam2_1_timevserr, "plots/timevserr_1.png", setLogZ = True)

print("Noisy channels")
for h in beam1err + beam2err:
    print(h.GetName(), countRangeHistogram(h,max=3))


beam1proj = beam1[1].ProjectionY()
beam2proj = beam2[1].ProjectionY()
oldproj =   old[1].ProjectionY()

beam1proj.Scale(1/360.)
beam2proj.Scale(1/360.)
oldproj.Scale(1/360.)

c = ROOT.TCanvas("c", "c", 600,600)
maximum = max([h.GetBinContent(h.GetMaximumBin()) for h in [beam1proj, beam2proj, oldproj]])
minimum = min([h.GetBinContent(h.GetMinimumBin()) for h in [beam1proj, beam2proj, oldproj]])

beam1proj.SetMaximum(maximum)
beam1proj.SetMinimum(minimum)
beam1proj.SetLineColor(ROOT.kRed)
beam1proj.SetMarkerStyle(0)
beam1proj.SetLineStyle(1)
beam1proj.GetXaxis().SetRangeUser(-10,10)
beam1proj.Draw()
beam2proj.SetLineColor(ROOT.kBlue)
beam2proj.SetMarkerStyle(0)
beam2proj.SetLineStyle(1)
beam2proj.Draw("same")
oldproj.SetLineColor(ROOT.kBlack)
oldproj.SetMarkerStyle(0)
oldproj.Draw("same")
c.SaveAs("plots/EBprojection.png")

beam1_avg = beam1[1].Integral(1,360,87,87)/360
beam2_avg = beam2[1].Integral(1,360,87,87)/360
old_avg   = old[1].Integral(1,360,87,87)/360

for i in range(3):
    addConstant(beam1[i], old_avg - beam1_avg)
    addConstant(beam2[i], old_avg - beam2_avg)

drawMultipleGrid(beam1 + beam2,"plots/corrected.png", limits=[-5,5])

print(beam1_avg, beam1[1].Integral(1,360,87,87)/360)
print(beam2_avg, beam2[1].Integral(1,360,87,87)/360)
print(old_avg,   old[1].Integral(1,360,87,87)/360  )

time1d = [to1d(h,min=-10,max=10,bins=21) for h in beam1 + beam2]
rms1d = [to1d(h,min=0,max=10,bins=100) for h in beam1err + beam2err]

ROOT.gStyle.SetStatW(.4)
drawMultipleGrid(time1d,"plots/1d.png",setLogY = True)
drawMultipleGrid(rms1d,"plots/rms1d.png", setLogY = True)

for i in range(3):
    addHistogram(beam1[i], old[i],-1)
    addHistogram(beam2[i], old[i],-1)

drawMultipleGrid(beam1 + beam2,"plots/diff-old.png", limits=[-6,6])

for i in range(3):
    addHistogram(beam1[i], beam2[i],-1)

drawMultipleGrid(beam1,"plots/diff-b1b2.png", limits=[-6,6])

beam1rootfile = ROOT.TFile("/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_26_events_beam_1.root")
beam2rootfile = ROOT.TFile("/afs/cern.ch/work/p/phansen/public/ecal-timing/newCalib/splash_events_run_239895_31_events_beam_2.root")

beam1energytimeEB  = beam1rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEB")
beam1energytimeEEP = beam1rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEEP")
beam1energytimeEEM = beam1rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEEM")

beam2energytimeEB  = beam2rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEB")
beam2energytimeEEP = beam2rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEEP")
beam2energytimeEEM = beam2rootfile.Get("TriggerResults/EcalSplashTiming_0/RechitEnergyTimeEEM")

ROOT.gStyle.SetStatX(.8)
ROOT.gStyle.SetStatW(.4)
drawMultipleGrid( [beam1energytimeEEM, beam1energytimeEB, beam1energytimeEEP, beam2energytimeEEM, beam2energytimeEB, beam2energytimeEEP],
        "plots/energy-vs-time.png", setLogZ=True)

