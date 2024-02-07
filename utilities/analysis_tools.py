#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:05:00 2022

"""

import numpy as np;
from os import path, listdir;
from string import Template;
import re;
import json;
from copy import deepcopy;

from utilities import data_extractors;



#returns a list containing the value extracted by the extractorFunc for each repeat
#rootDirectory: directory contraining all the repeat runs
#extractorFunc: function to use to extract/calculate data from a simulation run
#repDirTemplate: allows changing the directory name for repeats. If set to None it
#                applies the extractorFunc to the rootDirectory only
def extract_from_repeats(rootDirectory, extractorFunc, repDirTemplate = Template("rep=${repNum}")):
    output = [];
    repNum = 0;
    if repDirTemplate is not None:
        while (True): #Keep looping until we generate a repeat directory which is invalid
            repDir = path.join(rootDirectory, repDirTemplate.safe_substitute(repNum=repNum));
            if path.exists(repDir) == False:
                break; #Assume there are no more repeats
            else:
                output.append(extractorFunc(repDir));
                repNum += 1; #check the next repeat number next
    else: #no repeat dir (this means it's not actually a directory of repeats)
        output.append(extractorFunc(rootDirectory));
    return output;



#Extracts data from an N-dimensional parameter sweep. Extraction / calculation
# operation is determined by the extractorFunc. Returned data is a tuple of
# length 3.
#The first element of the tuple contains a list of the names of the parameters
# varied over the sweep (i.e. the N grid dimension names).
#The second tuple element contains dictionary of lists containing the values
# for each parameter (i.e. axis values of the N dimensional grid) as
# {paramName: [paramValues]} pairs.
#The third tuple element contains the N-dimensional grid. This is setup as a
# recursively nested dictionary (N levels deep). This allows access using:
# data[0.05][0.2]["high"] for a 3-parameter sweep, for example. Here the three
# index values correspond to a unique set of parameter values used to in the
# parameter sweep. The order is defined by the paramNames (first tuple element)
#Function arguments:
#rootDirectory: the sweep's root directory
#extractorFunc: a function which extracts or calculates the particular piece of
#               data you want. Should take a directory path as it's argument
#repDirTemplate: allows changing the directory name for repeats. If set to None it
#                applies the extractorFunc to the rootDirectory only (i.e. from a
#                sweep with no repeat runs performed)
def extract_from_sweep(rootDirectory, extractorFunc, repDirTemplate = Template("rep=${repNum}")):
    def construct_recursive_dictionary_storage(paramNames, paramValues):
        output = None;
        for paramName in paramNames[::-1]:
            output = {val: deepcopy(output) for val in paramValues[paramName]};
        return output;
    
    #Sets a value in the recursive dictionary structure.
    def set_recursive_dictionary_value(dictionary, keys, valueToStore):
        if len(keys) == 1:
            dictionary[keys[0]] = valueToStore;
        else:
            set_recursive_dictionary_value(dictionary[keys[0]], keys[1:], valueToStore);
    
    
    with open(path.join(rootDirectory, "sweep_info.json"), 'r') as file:
        sweepInfo = json.load(file);
    
    #Create a nested dictionaries where keys correspond to paramNames (in order)
    # and the innermost of which contain one element for each parameter value combination
    paramNames = list(sweepInfo.keys());
    data = construct_recursive_dictionary_storage(paramNames, sweepInfo);
    
    #get list of all the directories in the rootDirectory
    sweepDirs = [path.join(rootDirectory, directory) for directory in listdir(rootDirectory) if path.isdir(path.join(rootDirectory, directory))];
    
    for sweepDir in sweepDirs:
        #extracting parameter values from the parameter file (rather than the directory name)
        exampleSimDir = sweepDir if repDirTemplate is None else path.join(sweepDir, repDirTemplate.safe_substitute(repNum=0));
        params = data_extractors.get_params_file(exampleSimDir);
        paramVals = [params[paramName] for paramName in paramNames];
        
        #extract and store the data we're interested in
        extractedData = extract_from_repeats(path.join(rootDirectory, sweepDir), extractorFunc);
        set_recursive_dictionary_value(data, paramVals, extractedData);
    
    return paramNames, sweepInfo, data;
