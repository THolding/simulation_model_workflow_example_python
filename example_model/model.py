#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd;
import numpy as np;
from os import path, makedirs;

#Constant parameter values that will never change
missingValue = -1;
childAge = 14;
menopauseAge = 48;
maxAge = 85;

def initialise_agents(numAgents):
    agents = pd.DataFrame();
    #agents.index = np.arange(0, numAgents); #id
    agents["age"] = np.random.randint(low=0, high=maxAge, size=numAgents);
    agents["isFemale"] = np.random.choice([True, False], size=numAgents, replace=True);
    agents["partner"] = np.full((numAgents,), -1);
    return agents;


def add_newly_born_agents(agents, reproducingIDs):
    numToAdd = len(reproducingIDs);
    newAgents = pd.DataFrame();
    newAgents["age"] = np.zeros((numToAdd, ), int);
    newAgents["isFemale"] = np.random.choice([True, False], size=numToAdd, replace=True);
    newAgents["partner"] = np.full((numToAdd,), -1);
    agents = pd.concat([agents, newAgents], ignore_index=True);
    return agents;


def age_agents(agents):
    agents["age"] = agents["age"]+1;
    return agents;


def pair_unmarried_agents(agents):
    wUnmarriedFemales = agents["isFemale"] & (agents["age"] > childAge) & (agents["partner"] == -1);
    unmarriedFemales = agents.index[wUnmarriedFemales].to_numpy();
    wUnmarriedMales = (agents["isFemale"] == False) & (agents["age"] > childAge & (agents["partner"] == -1));
    unmarriedMales = agents.index[wUnmarriedMales].to_numpy();
    
    np.random.shuffle(unmarriedFemales);
    np.random.shuffle(unmarriedMales);
    
    numToMarry = min(len(unmarriedFemales), len(unmarriedMales));
    
    agents.loc[unmarriedFemales[0:numToMarry], "partner"] = unmarriedMales[0:numToMarry];
    agents.loc[unmarriedMales[0:numToMarry], "partner"] = unmarriedFemales[0:numToMarry];
    return agents;


def do_reproduction(agents, fertilityRate):
    canReproduceIds = agents.index[agents["isFemale"] & (agents["partner"] != -1)];
    reproducing = canReproduceIds[np.random.random(len(canReproduceIds)) < fertilityRate];
    numBirths = len(reproducing);
    agents = add_newly_born_agents(agents, reproducing);
    return agents, numBirths;


def do_mortality(agents, mortalityRate):
    wSurviving = np.random.random(len(agents)) >= mortalityRate;
    agents = agents.loc[wSurviving];
    return agents, np.sum(wSurviving==False);


#This is the main model function. It contains all the top-level model logic
# and calls all the constituent functions. Having all the details in these
# functions makes it easy to see the overall steps of the model here without
# getting bogged down with details
def run_model(fertilityRate, mortalityRate, initialPopulationSize, tMax, outputDirectory, verbose=False):
    #First create the output directory if it doesn't already exist
    #Doing this first means we can also use the existance of the directory as
    # a hacky cue that a core is already dealing with this particular run, and
    # prevent different cores duplicating/overwriting one another's work.
    if path.exists(outputDirectory) == False:
        makedirs(outputDirectory);
    
    ###Pre simulation setup:
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
        
        #Append metrics of interest for outputting later
        deathsTimeSeries.append(numDeaths);
        birthsTimeSeries.append(numBirths);
        popSizeTimeSeries.append(len(population));
        
        #Stop running if the population has gone extinct
        if (len(population) == 0):
            break;
    
    ###Finished simulation
    #Accumulate all the output metrics into one data frame
    output = pd.DataFrame();
    output["popSize"] = popSizeTimeSeries;
    output["deaths"] = deathsTimeSeries;
    output["births"] = birthsTimeSeries;
    
    #Write output to file
    outputFile = path.join(outputDirectory, "timeseries_outputs.csv")
    output.to_csv(outputFile, sep=",");
    if verbose: print("Output written to", outputFile);
    


