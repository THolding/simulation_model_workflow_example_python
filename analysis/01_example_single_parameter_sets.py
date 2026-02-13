#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 09:41:02 2024

@author: verwirrt
"""


from os import path;
import json;
import numpy as np;

from utilities import parameters;
from utilities import filepaths;
from utilities import run_tools;
from utilities import status_codes;


#####Run a single simulation with default parameters
params = parameters.get_default_params();
params["outputDirectory"] = path.join(filepaths.modelOutputRoot, "example_run_single");
run_tools.run_single(params, verbose=True);


#####Replicate the last simulation with the same seed
with open(path.join(params["outputDirectory"], "params_used.json"), 'r') as file:
    replicaParams = json.load(file);
replicaParams["outputDirectory"] = path.join(filepaths.modelOutputRoot, "example_run_single_replication");
status = run_tools.run_single(replicaParams, overwriteSeed=replicaParams["seed"], verbose=True); #Note: overwriting the seed using the seed from the previous run
print("Simulation status:", status_codes.descriptions[status]);


#####Repeat runs
params = parameters.get_default_params();
params["outputDirectory"] = path.join(filepaths.modelOutputRoot, "example_run_repeats");
statusList = run_tools.run_reps(params, numReps=16, verbose=True, innerVerbose=False, numCores=4);
#we can check they all ran ok with the return statuses:
print(np.sum(statusList==status_codes.SUCCESSFUL), "simulations completed successfully,",
      np.sum(statusList==status_codes.SKIPPED), "were skipped, and", np.sum(statusList==status_codes.ERROR), "had errors.");
