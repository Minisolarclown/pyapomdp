# The αPOMDP framework for User-Adaptive Decision Making

## Contents
This package contains two main elements:
* Our simulation suite (Julia code used in our simulations, Python plotter);
* A ROS package for interfacing with real robots.

The whole code is packaged as a ROS package, with both ROS and non-ROS-specific code in it. This allowed us to have a single implementation of the aPOMDP "class" that is used both by the simulator and the ROS stuff.

The package is composed of a few main files:
* Core:
  * `apomdp.jl` defines the aPOMDP object, which is the core of our solution. It contains our definitions of the POMDP problem, including our learning facilities and the various rewards we have implemented. It also contains a function to log the results of a trial run.
  * `plotter.py` is a python script that can be used to plot the results of any trial in which the logging function is used. It produces the figures we have used throughout the paper.
  * `apomdp_tests.jl` contains a number of small "unit tests" for the aPOMDP object that come in handy to check if everything is running smoothly.
* Simulation-specific:
  *  `hri_simulator.jl` implements our simulator. It basically consists of a main function that implements the interaction loop (get action, get reward, transition state, learn), with a few auxiliary functions.
* ROS-specific:
  * `policy_calculator.jl` is our ROS-facing interface for `apomdp.jl`. It serves a ROS service defined in `GetAction.srv`, wherein it receives an observed state and returns the appropriate action. It simultaneously (and in parallel with the service) integrates the observed transitions for learning, and re-calculates the policy after each integration.
  * `apomdp_conductor.jl` implements similar logic as the `hri_simulator.jl`, interfacing with [the GrowMu robot](www.growmeup.eu) in order to speak, move around, listen to the user, etc...

## Requirements
This package was tested under:
* [Julia](https://julialang.org/) 0.6 (0.5 is known not to work)
* [ROS](http://www.ros.org/) Indigo (later versions should work)
* Latest versions of [JuliaPOMDP](https://github.com/JuliaPOMDP/POMDPs.jl) and related packages, as of October 2017
* ROS interfacing was obtained using the [RobotOS](https://github.com/jdlangs/RobotOS.jl) Julia package

## Installation Instructions

1. Install [Julia v0.6.4](https://julialang.org/downloads/oldreleases/).
2. Add Julia 0.6 to your operating system's PATH. 
3. Open a new terminal and run `julia`
4. Run `Pkg.add("POMDPs")`
5. Run `Pkg.add("POMDPModels")`
6. Run `Pkg.add("LightXML")`
7. Run `Pkg.clone("https://github.com/JuliaPOMDP/QMDP.jl")`
8. Run `Pkg.clone("https://github.com/JuliaPOMDP/DiscreteValueIteration.jl")`
9. Run `Pkg.clone("https://github.com/JuliaCollections/IterTools.jl")`
10. Run `Pkg.clone("https://github.com/JuliaPOMDP/SARSOP.jl")`
11. Run `Pkg.clone("https://github.com/JuliaPOMDP/POMDPXFiles.jl")`
12. Close Julia by running `exit()`.
14. Still in the terminal, run `cd ~/.julia/v0.6/QMDP`
15. Run `git fetch --all`
16. Run `git checkout 0.6-version`
17. Run `cd ~/.julia/v0.6/DiscreteValueIteration`
18. Run `git fetch --all`
19. Run `git checkout v0.1.0`
20. Run `cd ~/.julia/v0.6/IterTools`
21. Run `git fetch --all`
22. Run `git checkout v0.2.1`
23. Run `cd ~./.julia/v0.6/SARSOP`
24. Run `git fetch --all`
25. Run `git checkout 4410c1f`
26. Run `cd ~./.julia/v0.6/POMDPXFiles`
27. Run `git fetch --all`
28. Run `git checkout 0.6-version`
29. Change the terminal directory back to the aPOMDP project directory

As a test, run the following commands. If you see the number 1 followed by o's, everything is working correctly and you can halt the program. Otherwise, it may run for a very long time.

30. Run `touch results/random_qmdp_isvr_200_-1_0_10000_new_struct_space_cenas.yaml`
31. Run `julia ./src/hri_simulator.jl`

## Usage
### Simulations
The main entry point is the `hri_simulator.jl` script, which is our main simulator. This makes use of the "class" defined in `apomdp.jl`. The script contains the various configurations used for producing the results in the paper.


### ROS
To use this package with a robot, you will need to use the `apomdp_conductor.py` script as a guide for implementing your own script that interfaces with your robot. In our case, we have used [the GrowMu robot](www.growmeup.eu), and our proprietary (maybe I'll get to release it some day) toolset for interfacing with it.

You will also have to configure the `policy_calculator.jl` script to work on your definitions of the action and observation/state spaces. These should be a matter of re-configuring the parameters used to construct the `pomdp` object.

### Plotting Results
In both cases, YAML files containing the results will be produced. The `plotter.py` script can be used to obtain the illustrations used throughout the papers from both data sources, simply by configuring which files it looks at in the main function.

