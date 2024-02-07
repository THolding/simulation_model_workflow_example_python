#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This script runs a sweep of simulations for different fertility rates

import parameters;
from example_model import model;
from example_model.plot_scripts import plot_population_time_series, plot_births_deaths_time_series;
from os import path;

#Boolean 'control' flags to let you turn on/off differant sections of the analysis.
#Useful if you want to replot everything but not run the simulations again etc.
#Can be expanded to more fine-grained control in more complex scripts
runSimulations = True;
makePlots = True;

#Set up variables and parameters needed before we loop over fertility rates
fertilityRates = [0.01, 0.015, 0.02, 0.025, 0.03]; #per year
numReps = 5;
outputPath = path.join("model_output", "fertility_rate_sweep");
defaultRunParams = parameters.get_default_params();

#Run numReps repeat simulations for each fertility rate. For convenience, store
# all the output directories in 'outputLocations' as we go. This allows easy
# plotting later. Alternatively you could run the plots within the loop.
outputLocations = [];
for currentFertilityRate in fertilityRates:
    for rep in range(0, numReps):
        print("Running fertility rate:", currentFertilityRate, "rep:", rep);
        runOutputPath =  path.join(outputPath, "fertilityRate="+str(currentFertilityRate)+"_rep="+str(rep));
        outputLocations.append(runOutputPath);
        
        if runSimulations:
            #First check if the directory already exists. If it does, assume the
            # simulation already exists. This is a simple trick that lets you
            # easily run the sweep on multiple cores by skipping anything another process has already made.
            if path.exists(runOutputPath):
                print("Skipping fertility rate:", currentFertilityRate, "rep:", rep, "because directory already exists...");
                continue;
            
            model.run_model(fertilityRate = currentFertilityRate,
                            mortalityRate = defaultRunParams["mortalityRate"],
                            initialPopulationSize = defaultRunParams["initialPop"],
                            tMax = defaultRunParams["maxTime"],
                            outputDirectory=runOutputPath
                            );


###plot time series data for each simulation
if makePlots:
    for dataPath in outputLocations:
        plot_population_time_series(dataPath, saveDir=path.join(dataPath, "plots"));
        plot_births_deaths_time_series(dataPath, saveDir=path.join(dataPath, "plots"));
    
