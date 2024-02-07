#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:02:06 2024

@author: tom holding
"""

#Named variables for the returned status values from the model and run_tools functions
SUCCESSFUL = 0;
ERROR = -1;
SKIPPED = -2;

descriptions = {SUCCESSFUL: "successfully completed",
                ERROR: "an error occured",
                SKIPPED: "skipped to avoid overwriting existing files",
                };