This code was written by Freddy Alexis Cisneros using python3 to simulate kinesin-driven transport when the cargo undergoes TASEP dynamics and unbound motors undergo Brownian diffusion. To run simulations using this code on the terminal type and enter

python3 TASEPcargodynamics.py 1000 10

on the terminal line where 1000 is the number of motors both bound and unbound in the system and 10 in this case is the rate at which a motor cargo complex MCC attaches to the microtubule.

The number of binding sites on the cargo are Nb = 3. This code can clearly be adapted to read in many more paramters but I left in this format since parameters such as k_on, k_off, etc. were to remain fixed.
