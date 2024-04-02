import numpy as np
import random as random
import sys

def Ncomputer():
 Sum = 0
 for k in S:
  if ms[k] != 0 and cs[k] < Nb and cs[k] > 0:
   Sum += ms[k]*(Nb - cs[k])
 return Sum
def initialize_motor_distributions(M,L,name_of_ms_file):
 global u  
 m = np.loadtxt(name_of_ms_file,dtype = int)
 b = [i for i,j in enumerate(m) if j != 0 and i > 0 and i < L-1]
 u = sum(m[1:L-1])
 if m[0] > 0:
  global m0
  m0 = 1
 return m,b
def initialize_cargo_distributions(L,name_of_file):
 global l,b
 c = np.loadtxt(name_of_file,dtype = int)
 C = [i for i,j in enumerate(c) if j > 0]
 A = []
 for index in C:
  if (index + 1 < L) and (index + 1 not in C):
   A.append(index)
 b = len(C)
 l = len(A)
 c0 = 0
 if c[0] > 0:
  c0 = 1
 return c,C,A,c0
def initialize_S_distributions():
 global N
 S = []
 if len(ms) >= len(C):
  for ind in C:
   if ms[ind] > 0 and cs[ind] < Nb:
    S.append(ind)
    N += ms[ind]*(Nb - cs[ind])
  return S
 for ind,val in enumerate(ms):
  if val > 0 and ind in C and cs[ind] < Nb:
   S.append(ind)
   N += val*(Nb - cs[ind])
 return S
def add_cargo():
 global b,m0,l,c0
 motors_to_bind = random.choice(range(np.minimum(ms[0],Nb))) + 1
 ms[0] -= motors_to_bind
 cs[0] = motors_to_bind
 C.append(0)
 c0 = 1
 b += motors_to_bind
 if cs[1] == 0:
  A.append(0)
  l += 1
 if ms[0] == 0:
  m0 = 0
  return
 if ms[0] > 0 and motors_to_bind < Nb:
  S.append(0)
def move_bulk_motor_left(Site):  
 Left_site = Site - 1
 ms[Site] -= 1
 ms[Left_site] += 1
 if Site == 1:
  global u,m0
  u -= 1
  m0 = 1 
  if ms[Site] == 0:
   B.remove(Site)
   if Site in S:
    S.remove(Site) 
  if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
    S.append(Left_site)  
  return
 # If the left site is still in the bulk.
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:
   S.remove(Site)
 if Left_site not in B:
  B.append(Left_site)
 if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)
def move_bulk_motor_right(Site): 
 Right_site = Site + 1
 ms[Site] -= 1
 ms[Right_site] += 1
 if Site == L-2:
  global u
  u -= 1 
  if ms[Site] == 0:
   B.remove(Site)
   if Site in S:  
    S.remove(Site)
  if cs[Right_site] > 0 and cs[Right_site] < Nb and Right_site not in S: 
   S.append(Right_site)
  return 
 # If the right site is still in the bulk.
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:    
   S.remove(Site)
 if cs[Right_site] > 0 and cs[Right_site] < Nb and Right_site not in S:
   S.append(Right_site)
def move_left_boundary_motor(): 
 ms[0] -= 1
 ms[1] += 1
 global u
 u += 1 
 if ms[0] == 0:
  global m0
  m0 = 0 
  if 0 in S:
   S.remove(0)
 if 1 not in B:
  B.append(1)
 if cs[1] > 0 and cs[1] < Nb and 1 not in S:
   S.append(1)
def move_right_boundary_motor():  
 Site = L-1
 Left_site = L-2 
 ms[Site] -= 1
 ms[Left_site] += 1
 global u
 u += 1
 if Left_site not in B:
  B.append(Left_site)
 if ms[Site] == 0:
  if Site in S:  
   S.remove(Site)
 if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)

# Finish cleaning this function up.
def unbind_motor(x):
 global b
 ms[x] += 1
 cs[x] -= 1
 b -= 1
 
 if x == 0:
  global m0
  m0 = 1
  if cs[0] == 0:
   global c0
   c0 = 0
   C.remove(0)
   if 0 in S:
    S.remove(0)
   return 0
  if 0 not in S:
   S.append(0)
  return -1
  
 if x == L-1:
  if cs[x] == 0:
   global c0
   c0 = 0
   return 0
  if 0 not in S:
   S.append(0)
  return -1
  
  
  
   
 if x > 0 and x < L-1:
  global u
  u += 1
  if x not in B:
   B.append(x)
 if cs[x] == 0:
  C.remove(x)
  if x in A:
   global l
   l -= 1
   A.remove(x) 
  if x > 0 and cs[x-1] > 0 and (x-1 not in A):
   A.append(x-1)
   l += 1   
 if (cs[x] == 0 or ms[x] == 0) and x in S:
  S.remove(x)
 if cs[x] == 0:
  global relax_time,step
  if step >= relax_time:
   return x   
 if cs[x] < Nb and cs[x] > 0 and ms[x] != 0:      
  if x not in S:
   S.append(x)
 return -1 
