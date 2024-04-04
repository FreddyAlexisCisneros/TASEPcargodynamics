#************************************************************************
# Written by Freddy Alexis Cisneros.                                    *
# The following code is working properly and has been updated 4/4/2024. *
#************************************************************************
import numpy as np
import random as random
import sys

def compute_N():
 Sum = 0
 for k in S:
  Sum += ms[k]*(Nb - cs[k])
 return Sum

def initialize_motor_distributions(M,L,name_of_ms_file):
 global u  
 m = np.loadtxt(name_of_ms_file,dtype = int)
 b = [ind for ind,val in enumerate(m) if val != 0 and ind > 0 and ind < L-1]
 u = sum(m[1:L-1])
 global m0
 m0 = 1 if m[0] > 0 else 0
 return m,b

def initialize_cargo_distributions(L,name_of_file):
 global l,b
 c = np.loadtxt(name_of_file,dtype = int)
 C = [ind for ind,val in enumerate(c) if val > 0]
 A = [ind for ind in C if ind+1 < L and ind + 1 not in C]
 b = len(C)
 l = len(A)
 c0 = 1 if c[0] > 0 else 0
 return c,C,A,c0

def initialize_S_distributions():
 if len(ms) >= len(C):
  S = [ind for ind in C if ms[ind] > 0 and cs[ind] < Nb]
  return S
 S = [ind ind,val in enumerate(ms) if val > 0 and ind in C and cs[ind] < Nb]
 return S

def add_cargo():
 motors_to_bind = random.randint(1,np.minimum(ms[0],Nb))
 ms[0] -= motors_to_bind
 cs[0] = motors_to_bind
 C.append(0)
 global b,m0,l,c0
 c0 = 1
 b += motors_to_bind
 if cs[1] == 0:
  A.append(0)
  l += 1 
 if ms[0] > 0 and motors_to_bind < Nb:
  S.append(0)
  return
 elif ms[0] == 0: 
  m0 = 0

def move_bulk_motor_left(Site):  
 Left_site = Site - 1
 ms[Site] -= 1
 ms[Left_site] += 1
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:
   S.remove(Site)
 if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)  
 if Site > 1
  if Left_site not in B:
   B.append(Left_site)
  return 
 global u,m0
 u -= 1
 m0 = 1 
  
def move_bulk_motor_right(Site): 
 Right_site = Site + 1
 ms[Site] -= 1
 ms[Right_site] += 1
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:    
   S.remove(Site)
 if cs[Right_site] > 0 and cs[Right_site] < Nb and Right_site not in S:
   S.append(Right_site)
 if Right_site < L-2:
  if Right_site not in B:
   B.append(Left_site)
  return
 global u
 u -= 1 

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
 if 1 in B:
  if cs[1] > 0 and cs[1] < Nb and 1 not in S:
   S.append(1)
  return
 B.append(1)

def move_right_boundary_motor():  
 Site = L-1
 Left_site = L-2 
 ms[Site] -= 1
 ms[Left_site] += 1
 global u
 u += 1
 if ms[Site] == 0 and Site in S:  
  S.remove(Site) 
 if Left_site in B:
  if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)
  return  
 B.append(Left_site)
