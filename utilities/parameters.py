#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Define important parameter sets in a single place.
#This makes it trivial to add or modify parameters as the project evolves.
#Storing parameters as a dictionary, named list or object make it easy to
# pass them around between parts of your code, and to write them to file.

from os import path;
from utilities import filepaths;


#Returns the default parameter set. This can then be modified by particular
# scripts or parameter sweeps. E.g.:
#highFertilityParams = get_default_params();
#highFertilityParams["fertilityRate"] = 0.05;
def get_default_params():
    params = {"initialPopulationSize": 5000, #agents
              "maxTime": 200, #years
              "mortalityRate": 0.015, #per year
              "fertilityRate": 0.075, #per year
              "outputDirectory": path.join(filepaths.modelOutputRoot, "default_output_directory"),
              };
    return params;


#Additional parameter sets can be defined if they will be used regularly.
#E.g. if we regularly run sets of simulations with higher mortality and fertility rates:
def get_high_mort_high_fert_params():
    #Start with the default parameters, so any changes that aren't specific
    # to this parameter set will propagate to it.
    params = get_default_params();
    params["mortalityRate"] = 0.03;
    params["fertilityRate"] = 0.15;
    return params;


#A convenient way to write these functions can be using parameter packs
# to override default values:
#This function returns a parameter set where all values are the same as the
# default parameter set, except they key:value pairs defined by 'overrides'.
def override_default_parameters(overrides: dict):
    #Start with the default parameters
    params = get_default_params();
    
    #Check that all of the overriding parameters exist (helps prevent errors due to typos or version mismatch) 
    unrecognisedParamNames = set(overrides.keys()) - set(params.keys());
    if len(unrecognisedParamNames) > 0:
        raise KeyError("Unrecognised parameter name(s): "+ str(unrecognisedParamNames));
    
    #Override parameters:
    params.update(**overrides);

    return params;
