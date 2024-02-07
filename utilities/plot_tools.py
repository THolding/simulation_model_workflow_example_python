#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 11:21:08 2022

"""

from os import path, makedirs;
import matplotlib.pyplot as plt;
import numpy as np;
import pandas as pd;
import pickle;

#from . import data_extractors;
#from . import parameters;
import utilities.data_extractors as data_extractors;
import utilities.parameters as parameters;

#Create a plot of realised age specific pregnancy
def make_realised_pregnancy_rate_plot(directory, saveDirectory=None, closeFig=True, saveData=False, ax=None, fontsize=12):
    meanRates = data_extractors.get_realised_pregnancy_rates(directory);
    sdRates = data_extractors.get_realised_pregnancy_rates_sd(directory);
    x = np.arange(0, len(meanRates))/parameters.timeStepsPerYear;

    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(1,1);
    ax.fill_between(x, meanRates+sdRates, meanRates-sdRates, color='k', alpha=0.5, edgecolor=None);
    ax.plot(x, meanRates);
    ax.set_xlabel("age (years)", fontsize=fontsize);
    ax.set_ylabel("realised pregnancy rate", fontsize=fontsize);
    ax.tick_params(axis="both", which="major", labelsize=fontsize);
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory,"realised_age_specific_pregnancy_rate.png"));
        if saveData:
            output = pd.DataFrame();
            output["age_years"] = x;
            output["realised_pregnancy_mean"] = meanRates;
            output["realised_pregnancy_sd"] = sdRates;
            output.to_csv(path.join(saveDirectory,"realised_age_specific_pregnancy_rate.csv"), sep=",");
    if closeFig: plt.ion(); plt.close();
    return ax;

#Create a plot of realised age specific mishap rates
def make_realised_mishap_rate_plot(directory, saveDirectory=None, closeFig=True, saveData=False, ax=None, fontsize=12):
    meanRates = data_extractors.get_realised_mishap_rates(directory);
    sdRates = data_extractors.get_realised_mishap_rates_sd(directory);
    x = np.arange(0, len(meanRates))/parameters.timeStepsPerYear;
    
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(1,1);
    ax.fill_between(x, meanRates+sdRates, meanRates-sdRates, color='k', alpha=0.5, edgecolor=None);
    ax.plot(x, meanRates);
    ax.set_xlabel("age (years)", fontsize=fontsize);
    ax.set_ylabel("realised mishap rate", fontsize=fontsize);
    ax.tick_params(axis="both", which="major", labelsize=fontsize);
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory,"realised_age_specific_mishap_rate.png"));
        if saveData:
            output = pd.DataFrame();
            output["age_years"] = x;
            output["realised_mishap_mean"] = meanRates;
            output["realised_mishap_sd"] = sdRates;
            output.to_csv(path.join(saveDirectory,"realised_age_specific_mishap_rate.csv"), sep=",");
    if closeFig: plt.ion(); plt.close();
    return ax;


#plot parity frequencies
def make_final_parity_histogram(directory, saveDirectory=None, closeFig=True, ax=None, fontsize=12, rescale=1, colour=None, alpha=1.0):
    parityAgentMap = data_extractors.get_agents_by_completed_fertility(directory);
    parities = sorted(parityAgentMap.keys());
    finalParityCounts = [len(parityAgentMap[parity]) for parity in parities]
    
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(1,1);
    if colour is None:
        ax.bar(parities, np.array(finalParityCounts)*rescale, alpha=alpha);
    else:
        ax.bar(parities, np.array(finalParityCounts)*rescale, alpha=alpha, color=colour);
    ax.set_xlabel("completed fertility", fontsize=fontsize);
    ax.set_ylabel("frequency", fontsize=fontsize);
    ax.tick_params(axis="both", which="major", labelsize=fontsize);
    #ax.set_yticklabels([str(label/1000)+"k" for label in ax.get_yticks()]);
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory,"final_parity_histogram.png"));
    if closeFig: plt.ion(); plt.close();
    return ax;


def make_cumulative_birth_count_plot(directory, saveDirectory=None, closeFig=True, saveData=False, ax=None, fontsize=12):
    meanRates = data_extractors.get_realised_birth_counts(directory);
    sdRates = data_extractors.get_realised_birth_counts_sd(directory);
    x = np.arange(0, len(meanRates))/parameters.timeStepsPerYear;
    
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(1,1);
    ax.fill_between(x, meanRates+sdRates, meanRates-sdRates, color='k', alpha=0.5, edgecolor=None);
    ax.plot(x, meanRates);
    ax.set_xlabel("age (years)", fontsize=fontsize);
    ax.set_ylabel("parity", fontsize=fontsize);
    ax.tick_params(axis="both", which="major", labelsize=fontsize);
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory,"realised_age_specific_parity.png"));
        if saveData:
            output = pd.DataFrame();
            output["age_years"] = x;
            output["realised_parity_mean"] = meanRates;
            output["realised_parity_sd"] = sdRates;
            output.to_csv(path.join(saveDirectory,"realised_age_specific_parity.csv"), sep=",");
    if closeFig: plt.ion(); plt.close();
    return ax;


#Plot the realised mortality rates for male and female agents
def make_realised_mortality_plot(directory, saveDirectory=None, closeFig=True, saveData=False, fontsize=12):
    data = pd.read_table(path.join(directory, "age_sex_binned_realised_mortality_rates.csv"), sep=",");
    if closeFig: plt.ioff();
    plt.figure();
    age = data["age"];
    plt.figure();
    plt.plot(age, data["realisedMortalityRateFemale"], label="female");
    plt.plot(age, data["realisedMortalityRateMale"], label="male");
    plt.xlabel("age (time steps)", fontsize=fontsize);
    plt.ylabel("realised mortality rate", fontsize=fontsize);
    plt.tight_layout();
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory,"age_sex_distributed_realised_mortality_rate.png"));
        if saveData:
            data.to_csv(path.join(saveDirectory,"age_sex_distributed_realised_mortality_rate.csv"), sep=",")
    if closeFig: plt.ion(); plt.close();


#Creates a time series plot of population size
def make_population_size_plot(directory, timeStepsPerYear=2, saveDirectory=None, closeFig=True, saveData=False, ax=None, fontsize=12):
    popSizeTS = data_extractors.get_pop_size_time_series(directory);
    if closeFig: plt.ioff();
    if ax is None:
        fig1, ax = plt.subplots(1,1);
    x = np.arange(len(popSizeTS))/2;
    ax.plot(x, popSizeTS/10000, 'k', linewidth=2);
    ax.set_xlabel("time (years)", fontsize=fontsize); ax.set_ylabel("population size (10,000s)", fontsize=fontsize);
    ax.tick_params(axis="both", which="major", labelsize=fontsize);
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory, "time_series_pop_size.png"));
        if saveData:
            np.savetxt(path.join(saveDirectory,"time_series_pop_size.csv"), popSizeTS, delimiter=",");
    if closeFig: plt.ion(); plt.close();
    return ax;
    

#Creates a time series plot of population the number of births and deaths
def make_birth_death_count_plot(directory, saveDirectory=None, closeFig=True, saveData=False):
    birthsTS, deathsTS = data_extractors.get_births_deaths_time_series(directory);
    
    if closeFig: plt.ioff();
    plt.figure();
    plt.plot(birthsTS, linewidth=2, label="births");
    plt.plot(deathsTS, linewidth=2, label="deaths");
    plt.xlabel("time (time steps)"); plt.ylabel("frequency");
    plt.legend(loc=0);
    plt.tight_layout();
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False:
            makedirs(saveDirectory);
        plt.savefig(path.join(saveDirectory, "time_series_births_deaths.png"));
        if saveData:
            df = pd.DataFrame();
            df["births"] = birthsTS;
            df["deaths"] = deathsTS;
            df.to_csv(path.join(saveDirectory, "time_series_births_deaths.csv"), sep=",", index=False);
    if closeFig: plt.ion(); plt.close();


def make_pop_pyramid_plot(directory, saveDirectory=None, closeFig=True, overrideFilename=None, xlim=None, binSize=10,
                          ax=None, fontsize=12, noLabels=False, noLegend=False):
    def make_labels(ageThresholds, includeUpperCategory=False):
        strs = [str(age) for age in ageThresholds];
        labels = [strs[i-1]+"-"+strs[i] for i in range(1, len(strs))];
        labels = ["0-"+strs[0]]+labels;
        if includeUpperCategory:
            labels = labels+[strs[-1]+"+"];
        return labels;
    
    #Get raw count data
    data = pd.read_table(path.join(directory, "age_sex_binned_realised_mortality_rates.csv"), sep=",");
    femaleFreqs = data["countsFemale"].to_numpy();
    maleFreqs = data["countsMale"].to_numpy();
    
    #make the bin thresholds
    binThresholds = np.arange(binSize, len(femaleFreqs)+binSize, step=binSize);
    femaleBinFreqs = np.array([np.sum(femaleFreqs[i-binSize:i]) for i in binThresholds]);
    maleBinFreqs = np.array([np.sum(maleFreqs[i-binSize:i]) for i in binThresholds]);
    binLabels = make_labels(binThresholds);
    
    if closeFig: plt.ioff();
    if ax is None:
        fig1, ax = plt.subplots(1,1);
    ax.barh(binLabels, femaleBinFreqs, align="center", color='r', label="female");
    ax.barh(binLabels, -maleBinFreqs, align="center", color='b', label="male");
    if noLabels==False:
        ax.set_ylabel("Age category (time steps)", fontsize=fontsize);
    if xlim is not None:
        ax.xlim(xlim);
    if noLabels:
        ax.axes.xaxis.set_ticklabels([]);
        ax.axes.yaxis.set_ticklabels([]);
        #ax.axes.get_xaxis().set_visible(False);
        #ax.axes.get_yaxis().set_visible(False);
    if noLegend==False:
        ax.legend(loc=0, prop={'size': fontsize});
    if saveDirectory is not None:
        if path.exists(saveDirectory)==False: makedirs(saveDirectory);
        if overrideFilename is not None:
            plt.savefig(path.join(saveDirectory, overrideFilename));
        else:
            plt.savefig(path.join(saveDirectory, "population_pyramid.png"));
    if closeFig: plt.ion(); plt.close();



def make_core_individual_run_plots(dataDirectory, saveDirectory=None, closeFigs=True, saveData=True):
    if (saveDirectory is not None) and (path.exists(saveDirectory) == False):
        makedirs(saveDirectory);
    
    make_realised_pregnancy_rate_plot(dataDirectory, saveDirectory=saveDirectory, closeFig=closeFigs, saveData=saveData);
    make_realised_mortality_plot(dataDirectory, saveDirectory=saveDirectory, closeFig=closeFigs, saveData=saveData);
    make_population_size_plot(dataDirectory, saveDirectory=saveDirectory, closeFig=closeFigs, saveData=saveData);
    make_birth_death_count_plot(dataDirectory, saveDirectory=saveDirectory, closeFig=closeFigs, saveData=saveData);
    make_pop_pyramid_plot(dataDirectory, saveDirectory=saveDirectory, closeFig=closeFigs);
    




def make_ibi_parity_mishap_plot(directory, saveDirectory=None, closeFig=True, allScale=1.0,
                                xlim=None, ax=None, figsize=(10,8), fontsize=12, timeStepsPerYear=4, title=None, skipParities=[]):
    
    ####Temp - need to search events and find marriage age in reality!
    conf = data_extractors.get_config_file(directory);
    partnerSeekRate = np.array(conf["basePartnerSeekingRate"]);
    #marriageAge = np.where(partnerSeekRate != 0)[0][0] / conf["timeStepsPerYear"];
    
    #Plot constants
    colours = plt.rcParams['axes.prop_cycle'].by_key()['color'];
    pointScale = 1800*allScale;
    regionScale = 0.3*allScale;
    
    #Load data if it already exists, if not then calculate it then load it.
    dataFilePath = path.join(directory, "processed_IBI_parity_binned_by_CF.pickle");
    if path.exists(dataFilePath) == False:
        data = data_extractors.get_mean_interbirth_intervals_and_mishap_counts_by_parity_structured_by_completed_fertility(directory, timeStepsPerYear=timeStepsPerYear);
        with open(dataFilePath, "wb") as dataFile:
            pickle.dump(data, dataFile);
    else: #data already exists, just load it
        with open(dataFilePath, "rb") as dataFile:
            data = pickle.load(dataFile);
    
    intervalMeans = data["allIntervalMeans"];
    intervalSDs = data["allIntervalSDs"];
    mishapCountMeans = data["allMishapCountMeans"];
    mishapCountSDs = data["allMishapCountSDs"];
    alphas = np.linspace(1.0, 0.25, num=max(intervalMeans.keys())+1);
    
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize);
    
    #Find highest and lowest IBI to use for y axis limits
    yMin = np.inf;
    yMax = 0.0;
    for i in range(len(intervalMeans)): #for each completed fertility group
        if i not in intervalMeans:
            continue;
        for intervalMean in intervalMeans[i]:
            if intervalMean < yMin:
                yMin = intervalMean;
            if intervalMean > yMax:
                yMax = intervalMean;
    ylim = (yMin-0.5, yMax+0.5);
    
    #Plot separate lines for each completed fertility bin
    for j, completedFert in enumerate(sorted(intervalMeans.keys())):
        if completedFert in skipParities:
            continue;
        if completedFert == 0: continue; #ignore agents with 0 successful births (because no intervals exist here)
        mishapPointSizes = np.array(mishapCountMeans[completedFert])*pointScale;
        mishapUncertaintySizes = (np.array(mishapCountMeans[completedFert])+np.array(mishapCountSDs[completedFert]))*pointScale;
        x = np.arange(1, len(intervalMeans[completedFert])+1);
        mishapRegionSizes = np.array(mishapCountMeans[completedFert])*regionScale;
        #mishapRegionUncertaintySizes = (np.array(mishapCountMeans[completedFert])+np.array(mishapRegionSizes))*regionScale; #could be used to add a ring around the mishap points to indicate uncertainty...
        ax.fill_between(x, intervalMeans[completedFert]-mishapRegionSizes, intervalMeans[completedFert]+mishapRegionSizes, color=colours[j%len(colours)], alpha=alphas[j]*0.5, edgecolor="none");
        ax.scatter(x, intervalMeans[completedFert], s=mishapPointSizes, color=colours[j%len(colours)], edgecolors="none", alpha=alphas[j]);
        ax.scatter(x, intervalMeans[completedFert], s=mishapUncertaintySizes, color=colours[j%len(colours)], facecolors="none", alpha=alphas[j]);
        ax.errorbar(x, intervalMeans[completedFert], yerr=intervalSDs[completedFert], color=colours[j%len(colours)], label="Completed fertility="+str(completedFert), capsize=6, alpha=alphas[j]);
    
    #now plot the combined outputs on top:
    combinedIntervalMeans = data["intervalMeans"];
    combinedIntervalSDs = data["intervalSDs"];
    combinedMishapCountMeans = data["mishapCountMeans"];
    combinedMishapCountSDs = data["mishapCountSDs"];
    mishapPointSizes = np.array(combinedMishapCountMeans)*pointScale;
    mishapUncertaintySizes = (np.array(combinedMishapCountMeans)+np.array(combinedMishapCountSDs))*pointScale;
    x = np.arange(1, len(combinedIntervalMeans)+1);
    mishapRegionSizes = np.array(combinedMishapCountMeans)*regionScale;
    #mishapRegionUncertaintySizes = (np.array(combinedMishapCountMeans)+np.array(mishapRegionSizes))*regionScale; #could be used to add a ring around the mishap points to indicate uncertainty...
    ax.fill_between(x, combinedIntervalMeans-mishapRegionSizes, combinedIntervalMeans+mishapRegionSizes, color='k', alpha=0.25, edgecolor="none");
    ax.scatter(x, combinedIntervalMeans, s=mishapPointSizes, color='k', edgecolors="none", alpha=0.5);
    ax.scatter(x, combinedIntervalMeans, s=mishapUncertaintySizes, color='k', facecolors="none", alpha=0.5);
    ax.errorbar(x, combinedIntervalMeans, yerr=combinedIntervalSDs, color='k', label="All agents", capsize=6, alpha=0.5);
    
    ax.set_xlabel("parity", fontsize=fontsize);
    ax.set_ylabel("interval (years)", fontsize=fontsize);
    if xlim is not None:
        ax.set_xlim(xlim);
    ax.set_ylim(ylim);
    ax.legend(loc=0, prop={'size': fontsize-4}, ncol=2);
    if title is not None:
        ax.set_title(title, fontsize=fontsize+2);
    if saveDirectory is not None:
        plt.savefig(path.join(saveDirectory, "interbirth_intervals_with_mishaps_CF_binned.pdf"));
    if closeFig: plt.ion(); plt.close();
    
    return ax;


def make_ibi_parity_plot_simplified(directory, saveDirectory=None, closeFig=True,
                                xlim=None, ax=None, figsize=(10,8), fontsize=12, timeStepsPerYear=4, title=None,
                                plotSubpopulations=True, mainColourOverride=None, subPopColourOverride=None,
                                linewidth=1, alphaMain=0.8, mainErrBarAlpha=0.8, ignoreFirstParity=False, mainErrBars=True, mainOffsetX=0,
                                addTextLabels=True, subpopErrBars=True, subpopAlphaOverride=None, mainLabel=None):
    
    mainColour = mainColourOverride if mainColourOverride is not None else 'k'; 
    
    #marriageAges = data_extractors.get_agent_age_first_married_dict(directory);
    
    #Plot constants
    colours = plt.rcParams['axes.prop_cycle'].by_key()['color'];
    
    #Loads data if it already exists, otherwise calculates it.
    data = data_extractors.get_mean_interbirth_intervals_and_mishap_counts_by_parity_structured_by_completed_fertility(directory, timeStepsPerYear=timeStepsPerYear);
    
    intervalMeans = data["allIntervalMeans"];
    intervalSDs = data["allIntervalSDs"];
    if subpopAlphaOverride is None:
        alphas = np.linspace(1.0, 0.25, num=max(intervalMeans.keys())+1);
    else:
        alphas = [subpopAlphaOverride]*(max(intervalMeans.keys())+1);
    
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize);
    
    #Find highest and lowest IBI to use for y axis limits
    yMin = np.inf;
    yMax = 0.0;
    for i in range(len(intervalMeans)): #for each completed fertility group
        if i not in intervalMeans:
            continue;
        for intervalMean in intervalMeans[i]:
            if intervalMean < yMin:
                yMin = intervalMean;
            if intervalMean > yMax:
                yMax = intervalMean;
    ylim = (yMin-0.5, yMax+0.5);

    
    #Plot separate lines for each completed fertility bin
    subPopColour = subPopColourOverride;
    if plotSubpopulations:
        for j, completedFert in enumerate(sorted(intervalMeans.keys())):
            if completedFert == 0: continue; #ignore agents with 0 successful births (because no intervals exist here)
            if ignoreFirstParity and completedFert == 1: continue;
            x = np.arange(1, len(intervalMeans[completedFert])+1);
            #mishapRegionUncertaintySizes = (np.array(mishapCountMeans[completedFert])+np.array(mishapRegionSizes))*regionScale; #could be used to add a ring around the mishap points to indicate uncertainty...
            #ax.fill_between(x, intervalMeans[completedFert]-mishapRegionSizes, intervalMeans[completedFert]+mishapRegionSizes, color=colours[j%len(colours)], alpha=alphas[j]*0.5, edgecolor="none");
            #ax.scatter(x, intervalMeans[completedFert], s=mishapPointSizes, color=colours[j%len(colours)], edgecolors="none", alpha=alphas[j]);
            #ax.scatter(x, intervalMeans[completedFert], s=mishapUncertaintySizes, color=colours[j%len(colours)], facecolors="none", alpha=alphas[j]);
            if subPopColourOverride is None:
                subPopColour = colours[j%len(colours)];
            if subpopErrBars:
                ax.scatter(x, intervalMeans[completedFert], color=subPopColour, s=30, alpha=alphas[j]);
                ax.errorbar(x, intervalMeans[completedFert], yerr=intervalSDs[completedFert], color=subPopColour, label="Completed fertility="+str(completedFert), capsize=6, alpha=alphas[j], linewidth=linewidth);
            else:
                ax.plot(x, intervalMeans[completedFert], color=subPopColour, label="Completed fertility="+str(completedFert), alpha=alphas[j], linewidth=linewidth);
            if addTextLabels:
                ax.text(x[len(x)-1], intervalMeans[completedFert][-1], str(completedFert), fontsize=fontsize, color=subPopColour);
    

    ### Plotting the main line.
    #now plot the combined outputs on top:
    combinedIntervalMeans = data["intervalMeans"];
    combinedIntervalSDs = data["intervalSDs"];
    x = np.arange(1, len(combinedIntervalMeans)+1);
    #ax.fill_between(x, combinedIntervalMeans-mishapRegionSizes, combinedIntervalMeans+mishapRegionSizes, color='k', alpha=0.25, edgecolor="none");
    #ax.scatter(x, combinedIntervalMeans, s=mishapPointSizes, color='k', edgecolors="none", alpha=0.5);
    #ax.scatter(x, combinedIntervalMeans, s=mishapUncertaintySizes, color='k', facecolors="none", alpha=0.5);
    if ignoreFirstParity:
        x = x[1:];
        combinedIntervalMeans = combinedIntervalMeans[1:];
        combinedIntervalSDs = combinedIntervalSDs[1:];
    
    mainLabelToUse = "All agents";
    if mainLabel is not None:
        mainLabelToUse = mainLabel;
    if mainErrBars:
        ax.errorbar(x+mainOffsetX, combinedIntervalMeans, yerr=combinedIntervalSDs, color=mainColour, linestyle="none", capsize=6, alpha=mainErrBarAlpha, linewidth=linewidth/2);
        ax.plot(x+mainOffsetX, combinedIntervalMeans, color=mainColour, label=mainLabelToUse, alpha=alphaMain, linewidth=linewidth/2);
    else:
        ax.plot(x+mainOffsetX, combinedIntervalMeans, color=mainColour, label=mainLabelToUse, alpha=alphaMain, linewidth=linewidth/2);
    

    ax.set_xlabel("parity", fontsize=fontsize);
    ax.set_ylabel("interval (years)", fontsize=fontsize);
    if xlim is not None:
        ax.set_xlim(xlim);
    ax.set_ylim(ylim);
    #ax.legend(loc=0, prop={'size': fontsize-4}, ncol=2);
    if title is not None:
        ax.set_title(title, fontsize=fontsize+2);
    if saveDirectory is not None:
        plt.savefig(path.join(saveDirectory, "interbirth_intervals_with_mishaps_CF_binned.pdf"));
    if closeFig: plt.ion(); plt.close();
    
    
    return ax;



def make_final_parity_grouped_ages_at_birth_plot(directory, saveDirectory=None, closeFig=True, 
                                                 xlim=None, ax=None, fontsize=12, title=None):
    
    #Load data if it already exists, if not then calculate it then load it.
    dataFilePath = path.join(directory, "processed_AoB_parity_binned_by_CF.pickle");
    if path.exists(dataFilePath) == False:
        dataTup = data_extractors.get_final_parity_grouped_ages_at_birth(directory);
        with open(dataFilePath, "wb") as dataFile:
            pickle.dump(dataTup, dataFile);
    else: #data already exists, just load it
        with open(dataFilePath, "rb") as dataFile:
            dataTup = pickle.load(dataFile);
    
    #unpack data tupple
    dataMeans = dataTup[0];
    dataSDs = dataTup[1];
    
    #Plotting
    if closeFig: plt.ioff();
    if ax is None:
        fig, ax = plt.subplots(figsize=(10,8));
    for finalParity in sorted(dataMeans.keys()):
        x = range(1, finalParity+1);
        ax.errorbar(x, dataMeans[finalParity], yerr=dataSDs[finalParity], label="Completed Fertility = "+str(finalParity), capsize=3);
    ax.set_xlabel("parity", fontsize=fontsize);
    ax.set_ylabel("age (years)", fontsize=fontsize);
    
    if xlim is not None:
        ax.set_xlim(xlim);
    #ax.set_ylim(ylim);
    ax.legend(loc=0, prop={'size': fontsize-4});
    if title is not None:
        ax.set_title(title, fontsize=fontsize+2);
        
    if saveDirectory is not None:
        plt.savefig(path.join(saveDirectory, "ages_at_births_CF_binned.pdf"));
    if closeFig: plt.ion(); plt.close();