Installation Instructions

1. Install [Julia v0.6.4](https://julialang.org/downloads/oldreleases/)
2. Open a new terminal and run `julia`
3. Run `Pkg.add("POMDPs")`
4. Run `Pkg.add("POMDPModels")`
5. Run `Pkg.clone("https://github.com/JuliaPOMDP/QMDP.jl")`
6. Run `Pkg.clone("https://github.com/JuliaPOMDP/DiscreteValueIteration.jl")`
7. Run `Pkg.clone("https://github.com/JuliaCollections/IterTools.jl")`
8. Close Julia by entering CTRL-D. If that does not work, follow that up with CTRL-C.
9. Still in the terminal, run `cd ~/.julia/v0.6/QMDP`
10. Run `git fetch --all`
11. Run `git checkout 0.6-version`
12. Run `cd ~/.julia/v0.6/DiscreteValueIteration`
13. Run `git fetch --all`
14. Run `git checkout v0.1.0`
15. Run `cd ~/.julia/v0.6/IterTools`
16. Run `git fetch --all`
17. Run `git checkout v0.2.1`
18. Change the terminal directory back to the aPOMDP project directory
19. In ./src/apomdp.jl, remove all references to SARSOP
20. Run `touch results/random_qmdp_isvr_200_-1_0_10000_new_struct_space_cenas.yaml`
21. Run `julia ./src/hri_simulator.jl`
