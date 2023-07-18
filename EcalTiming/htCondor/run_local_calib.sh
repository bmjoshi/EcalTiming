#!/bin/sh -e

JOBID=$1
INPUTFILES=$2;
OUTPUTDIR=$3;

cp -r $CMSSW_BASE ./
cd $CMSSW_VERSION/src

echo -e "evaluate"
eval `scramv1 ru -sh`

cd EcalTiming/EcalTiming/test

echo -e ">>> Run calibration";
python3 run_local.py -s 366396 -e 366442 -r 10 --era 2023B

echo -e "DONE";
