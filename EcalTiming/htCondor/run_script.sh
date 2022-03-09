#!/bin/sh -e

JOBID=$1
INPUTFILES=$2;
OUTPUTDIR=$3;

cp -r /afs/cern.ch/work/b/bjoshi/Analysis/UMN/CMSSW_10_6_14 ./
cd CMSSW_10_6_14/src

echo -e "evaluate"
eval `scramv1 ru -sh`
export HOME='/afs/cern.ch/user/b/bjoshi'

cd EcalTiming/EcalTiming/htCondor/

eos mkdir ${OUTPUTDIR}

sed -i "s%LISTOFFILES%${INPUTFILES}%" EcalTimingCalibration_cfg.py
sed -i "s%OUTPUT%${OUTPUTDIR}%" EcalTimingCalibration_cfg.py

echo -e ">>> Run calibration";
EcalTimingCalibration EcalTimingCalibration_cfg.py

echo -e "DONE";
