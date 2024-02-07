#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd;
import numpy as np;
from os import path, makedirs;
import json;

from utilities import status_codes;

######
#A simple example agent-based model.
#Agents are defined by their age, sex and partnered status.
#Unpartnered agents always partner with an unpartner agent of the opposite sex
# if possible, but only from age 14 time steps.
#Partnered agents reproduce up to once per time step with a fixed probability.
#On reproduction a new unpartnered agent, age 0 and random sex is added.
#Mortality occurs with a fixed probability.
#Output: time series of population size, number of death, and number of births.


#Constant parameter values that will never change. If they might change they
# should go in the parameters file.
childAge = 14; #Age of transition from child to adult (children can't form partnerships)
maxAge = 85; #Only used for generating the initial population
NO_PARTNER = -1; #Used to indicate an agent has no partner


#Initialise numAgents agents. Returns a pandas data frame containing agent state
def initialise_agents(numAgents):
    agents = pd.DataFrame();
    #agents.index = np.arange(0, numAgents); #id
    agents["age"] = np.random.randint(low=0, high=maxAge, size=numAgents);
    agents["isFemale"] = np.random.choice([True, False], size=numAgents, replace=True);
    agents["partner"] = np.full((numAgents,), NO_PARTNER);
    return agents;


#Performs partnering of unmarried adults.
def pair_unmarried_agents(agents):
    wUnmarriedFemales = agents["isFemale"] & (agents["age"] > childAge) & (agents["partner"] == NO_PARTNER);
    unmarriedFemales = agents.index[wUnmarriedFemales].to_numpy();
    wUnmarriedMales = (agents["isFemale"] == False) & (agents["age"] > childAge) & (agents["partner"] == NO_PARTNER);
    unmarriedMales = agents.index[wUnmarriedMales].to_numpy();
    
    np.random.shuffle(unmarriedFemales);
    np.random.shuffle(unmarriedMales);
    
    numToMarry = min(len(unmarriedFemales), len(unmarriedMales));
    
    agents.loc[unmarriedFemales[0:numToMarry], "partner"] = unmarriedMales[0:numToMarry];
    agents.loc[unmarriedMales[0:numToMarry], "partner"] = unmarriedFemales[0:numToMarry];
    return agents;


#Reproduction, returns number of births. add_newly_born_agents handles creation
# of new agents.
def do_reproduction(agents, fertilityRate):
    canReproduceIds = agents.index[agents["isFemale"] & (agents["partner"] != NO_PARTNER)];
    reproducing = canReproduceIds[np.random.random(len(canReproduceIds)) < fertilityRate];
    numBirths = len(reproducing);
    agents = add_newly_born_agents(agents, reproducing);
    return agents, numBirths;


#Checks for agent death and removes dead agents from the population.
#Returns number of deaths.
def do_mortality(agents, mortalityRate):
    wSurviving = np.random.random(len(agents)) >= mortalityRate;
    agents = agents.loc[wSurviving];
    return agents, np.sum(wSurviving==False);


#Increments the age of all living agents.
def age_agents(agents):
    agents["age"] = agents["age"]+1;
    return agents;


#Creates newly born agents, given the agent IDs (indices) of the reproducting agents.
def add_newly_born_agents(agents, reproducingIDs):
    numToAdd = len(reproducingIDs);
    newAgents = pd.DataFrame();
    newAgents["age"] = np.zeros((numToAdd, ), int);
    newAgents["isFemale"] = np.random.choice([True, False], size=numToAdd, replace=True);
    newAgents["partner"] = np.full((numToAdd,), NO_PARTNER);
    agents = pd.concat([agents, newAgents], ignore_index=True);
    return agents;



#This is the main model function. It contains all the top-level model logic
# and calls all the constituent functions. Having all the details in these
# functions makes it easy to see the overall steps of the model here without
# getting bogged down with details
def run_model(params, verbose=False):
    #First create the output directory if it doesn't already exist
    #Doing this first means we can also use the existance of the directory as
    # a hacky cue that a core is already dealing with this particular run, and
    # prevent different cores duplicating/overwriting one another's work.
    if path.exists(params["outputDirectory"]) == False:
        makedirs(params["outputDirectory"]);
    
    #Now write the parameters to the output directory.
    with open(path.join(params["outputDirectory"], "params_used.json"), "w") as file:
        json.dump(params, file, indent=4);
    
    
    #For convenience, extract parameters as local variables
    initialPopulationSize = params["initialPopulationSize"];
    tMax = params["maxTime"];
    fertilityRate = params["fertilityRate"];
    mortalityRate = params["mortalityRate"];


    ###Pre simulation setup:
    #Set the random seed
    np.random.seed(params["seed"]);
    #Initialise places to store output data
    popSizeTimeSeries = [];
    deathsTimeSeries = [];
    birthsTimeSeries = [];
    
    #initialise the agent population
    population = initialise_agents(initialPopulationSize);
    
    
    ###Main simulation loop:
    for t in range(0, tMax):
        if verbose:
            print("t = ", t, " Population size: ", len(population));
        
        #Each step in the simulation is clearly layed out in human readable function names
        #details of each step can be found in their respective functions
        population = pair_unmarried_agents(population);
        population, numBirths = do_reproduction(population, fertilityRate);
        population, numDeaths = do_mortality(population, mortalityRate);
        population = age_agents(population);
        
        #Store outputs
        deathsTimeSeries.append(numDeaths);
        birthsTimeSeries.append(numBirths);
        popSizeTimeSeries.append(len(population));
        
        #Stop running if the population has gone extinct
        if (len(population) == 0):
            break;
    
    ###Finished simulation
    #Accumulate all the output into one data frame
    output = pd.DataFrame();
    output["popSize"] = popSizeTimeSeries;
    output["deaths"] = deathsTimeSeries;
    output["births"] = birthsTimeSeries;
    
    #Write output to file
    outputFile = path.join(params["outputDirectory"], "time_series_outputs.csv")
    output.to_csv(outputFile, sep=",");
    if verbose:
        print("Output written to", outputFile);
    
    #Returning a value can be used to indicate success or failure or other
    # information aboutt he run, which other parts of the workflow can react
    # to. By convention returning 0 is success / no error
    return status_codes.SUCCESSFUL;
    


