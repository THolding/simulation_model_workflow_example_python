#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt;
import pandas as pd;
from os import path, makedirs;


def plot_population_time_series(dataPath, saveDir=None, closeFig=True):
    data = pd.read_table(path.join(dataPath, "timeseries_outputs.csv"), sep=","); #extract data
    
    #plot time series
    if closeFig: #closing the figure is default, otherwise you end up with a million windows open
        plt.ioff(); #this just inhibits anything popping up on the screen while we plot. Otherwise we get flickering effect on the screen when plotting many things quickly
    fig = plt.figure();
    plt.plot(data["popSize"], 'k', linewidth=2);
    plt.xlabel("time (years)");
    plt.ylabel("population size");
    
    if saveDir is not None: #Save the figure to hard drive
        if path.exists(saveDir) == False:
            makedirs(saveDir);
        plt.savefig(path.join(saveDir, "population_size.pdf"));
    
    if closeFig: #Finished plotting so turn interactive (visible) plotting back on.
        plt.close();
        plt.ion();
    
    #return the figure handle, to allow modification/customisation.
    #only makes sense to do this if we haven't closed the figure
    if closeFig==False:
        return fig;
    

def plot_births_deaths_time_series(dataPath, saveDir=None, closeFig=True):
    data = pd.read_table(path.join(dataPath, "timeseries_outputs.csv"), sep=","); #extract data
    
    #plot time series
    if closeFig: #closing the figure is default, otherwise you end up with a million windows open
        plt.ioff(); #this just inhibits anything popping up on the screen while we plot. Otherwise we get flickering effect on the screen when plotting many things quickly
    fig = plt.figure();
    plt.plot(data["deaths"], 'r', linewidth=2, label="deaths");
    plt.plot(data["births"], 'b', linewidth=2, label="births");
    plt.xlabel("time (years)");
    plt.ylabel("birth and death counts");
    plt.legend(loc=0);
    
    if saveDir is not None: #Save the figure to hard drive
        if path.exists(saveDir) == False:
            makedirs(saveDir);
        plt.savefig(path.join(saveDir, "births_and_deaths.pdf"));
    
    if closeFig: #Finished plotting so turn interactive (visible) plotting back on.
        plt.close();
        plt.ion();
    
    #return the figure handle, to allow modification/customisation.
    #only makes sense to do this if we haven't closed the figure
    if closeFig==False:
        return fig;