#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:15:40 2022

"""

import pytest;
import pandas as pd;
import numpy as np;

###########
# Example unit tests. User-written functions should be tested.


from model.simple_model import initialise_agents, age_agents, pair_unmarried_agents, maxAge, childAge, NO_PARTNER;


#Test that initialised agents have the expected data format
def test_initialise_agents():
    n=5000;
    agents = initialise_agents(numAgents = n);
    assert isinstance(agents, pd.DataFrame);
    assert len(agents) == n;
    assert list(agents.keys()) == ["age", "isFemale", "partner"];
    assert agents["age"].max() <= maxAge;
    assert np.all(agents["age"] >= 0);
    

def test_age_agents():
    n=100;
    agents = initialise_agents(numAgents = n);
    
    firstAges = agents["age"];
    age_agents(agents);
    assert np.all(agents["age"] - firstAges == 1);
    

def test_pair_unmarried_agents():
    n=5000;
    agents = initialise_agents(numAgents = n);
    #agents are initialised with no partner
    assert np.all(agents["partner"] == NO_PARTNER);
    
    #After partnering, at least some agents will be partnered.
    pair_unmarried_agents(agents);
    assert np.any(agents["partner"] != NO_PARTNER);
    
    #Check no children are partnered
    children = agents.loc[agents["age"] <= childAge];
    assert np.all(children["partner"] == NO_PARTNER);
    
    #Create a pair of agents that we know should partner
    couple = pd.DataFrame();
    couple["age"] = [20, 20];
    couple["isFemale"] = [True, False];
    couple["partner"] = [NO_PARTNER, NO_PARTNER];
    pair_unmarried_agents(couple);
    assert np.all(couple["partner"] == [1, 0]); #They should be partnered with each other.


if __name__ == "__main__":
    np.random.seed();
    retcode = pytest.main();



