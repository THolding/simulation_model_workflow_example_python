#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 09:41:02 2024

@author: verwirrt
"""


from os import path;
import numpy as np;

from utilities import parameters;
from utilities import filepaths;
from utilities import run_tools;
from utilities import data_extractors;
from utilities import analysis_tools;


#####A simple test
#It's easy to setup and run simulations, which is nice during the testing and
# exploration phase of a project.
# Say we want to devlop a simple test to confirm that the fertility rate
# does actually affect the population growth rate:
lowFertParams  = parameters.override_default_parameters({"fertilityRate": 0.05,
                                                        "outputDirectory": path.join(filepaths.modelOutputRoot, "test_fertilityRate", "low_fertility_single")});
highFertParams = parameters.override_default_parameters({"fertilityRate": 0.10,
                                                        "outputDirectory": path.join(filepaths.modelOutputRoot, "test_fertilityRate", "high_fertility_single")});
run_tools.run_single(lowFertParams);
run_tools.run_single(highFertParams);
#Using data_extractors to perform the growth rate calculation for each run
lowFertGrowthRate = data_extractors.get_population_growth_rate(path.join(lowFertParams["outputDirectory"]));
highFertGrowthRate = data_extractors.get_population_growth_rate(path.join(highFertParams["outputDirectory"]));


#Using the run_tools functions, it's just as easy to run the test for repeat simulations:
lowFertParams["outputDirectory"] = path.join(filepaths.modelOutputRoot, "test_fertilityRate", "low_fertility_reps");
highFertParams["outputDirectory"] = path.join(filepaths.modelOutputRoot, "test_fertilityRate", "high_fertility_reps");
run_tools.run_reps(lowFertParams, numReps=16, numCores=4);
run_tools.run_reps(highFertParams, numReps=16, numCores=4);
#extract_from_repeats will search for directory structure which indicates repeat
# simulations and run a data_extractor function on each directory. The results
# are returned in an array.
lowFertGrowthRates = analysis_tools.extract_from_repeats(lowFertParams["outputDirectory"], data_extractors.get_population_growth_rate);
highFertGrowthRates = analysis_tools.extract_from_repeats(highFertParams["outputDirectory"], data_extractors.get_population_growth_rate);

print("Mean growth rates (std)\n\tlow fertilty:   ", np.mean(lowFertGrowthRates), " (", np.std(lowFertGrowthRates), ")\n\thigh fertility: ", np.mean(highFertGrowthRates), " (", np.std(highFertGrowthRates), ")", sep="");
