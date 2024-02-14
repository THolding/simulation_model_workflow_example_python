# Example Python workflow for agent-based models
This is the readme for the workflow explanation. For the readme for the example model (containing instructions on how to run the examples) see `example_readme.md`.

If you want to get into the details then the place to start (besides this readme file) the example scripts in the `analysis` directory.


## Overall principles:
The setup described here is just something I've slowly converged on over the years. I'm sure there are better ways to do a lot of these things (please do tell me about them!) Some of it might be over-engineered, but it's also reusable with minimal modifications. I'm very interested to hear suggestions or to compare with other people's setups. None of it is specific to Python and could be implemented in any other language. A lot of code probably is specific to data generating simulation models, however.

Most of the useful stuff is in the `utilities/run_tools.py`, `utilities/data_extractors.py` and `utilities/analysis_tools,py` files, which contain functions that can be used together to setup sets of simulation runs, extract or process data from simulation runs, and automatically traverse the directory tree to provide simulation output in a consistent format. This makes running, reading data and processing data from simulations just a matter of a few lines of code, regardless as to whether you're running a multi-parameter sweep or a single simulation. For examples, see the scripts in the `analysis` directory.

The basic idea is to:

 1. _Reduce the opportunity to make errors._ Humans aren't really very good at for reading and writing code, we're all pretty bad at it and it's incredibly easy to make mistakes. If we're lucky the mistake will break the code 'loudly' and produce error messages so we know to fix it. If we're unlucky the code still runs and a more subtle bug is introduced - and who knows when/if anyone will ever find it. Besides testing, reducing the opportunity to make these mistakes is the only way to prevent them. I try to do this by portioning code into reusable functions. This reduces the amount of code I can make mistakes in and increases the chance that I'll actually spot a mistake (because the code gets a lot of use). It also means that, when it comes to updated the code or fix a bug, there's hopefully only one place which needs changing and testing. Without doing this, I would spend a lot more time having to scan through all the files in a project looking for a specific piece of logic to update. It's so easy to miss one, and if I fix the others, it's unlikely that I or anyone else ever notice the one that's left.

 2. _Improve code readability, especially at the 'top level' (e.g. analysis scripts)._ This is largely about naming chunks of code using functions. Even if a function only encapsulates one or two lines of code and I might not use it again, a human-readable name lets me (or anyone brave enough to try to use my code) skip over the details when trying to understand what's going on at a larger scale. It also helps when writing unit tests.

 3. _Introduce quality of life functions_ to stop me getting distracted on the coding details so I can focus on running/understanding the model's behaviour. I used to spend a lot of time copy and pasting chunks of code to set up, run, and process data from simulations. Now I have functions which do most of this for me, and this cuts down on errors but also leaves me to focus on the bigger picture without getting bogged down in code details. The aim is for the 'top level' analysis scripts to look more a(n almost) human-readable recipe consisting of a series of function calls rather than a lot of complex nested logic.


## Folder structure:
* Project root directory:
	* Git repository directory (what you'll see and use as the root directory if you download this repo)
		* `model`: The model(s) itself.
		* `input_data`: Any input data used in the analysis or by the model.
		* `utilities`: Most of the good stuff is in here: important parameter sets, quality of life functions, tools for keeping everything organised. Lots of this is reusable between projects.
		* `tests`: Unit tests and any other tests. Larger tests of model behaviour might be better off in the `analysis` directory, especially if they're going to end up in a paper / supplementary.
		* `analysis`: One-off scripts which run a piece of analysis. They should ideally be self-contained, but might need to run in sequence.
		* `model_output`: Contains model output. This is usually excluded from the repository using .gitignore and backed up elsewhere.
		* `plots`: Plots created by the scripts in the `analysis` directory go here.
	* Various "for me only" notes: E.g. Which thing I'm currently working on (because I'll forget over the weekend), what still needs doing, what I plan to bring up in the next meeting with collaborators, useful ideas that I've not yet explored but don't want to forget, pros and cons of getting a dog, etc.... This doesn't get pushed to the git repository because it's outside the repo's root directory.


## The model (`model/simple_model.py`)
The main reason to have this separate from any other code is to make it easy to find. It can also be useful to keep them clearly separate when there are more than one model (which could use shared helper functions).


## Parameters (`utilities/parameters.py`)
Defines important parameter sets. This includes the default values, but can also include other parameter sets that are used often or have some special status/purpose. All additional parameter sets should be defined as deviations from the default (or from another parameter set that itself derives from the default, etc.) This means that if a default value changes, or a new parameter is added, there is just one place to make the update and the changes propagate through to the other parameter sets.


## File paths (`utilities/filepaths.py`)
Defines important file paths. It's useful to define variables for any file path you reuse a lot. It just means that there's only one place to change them when things inevitable change. It also helps readability when you're concatinating filepaths in-code. Typically I define, at a minimum, the project root, the model output directory and a directory for figures.


