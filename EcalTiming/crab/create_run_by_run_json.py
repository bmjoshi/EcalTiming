#!/usr/bin/env python3
import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', type=str, help='JSON file containing runs and lumis.', default='json/13TeV_Collisions18_DCSONLY.json')
parser.add_argument('-o', '--output_folder', type=str, help='Path to output folder.', default='json/run_by_run/')
args = parser.parse_args()

OUTPUT = args.output_folder
OUTPUT += args.json.split('/')[-1].replace('.json','')

with open(args.json, 'r') as file_:
    run_lumi_map = json.load(file_)

for run in run_lumi_map:
    tmpdict = {run: run_lumi_map[run]}
    with open('{}_{}.json'.format(OUTPUT, run), 'w') as file_:
        json.dump(tmpdict, file_)
