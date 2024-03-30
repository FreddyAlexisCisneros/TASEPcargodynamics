This code was written using python version python3, not sure how well it will perform using earlier versions.

This code performs simulations for kinesin driven sites where the cargo undergoes TASEP dynamics, meaning that there can be at most one cargo per site on the microtubule.
The way this code is to be called on the terminal is you type:

python3 TASEPcargodynamics.py 1000 10

where I have specified that I want the simulation to begin with 1000 motors and an alpha value of 1 where alpha is the rate at which cargo enters the microtubule.


The lag in printing data to the .txt files was resolved by using the flush function. Again and again.
