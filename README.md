This code was written by Freddy Alexis Cisneros using python3 to simulate kinesin-driven transport when the cargo undergoes TASEP dynamics and unbound motors undergo Brownian diffusion. To run simulations using this code on the terminal type and enter

python3 TASEPcargodynamics.py 1000 10

on the terminal line where 1000 is the number of motors both bound and unbound in the system and 10 in this case is the rate at which a motor cargo complex MCC attaches to the microtubule.

The number of binding sites on the cargo are Nb = 3. This code can clearly be adapted to read in many more paramters but I left in this format since parameters such as k_on, k_off, etc. were to remain fixed.

Many checks of the code were made including the following to ensure that S, A, L, u, l, b, m0, and c0 are all consistent with one-another.
 '''
 if sum(ms[1:L-1]) != u:
  print("bulk motors and u not equal!")
  break
  
 for indx,val in enumerate(cs):
  if val > 0 and indx not in C:
   print("cs and C not consistent!")
   break
  if val == 0 and indx in C:
   print("cs and C not consistent!")
   break
 
 if sum(ms) + sum(cs) != Motors:
  print("sum(cs) + sum(ms) not equal to motor number!")
  break 
  
 for indx,val in enumerate(ms):
  if indx in S:
   if cs[indx] == 0 or val == 0:
    print("S is not consistent with cs and ms!")
    print(S)
    print(ms)
    print(cs)
    break
 '''
