# -------------------------------------
# Script to generate CRAB jobs
# -------------------------------------

#!/usr/bin/env python

import os, sys

from yaml_utils import *
from collections import OrderedDict

from datetime import datetime
from time_utils import *

import json


class crab_job_manager():

    def __init__(self, file_ = ''):

        self.config_file = file_
        self.config = None
        self.mc = False
        self.run_file_map = None
        self.production_tag = ''
        self.parameter_list = ['InputDataset', 'Pycfgparams', 'JSON', 'Map',\
                 'RequestName','WorkArea', 'TransferOutputs','TransferLogs',\
                 'PsetName','MaxJobRunTime','InputDBS','Splitting',\
                 'UnitsPerJob','FilePath','StorageSite','UseWhitelist',\
                 'UseBlacklist','Whitelist','Blacklist', 'IgnoreGlobalBlacklist']
        self.ignore_list = []

    def check_config(self):

        for key_ in self.parameter_list:
            if key_ not in self.config:
                self.ignore_list.append(key_)

    def read_config_file(self, file_):

        self.config_file = file_
        self.config = ordered_load(open(file_), Loader=yaml.SafeLoader)

        self.config['RequestName'] = ''
        self.config['WorkArea'] = 'crab_projects/{}'.format(self.production_tag)

        self.check_config() 

    def produce_crab_submission_script(self):

        cfg_list = []

        with open(self.config['Map'], 'r') as _file:
            self.run_file_map = json.load(_file)

        # check if InputDataset exists
        if 'InputDataset' not in self.config:
            print('Input Dataset not found in the config file!!')
            sys.exit(2)

        dataset = self.config['InputDataset']

        # get the output prefix from the parameters
        output_prefix = None
        outputFile_idx = -1
        for iparam, param_ in enumerate(self.config['Pycfgparams']):
            if 'outputFile=' in param_:
                output_prefix = param_
                outputFile_idx = iparam

        if (outputFile_idx==-1):
            print('outputFile option nor found in pyCfgParams!!')
            sys.exit(2)

        # Print the list of ignored keys
        print('''The following parameters were not specified in the config.\nThey will be ignored in all the CRAB files.''')

        for item_ in self.ignore_list:
            print('\t-{}'.format(item_))

        # If the json is provided, select good runs
        check_runs = False
        good_runs = []
        if 'JSON' in self.config:
            check_runs = True
            with open(self.config['JSON'], 'r') as file_:
                good_runs = json.load(file_).keys()

        for irun, run in enumerate(self.run_file_map):

            if check_runs and run not in good_runs.keys(): continue

            dataset_tag = dataset.replace('/', '_')
            self.config['RequestName'] = '{}_{}'.format(dataset_tag[1:99], irun)
            pyscript_name = 'CRAB_{}{}_{}.py'.format(self.production_tag, dataset_tag, irun)

            # add run number suffix to the outputFile
            self.config['Pycfgparams'][outputFile_idx] = output_prefix.replace('.root','_{}.root'.format(run))
            
            with open('crab_template.txt', 'read') as tmp:
                with open(pyscript_name, 'w') as sub:

                        plain_text = tmp.readlines()
                        new_text = []

                        for line in plain_text:
                            newline = line
                            if 'Template file for CRAB job submission' in line:
                                newline = '# CRAB Job: {}\n'.format(print_creation_timestamp())
                            for key_ in self.parameter_list:
                                if '<{}>'.format(key_) in line:
                                    if key_ not in self.config: newline=''
                                    else:
                                        par_ = self.config[key_]
                                        if 'PycfgParams' in key_:
                                            newline = 'config.Data.pyCfgParams = ['
                                            for param_ in self.config['Pycfgparams']: newline += '"{}",\n'.format(param_)
                                            newline += ']\n'
                                    
                                        elif type(par_)==str:
                                            newline = line.replace('<{}>'.format(key_), "'{}'".format(par_))
                                        else:
                                            newline = line.replace('<{}>'.format(key_), str(par_))
                                            if key_=='Blacklist' and self.config['UseBlacklist']==False:
                                                newline = '#'+newline
                                            if key_=='Whitelist' and self.config['UseWhitelist']==False:
                                                newline = '#'+newline
                            
                            new_text.append(newline)


                        for line in new_text:
                            sub.write(line)

                        cfg_list.append(pyscript_name)

        return cfg_list

    def setup_crab(self, file_, tag_, mc_):

        self.mc = mc_
        self.production_tag = tag_
        self.read_config_file(file_)
        _ = self.produce_crab_submission_script()

        return _
