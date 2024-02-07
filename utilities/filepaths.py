#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:10:38 2022

"""

#This file defines file paths to directories which will be used repeatedly.
#It makes referencing these directories more comprehendible, and also means
# that there's a single place that changes need to be made if we change the
# directory structure later on.

from os import path;

projectRoot = path.abspath(path.join(path.dirname(__file__), ".."));
inputDataDir = path.join(projectRoot, "input_data");
modelOutputRoot = path.join(projectRoot, "model_output");
figuresOutputRoot  = path.join(projectRoot, "figures");
