#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:15:40 2022

"""

#This file contains functions which help with running the model
#Why do we need this? They're designed to:
#   1) Reduce boilerplate assoiated with setting up and running models - it quicker to setup a new model run
#   2) Simplifying the interface for running models reduces opportunities for errors e.g. passing in the wrong parameters
#   3) Define a consistent workflow for running models and storing model output.
#These functions start with a simple single model run, and build up to more complex way of running models (e.g. sets of repeat rungs and parameter sweeps).
#There can additionally be support for running on multiple cores, etc.

from os import path, urandom, makedirs;
import sys;
from concurrent.futures import ProcessPoolExecutor, wait;
import numpy as np;
import json;

from model import simple_model;
from utilities import status_codes;



#Runs a single simulation
#params: Dictionary containing the parameter set
#skipIfExists: Should the parameter overwrite existing data? Default behaviour is not to do this and instead print a message to the console.
def run_single(params, skipIfExists=True, overwriteSeed=None, verbose=False):
    if path.exists(params["outputDirectory"]) and skipIfExists == True:
        print("Skipping simulation with outputDirectory", params["outputDirectory"], "because it already exists...");
        return status_codes.SKIPPED;
    
    if overwriteSeed is None:
        #Set the seed to a value we know
        params["seed"] = int.from_bytes(urandom(4), sys.byteorder);
    else:
        params["seed"] = overwriteSeed;
    
    #run the model
    #This could involve calling a Python function or running something from the commandline.
    #In this case, the model is implemented with Python so we can just run it directly.
    status = simple_model.run_model(params, verbose);
    
    ####Additional steps can be added here, e.g. if you have a set of statistics or plots you always want to produce for any simulation:
    #if calcBasicStats:
    #    calc_basic_stats(params["outputDirectory"]);
    #if makeBasicPlots:
    #    plot_tools.make_diagnostic_individual_run_plots(params["outputDirectory"]), saveDirectory=path.join(params["outputDirectory"], "plots"), closeFigs=True);
    
    return status;



#Same as run_single but repeats the run numReps times.
#Output for each simulation will be stored in it's own directory by appending
# 'rep=#' to the baseParams['outputDirectory'] path.
#Run the model with a particular parameter set a fixed number of times, sorting output into separate folders
#baseParams: the parameter set to be used (the output directory will be modified)
#numReps: the number of repeats to run
#verbose: should the function output progress through the set of repeat simulations?
#innerVerbose: should each individual simulation be verbose? This only works for single core.
#numCores: If None only a single process is used, otherwise the number of cores specified
#           will be used and separate processes created for each repeat simulation.
def run_reps(baseParams, numReps, verbose=True, innerVerbose=False, numCores=None):
    with ProcessPoolExecutor(max_workers=numCores) as executor:
        processHandles = [];
        for rep in range(0, numReps):
            params = baseParams.copy();
            params["outputDirectory"] = path.join(baseParams["outputDirectory"], "rep="+str(rep));
            if numCores is None:
                print("running", params["outputDirectory"]);
                run_single(params, verbose=innerVerbose);
            else:
                print("queuing", params["outputDirectory"]);
                handle = executor.submit(run_single, params, verbose=False);
                handle.add_done_callback(lambda future,name=params["outputDirectory"] : print("Completed running: "+str(name))); #Note: using an additional argument and providing a default value allows the lambda to capture by value instead of reference.
                processHandles.append(handle);
        wait(processHandles);
        
        #Return an array of model return statuses.
        statusList = np.array([processHandle.result() for processHandle in processHandles]);
        return statusList;
        


#Run simulations for a parameter sweep over N dimensions.
#baseParams: parameter set containing parameter values which are constant across all runs
#paramNames: a list of parameters whose values change
#paramValueLists: a list of lists (or arrays). Each element in the outter list
#                 contains the parameter values for the corresponding element in paramNames
#numReps: number of repeat simulations to run for each unique combination of parameter values
#numCores: number of CPU cores to use. Default is None meaning no new processes are created.
#verbose: prints feedback on queued and completed simulation runs.
def run_sweep(baseParams, paramNames, paramValueLists, numReps=1, numCores=None, verbose=True):
    if not (isinstance(paramNames, list) or isinstance(paramNames, np.ndarray)):
        paramNames = [paramNames];
    if not (isinstance(paramValueLists[0], list) or isinstance(paramValueLists[0], np.ndarray)):
        paramValueLists = [paramValueLists];
    
    #Generate all parameter sets by iterating every combination of parameter value for each parameter name provided
    #Here we just store the differences from the base parameter set
    #The 'paramSetNames' becomes the output directory unique for that parameter set
    paramSetOverrides = [{}];
    paramSetNames = [""];
    for paramNameIdx, paramName in enumerate(paramNames):
        newParamSetOverrides = [];
        newParamSetNames = [];
        for paramVal in paramValueLists[paramNameIdx]:
            outputDirToken = "_" if paramNameIdx!=0 else "";
            outputDirToken += paramName+"="+str(paramVal);
            for paramSetNameIdx, oldParamSetOverride in enumerate(paramSetOverrides):
                newParamSetNames.append(paramSetNames[paramSetNameIdx] + outputDirToken);
                #Add the new parameter's override values
                newParamSetOverride = oldParamSetOverride.copy();
                newParamSetOverride[paramName] = paramVal;
                newParamSetOverrides.append(newParamSetOverride);
        paramSetOverrides = newParamSetOverrides;
        paramSetNames = newParamSetNames;
    
    #Write the sweep information to the base directory
    sweepInfo = {paramNames[i]: list(paramValueLists[i]) for i in range(len(paramNames))};
    if path.exists(baseParams["outputDirectory"]) == False:
        makedirs(baseParams["outputDirectory"]);
    with open(path.join(baseParams["outputDirectory"], "sweep_info.json"), 'w') as file:
        json.dump(sweepInfo, file, indent=2);
    
    #Pass these parameter sets onto the run_param_sets function actually run them
    return run_param_sets(baseParams, paramSetNames, paramSetOverrides, numCores=numCores, numReps=numReps, verbose=verbose);



#Run the model for a set of parameters sets. Uses baseParams and updates it for each
# paramSetOverride.
#baseParams: The parameter set containing values which are common to all simulations.
#paramSetNames: The names for each parameter set to run. These become directory names.
#paramSetOverrides: Dictionaries defining the particular values which should be
#   overwritten in the baseParams for each unique parameter set.
#numReps: how many repeats to run for each unique parameter set. When set
#   to None no 'rep=#' subdirectory is created.
#numCores: How many CPU cores to use. When set to None no new processes are created
#   and all work is done using the existing process.
#verbose: prints feedback on queued and completed simulation runs.
def run_param_sets(baseParams, paramSetNames, paramSetOverrides, numReps=1, numCores=None, verbose=True):
    if numCores is None: #Single CPU core, no new processes created
        outputStatuses = [];
        for i in range(len(paramSetNames)):
            #Create the full parameter set for the current set of overrides
            params = baseParams.copy();
            params.update(paramSetOverrides[i]);
            params["outputDirectory"] = path.join(params["outputDirectory"], paramSetNames[i]);
            if numReps is None: #Special case for when numReps is None (don't create an extra subdirectory)
                outputStatuses.append(run_single(params));
            else:
                outputStatuses += run_reps(params, numReps, verbose=False);
        return outputStatuses;
    
    else: #Run on multiple CPUs
        with ProcessPoolExecutor(max_workers=numCores) as executor:
            processHandles = [];
            for i in range(len(paramSetNames)):
                #Create the full parameter set for the current set of overrides
                params = baseParams.copy();
                params.update(paramSetOverrides[i]);
                params["outputDirectory"] = path.join(params["outputDirectory"], paramSetNames[i]);
                
                #Queue the simulations
                if numReps is None: #Special case for when numReps is None (don't create an extra subdirectory)
                    handle = executor.submit(run_single, params, verbose=False);
                    if verbose:
                        print("Queued parameter set:", paramSetNames[i]);
                        handle.add_done_callback(lambda future,name=paramSetNames[i]:print("Completed running: "+str(name))); #Note: using an additional argument and providing a default value allows the lambda to capture by value instead of reference.
                    processHandles.append(handle);
                else: #more than one repeat: note we don't rely on run_reps here because we want all the processes to be in the same ProcessPoolExecutor to avoid excess wait times
                    for r in range(numReps):
                        repParams = params.copy();
                        repParams["outputDirectory"] = path.join(params["outputDirectory"], "rep="+str(r));
                        handle = executor.submit(run_single, repParams, verbose=False);
                        if verbose:
                            print("Queued parameter set:", path.join(paramSetNames[i], "rep="+str(r)));
                            handle.add_done_callback(lambda future,name=paramSetNames[i]+" rep="+str(r) : print("Completed running: "+str(name))); #Note using an additional argument and providing a default value allows the lambda to capture by value instead of reference.
                        processHandles.append(handle);
            wait(processHandles);
            #Get simulation return codes
            outputStatuses = [ph.result() for ph in processHandles];
            return outputStatuses;
