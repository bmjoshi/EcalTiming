import sys
import os
import argparse
import random
from math import *

def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(xrange(start, end + 1)).difference(L))

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--inputList", type=str, help="inputList", required=True)
args = parser.parse_args()

with open(args.inputList) as f_list:
   data_list = f_list.read()
lines = data_list.splitlines() 
for iLine,line in enumerate(lines):
   line_new = line
   line_old = line.replace(line.split('/')[len(line.split('/'))-1],'ecalTiming-corr.dat')
   os.system('mv '+line_old+' '+line_new)
