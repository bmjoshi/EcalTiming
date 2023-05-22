import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("list", type=str, default="foo", help="File containing the list of files to be hadded")
parser.add_argument("start_run", type=int, default=366873, help="starting run")
parser.add_argument("end_run", type=int, default=366891, help="ending run")
args = parser.parse_args()

with open(args.list) as f_:
    files = [ l.strip("\n\r") for l in f_.readlines() ]

cmd = 'hadd -f timing_reco_selection_{}_{}.root '.format(args.start_run, args.end_run)+' '.join(files)
os.system(cmd)
