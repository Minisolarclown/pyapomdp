Installation Instructions

1. Install [Julia v0.6.4](https://julialang.org/downloads/oldreleases/)
2. Open a new terminal and run `julia`
3. Run `Pkg.add("POMDPS")`
4. Run `Pkg.add("POMDPModels")`
5. Run `Pkg.add("POMDPToolbox")`
6. Run `Pkg.clone("https://github.com/JuliaPOMDP/QMDP.jl")`
7. Run `Pkg.clone("https://github.com/JuliaPOMDP/DiscreteValueIteration.jl")`
8. Close Julia by entering CTRL-D. If that does not work, follow that up with CTRL-C.
9. Still in the terminal, run `cd ~/julia/v0.6/QMDP`
10. Run `git fetch --all`
11. Run `git checkout 0.6-version`
12. Run `cd ~/julia/v0.6/DiscreteValueIteration`
13. Run `git fetch --all`
14. Run `git checkout v0.1.0`
15. Change the terminal directory to this aPOMDP project directory
16. In ./src/apomdp.jl, remove all references to SARSOP
17. Run `julia ./src/hri_simulator.jl`