## Run tools (`utilities/run_tools.py`)
These are the functions I use to run simulations. I almost never run the model directly because there's always extra code around setting up and tearing down simulations. Using functions to do thise helps in two ways: 1) It helps to standardise the process, such enforcing a standard way of organising directory structure for sets of simulations. as creating subdirectories, setting and storing random seeds and model parameters. 2) It reduces the chance I'll make a mistake. By simplifying the code there is less to forget and it's also less likely I'll do something like substitute the wrong variable somewhere.

These functions start very simply - running a single simulation run with a single parameter set, and build on one another. There are functions to run repeated simulations with the same parameter set, to run sweeps varying a subset of parameter values (possible with repetitions), and for running simulations using a set of arbitrarily defined parameter sets.

The functions for running simple parameter sweeps can save a lot of time during the testing and exploration phase of a project. They create a consistent directory structure that can be traversed by the scripts functions in `analysis_tools.py` to make use of the functions in `data_extractors.py`. More on these in the next sections. More complex sensitivity analysis might require hand-crafted scripts which probably belong in the `analysis` subdirectory and/or need their own  `run_tools` functions to manage them.

These functions could also have an argument to determine which model to run. For example, if the model is written in another language then I just pass a path to the script or binary (stored in `filepaths.py`) which gets turned into a commandline command). A similar method would work if you have multiple models to run. Storing all the parameters in the a dictionary means the whole parameter set can be forwarded to whatever model is required, even if they use different parameters.


## Data retrieval (`utilities/data_extractors.py`)
Contains functions to perform data retrieval, transformation and common calculations. Each of these functions will be specific to your project. I tend to write data extractors for even very simple tasks like retrieving a particular column from an output CSV file because, over the course of a project, it's common that the format of an output file changes. When this happens all the scripts using this file break, there's only one place to update it. Some data extractors might be more complex and/or call other data extractors to build on intermediary calculations, and having a single place to fix bugs in these functions helps too. Naming chunks of data processing logic by turning them into functions also improves readability.

The main disadvantage is that you'll frequently end up repeating file read operations and intermediate calculations which can slow things down. I usually find that this is a small price to pay for having a clean interface and better maintainability. If something ends up being particularly slow and you find you're running it a lot, one approach is to write the intermediate calculation result to disk in the run's output directory. When you call the `data_extractor` function for that calculation it first searches the output directory for the cached file and only calculate it again if it doesn't exist. Add a version number to the filename so that if you ever change how you calculate it you can increment the version number and only ever read in the latest version.

I try to make it so that each function only needs the simulation run's directory to work on, though you could modify the `analysis_tools.py` functions to forward on additional arguments. Also, if your output files are very large and you want to avoid repeatedly reading from the hard drive, you don't need to provide the directory as an argument. Instead read the output file once and provide a handle to that in-memory data instead.


## Analysis tools (`utilities/analysis_tools.py`)
Running simulations using the functions in `run_tools.py` means we end up with a standard directory structure for all the simulation output. This, in turn, means we can write reusable functions to perform traverse this directory structure automatically, and perform any of the functions we defined in `data_extractors.py`. This makes reading and processing data from large multi-dimensional sweeps of runs as straightforward as for single runs. These functions are supplied in `analysis_tools.py`. There are functions for extracting data from a set of repeat simulations, or from parameter sweeps. They require a path to a directory containing the repeats/sweep output and a reference to one of the `data_extractor.py` functions. The function will then traverse the directory structure applying the extractor function and storing whatever is returned by the extractor function in a particular format.

Being able to retrieve all the data for a set of parameter sweeps, and keeping it in a common data structure, makes the code less confusing. It also dramatically cuts down the amount of data wrangling spaghetti code in analysis scripts, so you don't need to read through a load of code to tell how the data for a particular parameter sweep is going to be organised, because you can just run `extract_from_sweep(outputPath, data_extractors.get_birth_death_ratios)` and you have it in a standard format. The data is stored as follows:

 * Data from a set of repeats (`analysis_tools.extract_from_repeats`) simple returns an array containing one element for each repeat run. The content of each element depends on whatever is returned by the `data_extractor` function you pass in.

 * Data from an N-dimensional parameter sweep (`analysis_tools.extract_from_sweep`) will generate an N-dimensional grid (or N+1 with repeat runs). Three things are returned in a tuple. The first thing returned is a list of parameter names that were varied in the sweep. These match the parameter names used in parameter files/dictionaries. They define the axis names of the grid and the order in which to index the grid. The second thing returned is a dictionary indexed by the parameter names, that contains the parameter values used in the sweep. These define the grid coordinates (valid indexing values). The third thing returned is the data itself. It's returned as a recursively nested dictionary, N levels deep (one for each parameter). This lets you access data for a particular run using the parameter values used to generate it. Such as `data[0.5]["high"][2000]` to index a particular parameter set in a sweep where three variables were varied. It's probably easiest to see/run the examples in `analysis/03_example_parameter_sweeps.py`.
