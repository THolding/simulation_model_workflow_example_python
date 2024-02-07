## Model description:
A simple example agent-based model with birth, ageing, marriage and death. Agents are defined by their age, sex and partnered status. Unpartnered adult agents always partner with an unpartnern agent of the opposite sex, if possible. Partnered agents reproduce up to once per time step with a fixed probability. On reproduction a new unpartnered agent, age 0 and random sex is added. Mortality occurs with a fixed probability. Outputs from the model are time series of population size, number of death, and number of births. Output from each simulation run is stored in it's own directory, along with a JSON file containing the parameters used to run the simulation.

### Parameters:

 * `initialPopulationSize`, _n_: The number of agents the model is initialised with. Agents are initialised unpartnered, with a random sex and a random age from a uniform distribution between 0 and 85. Default: 5000.
 * `maxTime`,  _$t\_{max}$_: The maximum number of time steps to run the simulation for. If the population goes extinct the simulation will end before this. Default: 200.
 * `mortalityRate`, _m_: The per-time step probability that an agent will die. Uniform for all ages.
 * `fertilityRate`, _b_: The per-time step probability that a partnered female agent will give birth.
 * `outputDirectory`: File path to a directory for output to be stored. If the directory doesn't exist it will be created.


## Instructions:
The model was developed using Python version 3.8.15. Additional dependencies are listed in `root/requirements.txt` and can be installed e.g. with the pip command `pip install -r root/requirements.txt` (replacing `root` with the directory of the project).

Set the current working directory to the project's root directory.

Analysis scripts are found in `root/analysis` and can be run independently of one another. Explanations of what each does is described in-file at the top of each file. Simulation output from these scripts will be stored in `root/model_output` by default and any plots generated will be stored in `root/plots`. They can be ran from commandline as follows:
`PYTHONPATH=. python3 analysis/01_example_single_parameter_sets.py` This temporarily adds the current working directory (the project root directory) to `PYTHONPATH` to allow the scripts to find one another. If using an IDE just remember to set the path / working directory to the project `root` (not the `analysis` directory).


## Description of files/folders

 * `root/model`: Contains the agent-based model
 * `root/tests`: Unit tests of the model code
 * `root/input_data`: Contains input data used by the model (but there is none ;)
 * `root/model_output`: Model output will be stored here by default
 * `root/plots`: Plots will be stored here by default
 * `root/analysis`: Analysis scripts used to perform the analysis. These can be ran in any order.
	 * `01_example_single_parameter_sets.py`: Examples of running single simulations and replications.
 	* `02_example_comparing_parameter_sets.py`: Examples extracting data from individual runs and comparing output from two parameter sets.
 	* `03_example_parameter_sweeps.py`: Examples of running parameter sweets and extracting data from them.
 * `root/utilities`: A collection of scripts to help with running and analysing the mode. Of interest is `parameters.py` which defines the default parameter set.