# Example Python workflow for agent-based models
This is the readme for the workflow explanation. For the readme for the example model (containing instructions on how to run the examples) see `example_readme.md`.

If you want to get into the details then the place to start (besides this readme file) the example scripts in the `analysis` directory.


## Overall principles:
The setup described here is something I've slowly converged on over the years. I'm sure there are better ways to do a lot of these things (please do share them!) Some of it might be seem over-engineered, but it's also reusable with minimal modifications and comes with a lot of advantages which will make life easier in the long term (I promise)! I'm very interested to hear suggestions or to compare with other people's setups. None of it is specific to Python and could be implemented in any other language. Some probably is specific to data-generating simulation models, however, and is unlikely to generalise well to other types of projects.

The overall aims of organising a project like this are to:
1) Reduce the opportunity to make errors - humans aren't really very good at reading and writing code. It's incredibly easy to make mistakes, and if we're lucky this will break the code 'loudly' and produce and error message so we know to fix it. If we're unlucky, we'll introduce a more subtle bug which resulting in silent errors - and who knows if anyone will ever notice it! Besides writing tests for your code, organising your code to minimise the opportunity to make errors in the first place is the primary way to reduce these.

2) Reduce boilerplate code and the cognitive load required to run and extract data from your model(s). This frees up valuable cognitive resources for the actual science and analysis part of the job. If you're bogged down in mundane coding tasks, like manually setting parameter sweep values or remembering what directory structure and data format you used to store something, you have less time and energy to give to the science.



## Project structure
## Folder structure:
* Project root directory:
	* The git root repository directory (normally)
		* `model`: The model(s) itself.
		* `input_data`: Any input data used in the analysis or by the model.
		* `utilities`: Most of the good stuff is in here: important parameter sets, quality of life functions, tools for keeping everything organised. Lots of this is reusable between projects.
		* `tests`: Unit tests and any other tests. Larger tests of model behaviour might be better off in the `analysis` directory, especially if they're going to end up in a paper / supplementary.
		* `analysis`: One-off scripts which run a piece of analysis. They should ideally be self-contained, but might need to run in sequence.
		* `model_output`: Contains model output. This is usually excluded from the repository using .gitignore and backed up elsewhere.
		* `plots`: Plots created by the scripts in the `analysis` directory go here, usually in subdirectors which correspond to the analysis or planned manuscript figures etc.
	* Various "for me only" notes: E.g. Which thing I'm currently working on (because I'll forget over the weekend), what still needs doing, what I plan to bring up in the next meeting with my collaborators, pros and cons of getting a dog, anything that is important to the project but now want to be part of the git repository because it's not designed to be shared and doesn't need version control.


## The model (`model/simple_model.py`)
The main reason to have this separate from any other code is to make it easy to find, but for complex projects the model may be made up of many files. It can also be useful to keep them clearly separate when there are more than one model (which might use shared functions). This doesn't have to be Python, if the model is written in C++, for example, it might be a compiled binary.


## Parameters (`utilities/parameters.py`)
Defines important parameter sets. This includes the default values, but can also include other parameter sets that are used often e.g. particular scenarios that are important to your study. I find it useful to define additional parameter sets by creating an instance of the default parameters and modifying it. This sets up a hierarchy, so that if I need to change a default parameter later on, there's only one place to change it and the change will automatically propagage to any other parameter sets. There are different ways you might want to store and represent parameters, but often a dictionary will suffice (and has the advantage of being easily serialised).


## File paths (`utilities/filepaths.py`)
Defines important file paths. It's useful to define variables for any file path you reuse a lot for three reasons: 1) There's always one place to change them 2) You're less likely to make typos in, and 3) it helps readability and reduces long repetitive filepath concatenations. Typically I define, at a minimum, the project root, the model output directory and a directory for figures.


## Run tools (`utilities/run_tools.py`)
These are the functions I use to run simulations. I almost never run the model directly because there is always extra 'boilerplate' code needed to set up and clean up simulation runs, especially when running sets of simulations on parallel cores (which these functions support, too). And why repeat yourself when you can use a function? This helps because:
 1) It standardises the process by such enforcing a standard way of organising directory structure for sets of simulations; creating subdirectories, setting and storing random seeds and model parameters, etc.
 2) It reduces the chance I'll make a mistake by simplifying the process of setting up more complex sets of simulations. There is less to forget, less to test, lower cognitive load, and a single place to make changes if I need to update the process.

