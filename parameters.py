#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_default_params():
    params = {"initialPop": 500, #agents
              "maxTime": 200, #years
              "mortalityRate": 0.015, #per year
              "fertilityRate": 0.02, #per year
              };
    return params;