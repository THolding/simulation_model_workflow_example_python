#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 07:46:57 2022

"""

#This file provides a single place to define functions for data access,
# transformation and secondary calculation functions.
#Prevents code duplication, improves readability and meanst here's a single
# point to update these in the code.

from os import path;
import pandas as pd;
import numpy as np;
import json;


#Returns an array containing the time series of population size
def get_pop_size_time_series(directory):
    return pd.read_table(path.join(directory, "time_series_outputs.csv"), sep=",", usecols=["popSize"])["popSize"].to_numpy();


#Returns the average growth rate of the populatuon (from initial population to last time step).
#Time in 'time steps'
def get_population_growth_rate(directory):
    popSizeTS = get_pop_size_time_series(directory);
    return np.log(popSizeTS[-1]/popSizeTS[0])/(len(popSizeTS));


#Returns an array containing the time series of the birth:death ratio
def get_birth_death_ratio_time_series(directory):
    tsData = pd.read_table(path.join(directory, "time_series_outputs.csv"), sep=",")
    birthDeathRatio = tsData["births"].to_numpy() / tsData["deaths"].to_numpy();
    return birthDeathRatio;


#Returns the parameters used in a simulation in dictionary format.
def get_params_file(directory):
    with open(path.join(directory, "params_used.json"), "r") as f:
        config = json.load(f);
        return config;