These functions start very simply - running a single simulation run with a single parameter set, and build on one another. There is a function to run repeat simulations using the same parameter set. This invokes the previous function multiple times and manages the output directories in a predictable way. There's a function to run N-dimensional gridded parameter sweeps, automatically substituting in the correct parameter values, setting up a consistent directory structure and for running the simulations (with or without repeats). Finally there's a function for running simulations for a set of defined parameter sets.

These tools dramatically simplify the code you need to actually run your models, which can be especially useful during the exploratory and testing phase of project. They also, importantly, create consistent output directory structure which means we can write functions to traverse output. That's what the functions in `analysis_tools.py` do.

These functions could also have an argument to determine which model to run. For example, if the model is written in another language then I just pass a path to the script or binary (stored in `filepaths.py`) which gets turned into a commandline command). Or if you have multiple models implemented in Python, you could pass the class or function as an argument, so long as there is a consistent interface to actually invoke the model.


## Data retrieval ('utilities/data_extractors.py' and 'utilities/analysis_tools.py')
Since we have ran our model using the functions provided by 'run_tools.py', we have model output stored with a predictable directory structure. The functions in `analysis_tools.py` are designed to traverse this directory structure to extract data. The functions in `data_extractors.py` are in charge of performing actual data retrieval for a single run of the simulation, and they only require the run's output directory to do this. These data extracting functions are passed as arguments to the different functions in `analysis_tools.py` to perform their jobs over different sets of simulations, for example repeats of the same parameter set or gridded parameter sweeps (for single runs, you can just use the 'data extractor' function directly).

Having a simple way to retrieve all the data for a set of parameter sweeps, and keeping it in a common data structure, makes the code less confusing. It also dramatically cuts down the amount of confusing data wrangling code and lets you focus on the good bits. You don't need remember how you organised your parameter sweep, what parameters you used, and how the output directories were set up, because it always follows the same pattern and you have functions to exploit taht consistency:
 * For data from a set of repeats (`analysis_tools.extract_from_repeats`) returns an array containing one element for each repeat run. The content of each element depends on whatever is returned by the `data_extractor` function you pass in.
 * For data from an N-dimensional parameter sweep (`analysis_tools.extract_from_sweep`) will generate an N-dimensional grid (or N+1 with repeat runs). Three things are returned in a tuple. The first thing returned is a list of parameter names that were varied in the sweep. These match the parameter names used in parameter files/dictionaries. They define the axis names of the grid and the order in which to index the grid. The second thing returned is a dictionary indexed by the parameter names, that contains the parameter values used in the sweep. These define the grid coordinates (valid indexing values). The third thing returned is the data itself. It's returned as a recursively nested dictionary, N levels deep (one for each parameter). This lets you access data for a particular run using the parameter values used to generate it. Such as `data[0.5]["high"][2000]` to index a particular parameter set in a sweep where three variables were varied. It's probably easiest to see/run the examples in `analysis/03_example_parameter_sweeps.py`.

Note that many of the functions in `data_extractors.py` end up being very simple, perhaps just parsing a csv files, but it is still useful to write functions to do this job. It helps readability, because the function (hopefully) has a descriptive name, and it means that when something changes (a file name, a file format) then there's only one place to make the update and you can sleep easier at night knowing there are no relics hanging around leading to silent errors.

Data extracting/processing functions can be much more complex, however. They can call other data extracting functions and use them to perform any calculations you like.

The downside of using this setup is that you'll frequently end up repeating file read operations and intermediate calculations which can slow things down. I usually find that this is a small price to pay for having a clean interface and better maintainability. If something ends up being particularly slow and you find you're running it a lot, one approach is to write the intermediate calculation result to disk in the run's output directory. When you call the `data_extractor` function for that calculation it first searches the output directory for the cached file and only calculate it again if it doesn't exist. You can also add a version number to the filename so that if you ever change how you calculate it you can increment the version number and only ever read in the latest version.



## Analysis tools (`utilities/analysis_tools.py`)
Running simulations using the functions in `run_tools.py` means we end up with a standard directory structure for all the simulation output. This, in turn, means we can write reusable functions to perform traverse this directory structure automatically, and perform any of the functions we defined in `data_extractors.py`. This makes reading and processing data from large multi-dimensional sweeps of runs as straightforward as for single runs. These functions are supplied in `analysis_tools.py`. There are functions for extracting data from a set of repeat simulations, or from parameter sweeps. They require a path to a directory containing the repeats/sweep output and a reference to one of the `data_extractor.py` functions. The function will then traverse the directory structure applying the extractor function and storing whatever is returned by the extractor function in a particular format.


## Examples you can run
The `root/analysis` directory contains examples you can run, which demonstrate the functionality described above using a simple toy model. Make sure to run them with `root` as your working directory.