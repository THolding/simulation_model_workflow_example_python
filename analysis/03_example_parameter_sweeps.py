#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 09:41:02 2024

@author: verwirrt
"""

from os import path;
import numpy as np;
import matplotlib.pyplot as plt;

from utilities import parameters;
from utilities import filepaths;
from utilities import run_tools;
from utilities import data_extractors;
from utilities import analysis_tools;


#####Parameter sweeps
#Perform a parameter sweep over 'fertilityRate' parameter, and calculate the
# mean population growth rates for each
fertilityRateSweepParams = parameters.get_default_params();
fertilityRateSweepParams["outputDirectory"] = path.join(filepaths.modelOutputRoot, "fertility_rate_sweep");
#Define the fertility rates we want to use:
fertilityRates = np.linspace(0.05, 0.15, num=11);
run_tools.run_sweep(fertilityRateSweepParams, ["fertilityRate"], fertilityRates, numReps=10, numCores=4, verbose=True)

#Extract the data using extract_from_sweep
#The function returns the parameter names, parameter values, and a dictionary.
#The paramVals can be used to index into the dictionary to get the data
# corresponding to each parameter set, e.g. growthRates[0.05] gives us the
# growth rates for when fertilityRate was set to 0.05.
#Note, since we ran 10 repeats for each simulation, we have 10 versions of the
# data for each unique parameter value.
paramNames, paramVals, growthRates = analysis_tools.extract_from_sweep(fertilityRateSweepParams["outputDirectory"], data_extractors.get_population_growth_rate);
#Plot the growth rates
plt.figure();
plt.scatter(paramVals["fertilityRate"], [np.nanmean(growthRates[val]) for val in paramVals["fertilityRate"]]);
plt.xlabel("fertility rate");
plt.ylabel("population growth rate");




#####Multi-parameter sweeps
#The same works for sweeping over an arbitrary number of parameters.
#In this case: fertility rate, mortality rate, and initial population size
multiSweepParams = parameters.get_default_params();
multiSweepParams["outputDirectory"] = path.join(filepaths.modelOutputRoot, "multi_param_sweep");
fertilityRates = [0.05, 0.10, 0.15];
mortalityRates = [0.04, 0.05, 0.06];
initialPopulationSizes = [4000, 5000, 6000];
run_tools.run_sweep(multiSweepParams, ["fertilityRate", "mortalityRate", "initialPopulationSize"], [fertilityRates, mortalityRates, initialPopulationSizes], numReps=10, numCores=4);
#Extract the data
paramNames, paramVals, popSizeTSData = analysis_tools.extract_from_sweep(multiSweepParams["outputDirectory"], data_extractors.get_pop_size_time_series);
paramNames, paramVals, growthRates = analysis_tools.extract_from_sweep(multiSweepParams["outputDirectory"], data_extractors.get_population_growth_rate);
#A sweep over 3 parameters (with 10 repeats), this means the data extracted
# is stored in 3+1 dimensions. 'paramNames' defines the order to index these
# dimensions (note, the repeats are always last). 'paramVals' gives us the
# values to use to index them. For example: growthRates[0.1[0.06][4000]
# indexes all repeats of the parameter set with fertilityRate=0.1,
# mortalityRate=0.06 and initialPopulationSize=4000. Similarly
# popSizeTSData[0.1][0.06][4000][0] indexes the time series of population size
# for the same parameter set, but only the first repeat.
plt.figure();
plt.plot(popSizeTSData[0.1][0.06][4000][0]);
plt.xlabel("time step");
plt.ylabel("population size");

plt.figure();
for mortalityRate in paramVals["mortalityRate"]:
    plt.plot(paramVals["fertilityRate"], [np.nanmean(growthRates[fertRate][mortalityRate][5000]) for fertRate in paramVals["fertilityRate"]], label="Mortality rate = "+str(mortalityRate));
plt.legend(loc=0);
plt.xlabel("fertility rate");
plt.ylabel("population growth rate");






